#include <stdio.h>
#include <stdlib.h>
#ifdef __linux__
#include <ncurses.h>
#endif

// Keyboard Driver for CorvOS
// Real hardware input using ncurses

void keyboard_init() {
#ifdef __linux__
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
#endif
    printf("Keyboard Driver Initialized (ncurses)\n");
}

char keyboard_read() {
#ifdef __linux__
    return getch();
#else
    char c;
    scanf("%c", &c);
    return c;
#endif
}

void keyboard_close() {
#ifdef __linux__
    endwin();
#endif
}