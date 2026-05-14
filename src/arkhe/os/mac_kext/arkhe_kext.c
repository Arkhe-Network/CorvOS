// arkhe_kext.c
#include <mach/mach_types.h>
#include <sys/systm.h>
#include <sys/conf.h>

/* Minimal character device to simulate macOS kext hardware access */

static int arkhe_open(dev_t dev, int flags, int devtype, struct proc *p) {
    printf("arkhe_kext: device opened\n");
    return 0;
}

static int arkhe_close(dev_t dev, int flags, int devtype, struct proc *p) {
    printf("arkhe_kext: device closed\n");
    return 0;
}

static struct cdevsw arkhe_cdevsw = {
    arkhe_open,
    arkhe_close,
    eno_rdchk,
    eno_ioctl,
    eno_stop,
    eno_reset,
    eno_select,
    eno_mmap,
    eno_strat,
    eno_getc,
    eno_putc,
    D_TTY
};

kern_return_t arkhe_kext_start(kmod_info_t * ki, void *d) {
    printf("Arkhe Kext started. MacOS is now a substrate.\n");
    return KERN_SUCCESS;
}

kern_return_t arkhe_kext_stop(kmod_info_t *ki, void *d) {
    printf("Arkhe Kext stopped.\n");
    return KERN_SUCCESS;
}
