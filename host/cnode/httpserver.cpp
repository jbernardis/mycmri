#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>
#include <boost/asio.hpp>
#include <cstdlib>
#include <iostream>
#include <string>
#include <thread>

#include "httpserver.h"

namespace beast = boost::beast;         // from <boost/beast.hpp>
namespace http = beast::http;           // from <boost/beast/http.hpp>
namespace net = boost::asio;            // from <boost/asio.hpp>
using tcp = boost::asio::ip::tcp;       // from <boost/asio/ip/tcp.hpp>

int httpReq;			// pipe to which http requests are written
int httpResp;			// pipe from which I resd http responses
	
std::thread * thrHttp;

class http_connection : public std::enable_shared_from_this<http_connection> {
public:
    http_connection(tcp::socket socket)
        : socket_(std::move(socket))
    {
    }

    void start() {
        read_request();
        check_deadline();
    }

private:
    tcp::socket socket_;
	std::string names[16];
    beast::flat_buffer buffer_{8192};
    http::request<http::dynamic_body> request_;
    http::response<http::dynamic_body> response_;

    net::steady_timer deadline_{
        socket_.get_executor(), std::chrono::seconds(60)};

    void read_request() {
        auto self = shared_from_this();

        http::async_read(
            socket_,
            buffer_,
            request_,
            [self](beast::error_code ec,
                std::size_t bytes_transferred)
            {
                boost::ignore_unused(bytes_transferred);
                if(!ec)
                    self->process_request();
            });
    }

    void process_request() {
        response_.version(request_.version());
        response_.keep_alive(false);

        switch(request_.method())
        {
        case http::verb::get:
            response_.result(http::status::ok);
            response_.set(http::field::server, "Beast");
            create_response();
            break;

        default:
            // We return responses indicating an error if
            // we do not recognize the request method.
            response_.result(http::status::bad_request);
            response_.set(http::field::content_type, "text/plain");
            beast::ostream(response_.body())
                << "Invalid request-method '"
                << std::string(request_.method_string())
                << "'";
            break;
        }

        write_response();
    }

    void create_response() {
		std::string tgt = std::string(request_.target());
		std::string cmd;
		std::string parms;

		class httpMessage *req = new httpMessage();
		req->address = 0;
		req->nargs = 0;

		size_t pos = 0;
		if ((pos = tgt.find("?")) != std::string::npos) {
			req->command = tgt.substr(0, pos);
			parms = tgt.substr(pos+1);
		}
		else {
			req->command = tgt;
			parms = "";
		}
		
		int nparms = 0;
		std::string p[8];
		while ((pos = parms.find("&")) != std::string::npos) {
			p[nparms++] = parms.substr(0, pos);
			parms.erase(0, pos + 1);
		}
		if (parms.length() > 0) {
			p[nparms++] = parms;
		}
		int np = 0;
		std::string nm, val;
		for (int i = 0; i<nparms; i++) {
			if ((pos = p[i].find("=")) != std::string::npos) {
				nm = p[i].substr(0, pos);
				val = p[i].substr(pos+1);
			}
			else {
				nm = p[i];
				val = "";
			}

			if (nm == "addr") {
				req->address = std::stoi(val);
			}
			else {
				req->names[np]  = nm;
				req->args[np] = std::stoi(val);
				np++;
			}
		}

		response_.set(http::field::content_type, "text/plain");
		req->nargs = np;
		int rc = write(httpReq, &req, sizeof(req));

		if (rc != sizeof(req)) {
			perror("http outon write");
			exit(1);
		}

		struct pollfd fds[1];
		httpMessageBody *rsp;
		fds[0].fd = httpResp;
		fds[0].events = POLLIN;
		poll(fds, 1, 500);

		if (!(fds[0].revents & POLLIN)) {
			beast::ostream(response_.body()) 
				<< "no response from server\n";
		}
		else {
			int rc = read(httpResp, &rsp, sizeof(rsp));
			if (rc != sizeof(rsp)) {
				beast::ostream(response_.body()) 
					<< "error reading response from server\n";
			}
			else {
				beast::ostream(response_.body()) 
					<< "rc=" << rsp->rc << ";msg=\"" << rsp->body << "\"";
				delete rsp;
			}
		}
    }

    void write_response() {
        auto self = shared_from_this();

        response_.content_length(response_.body().size());

        http::async_write(
            socket_,
            response_,
            [self](beast::error_code ec, std::size_t)
            {
                self->socket_.shutdown(tcp::socket::shutdown_send, ec);
                self->deadline_.cancel();
            });
    }

    void check_deadline() {
        auto self = shared_from_this();

        deadline_.async_wait(
            [self](beast::error_code ec)
            {
                if(!ec)
                {
                    self->socket_.close(ec);
                }
            });
    }
};

void http_server(tcp::acceptor& acceptor, tcp::socket& socket) {
  acceptor.async_accept(socket,
      [&](beast::error_code ec) {
          if(!ec)
              std::make_shared<http_connection>(std::move(socket))->start();
          http_server(acceptor, socket);
      });
}

void serverThread(boost::asio::ip::address address, unsigned short port) {
    try {
        net::io_context ioc{1};

        tcp::acceptor acceptor{ioc, {address, port}};
        tcp::socket socket{ioc};
        http_server(acceptor, socket);

        ioc.run();
    }
    catch(std::exception const& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        exit(EXIT_FAILURE);
    }
}

void startHttpServer(boost::asio::ip::address address, unsigned short port, int pReq, int pResp) {
	httpReq = pReq;
	httpResp = pResp;

	thrHttp = new std::thread(serverThread, address, port);
}
