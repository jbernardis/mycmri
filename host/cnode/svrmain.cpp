#include <boost/beast/http.hpp>
#include <boost/asio.hpp>

#include <cstdlib>
#include <iostream>
#include <string>

#include "httpserver.h"

namespace net = boost::asio;            // from <boost/asio.hpp>

int main(int argc, char* argv[]) {
	// Check command line arguments.
	if(argc != 3) {
		std::cerr << "Usage: " << argv[0] << " <address> <port>\n";
		std::cerr << "  For IPv4, try:\n";
		std::cerr << "    receiver 0.0.0.0 80\n";
		std::cerr << "  For IPv6, try:\n";
		std::cerr << "    receiver 0::0 80\n";
		return EXIT_FAILURE;
	}

	auto const address = net::ip::make_address(argv[1]);
	unsigned short port = static_cast<unsigned short>(std::atoi(argv[2]));

    int pipeReq[2];
    if (pipe(pipeReq) != 0) {
        perror("HTTP request pipe");
        exit(1);
    }

    int pipeResp[2];
    if (pipe(pipeResp) != 0) {
        perror("HTTP response pipe");
        exit(1);
    }

	// pipe fds for use by the server thread;
	//httpReq = pipeReq[1];
	//httpResp = pipeResp[0];

	startHttpServer(address, port, pipeReq[1], pipeResp[0]);

    struct pollfd fds[1];
    class httpMessage *request;
    fds[0].fd = pipeReq[0];
    fds[0].events = POLLIN;
	while (true) {
		poll(fds, 1, 100);

		if (!(fds[0].revents & POLLIN))
			continue;

		if (read(pipeReq[0], &request, sizeof(request)) != sizeof(request)) {
			perror("http request read");
		}
		else {
			httpMessageBody * resp = new httpMessageBody();
			resp->body = "Here is my response";
			resp->rc = 0;
			int rc = write(pipeResp[1], &resp, sizeof(resp));
            if (rc != sizeof(resp)) {
                perror("http response write");
                exit(1);
            }

			delete request;
		}
	}


	return 0;
}

