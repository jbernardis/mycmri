// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#define PORT 8001
   

int nextMessage(int skt, char * buff) {
	int totalRead = 0;
	union {
		short readLen;
		unsigned char readChars[2];
	} u;
	int nRead;
	short msgLen;
			
	// first et the 2 byte length
	while (totalRead < 2) {
		nRead = read(skt, u.readChars+totalRead, 2-totalRead);
		if (nRead == 0)
			return -1;

		totalRead = totalRead + nRead;
	}
	
	if (u.readLen > 0) {
		totalRead = 0;

		while (totalRead < u.readLen) {
			nRead = read(skt, buff+totalRead, u.readLen-totalRead);
			if (nRead == 0)
				return -1;

			totalRead = totalRead + nRead;
		}
	}
	return totalRead;
}

int main(int argc, char const *argv[])
{
    int sock = 0, valread;
    struct sockaddr_in serv_addr;
    const char *hello = "Hello from client";
    char buffer[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }
   
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
       
    // Convert IPv4 and IPv6 addresses from text to binary form
    if(inet_pton(AF_INET, "192.168.1.142", &serv_addr.sin_addr)<=0) 
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }
   
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }
	short msgLen;
	while (true) {
		valread = nextMessage(sock, buffer);
		if (valread <= 0)
			break;

		buffer[valread] = '\0';
		printf("%s\n", buffer);
	}
    return 0;
}
