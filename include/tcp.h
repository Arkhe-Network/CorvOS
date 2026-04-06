#ifndef TCP_H
#define TCP_H

int net_init();
int tcp_connect(const char *ip, int port);
int tcp_send(int sock, const char *data, int len);
int tcp_recv(int sock, char *buffer, int len);
void tcp_close(int sock);

#endif