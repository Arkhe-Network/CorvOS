#include <stdio.h>
#include <stdlib.h>
#ifdef __linux__
#include <ncurses.h>
#endif

// Mouse Driver for CorvOS
// Basic mouse input using ncurses

typedef struct {
    int x, y;
    int button;
} MouseEvent;

void mouse_init() {
#ifdef __linux__
    mousemask(ALL_MOUSE_EVENTS, NULL);
#endif
    printf("Mouse Driver Initialized\n");
}

MouseEvent mouse_read() {
    MouseEvent ev = {0, 0, 0};
#ifdef __linux__
    MEVENT event;
    if (getmouse(&event) == OK) {
        ev.x = event.x;
        ev.y = event.y;
        ev.button = event.bstate;
    }
#endif
    return ev;
}