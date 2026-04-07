#ifndef ARKHE_DAEMON_H
#define ARKHE_DAEMON_H

void arkhe_daemon_init();
void arkhe_daemon_run();
void arkhe_daemon_command(const char *cmd);
float arkhe_get_global_coherence();

#endif
