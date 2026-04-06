#ifndef MOUSE_H
#define MOUSE_H

typedef struct {
    int x, y;
    int button;
} MouseEvent;

void mouse_init();
MouseEvent mouse_read();

#endif