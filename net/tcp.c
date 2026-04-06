#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

// Simple TCP Network Driver for CorvOS
// Basic TCP client/server functionality

int net_init() {
    printf("Network Driver Initialized\n");
    return 0;
}

int tcp_connect(const char *ip, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return -1;

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_pton(AF_INET, ip, &server_addr.sin_addr);

    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        close(sock);
        return -1;
    }
    return sock;
}

int tcp_send(int sock, const char *data, int len) {
    return send(sock, data, len, 0);
}

int tcp_recv(int sock, char *buffer, int len) {
    return recv(sock, buffer, len, 0);
}

void tcp_close(int sock) {
    close(sock);
}