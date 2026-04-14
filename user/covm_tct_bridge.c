// covm_tct_bridge.c — Ponte entre /dev/covm e o TCT digital twin
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
// Assuming json-c is available or simulated
#include <json-c/json.h>

#define COVM_IOCTL_MAGIC 'C'
#define COVM_IOCTL_INIT      _IO(COVM_IOCTL_MAGIC, 1)
#define COVM_IOCTL_MEASURE   _IOWR(COVM_IOCTL_MAGIC, 2, struct covm_measure_arg)
#define COVM_IOCTL_TUNE_TAU  _IOW(COVM_IOCTL_MAGIC, 3, struct covm_tune_arg)

struct covm_measure_arg {
    unsigned long long cobit_id;
    double lambda2;
};

int tct_send_command(const char *op, unsigned long long id, double *result) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(42000);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);

    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("connect");
        return -1;
    }

    json_object *jcmd = json_object_new_object();
    json_object_object_add(jcmd, "op", json_object_new_string(op));
    json_object_object_add(jcmd, "id", json_object_new_uint64(id));

    const char *json_str = json_object_to_json_string(jcmd);
    send(sock, json_str, strlen(json_str), 0);

    char buffer[1024] = {0};
    recv(sock, buffer, sizeof(buffer), 0);
    close(sock);

    json_object *jresp = json_tokener_parse(buffer);
    json_object *jstatus = json_object_object_get(jresp, "status");
    if (jstatus && strcmp(json_object_get_string(jstatus), "OK") == 0) {
        json_object *jlambda = json_object_object_get(jresp, "lambda2");
        if (jlambda) *result = json_object_get_double(jlambda);
        json_object_put(jresp);
        json_object_put(jcmd);
        return 0;
    }
    if (jresp) json_object_put(jresp);
    json_object_put(jcmd);
    return -1;
}

int main() {
    int fd = open("/dev/covm", O_RDWR);
    if (fd < 0) { perror("open /dev/covm"); return 1; }

    // 1. Cria COBIT no kernel
    unsigned long long cobit_id;
    if (ioctl(fd, COVM_IOCTL_INIT, &cobit_id) < 0) {
        perror("ioctl INIT");
        return 1;
    }
    printf("[Bridge] COBIT criado no kernel: id=%llu\n", cobit_id);

    // 2. Mede localmente
    struct covm_measure_arg meas = { .cobit_id = cobit_id };
    if (ioctl(fd, COVM_IOCTL_MEASURE, &meas) == 0) {
        printf("[Bridge] λ₂ local = %.6f\n", meas.lambda2);
    }

    // 3. Envia para o TCT Twin (simula GEOM_SWAP ou medição)
    double tct_lambda;
    if (tct_send_command("COH_MEASURE", cobit_id, &tct_lambda) == 0) {
        printf("[Bridge] TCT Twin respondeu: λ₂ = %.6f\n", tct_lambda);
    }

    close(fd);
    return 0;
}
