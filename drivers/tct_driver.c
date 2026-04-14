// tct_driver.c — Driver PCIe para TCT físico (CVD hardware)
#include <linux/module.h>
#include <linux/pci.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/mm.h>
#include <linux/interrupt.h>
#include <linux/delay.h>
#include <linux/slab.h>

#define TCT_VENDOR_ID 0x1A2B  // Placeholder: ID do dispositivo TCT
#define TCT_DEVICE_ID 0xC0DE

#define TCT_REG_FREQ       0x00  // Registrador de frequência (em Hz)
#define TCT_REG_PHASE      0x08  // Registrador de fase (em rad * 1e6)
#define TCT_REG_TAU        0x10  // Registrador de criticalidade τ
#define TCT_REG_CTRL       0x18  // Controle (bit 0: enable, bit 1: trigger)
#define TCT_REG_STATUS     0x20  // Status (bit 0: lock, bit 1: temp_ok)
#define TCT_REG_LAMBDA2    0x28  // λ₂ medido

struct tct_device {
    struct pci_dev *pdev;
    void __iomem *mmio;
    struct cdev cdev;
    dev_t dev_num;
    struct device *device;
};

static struct tct_device *g_tct = NULL;

// ============================================================================
// PCIe Probe e Remove
// ============================================================================
static int tct_probe(struct pci_dev *pdev, const struct pci_device_id *id) {
    int ret;
    struct tct_device *tct;

    ret = pci_enable_device(pdev);
    if (ret) return ret;

    ret = pci_request_regions(pdev, "tct");
    if (ret) goto disable;

    tct = kzalloc(sizeof(*tct), GFP_KERNEL);
    if (!tct) { ret = -ENOMEM; goto release; }

    tct->pdev = pdev;
    tct->mmio = pci_iomap(pdev, 0, 0);
    if (!tct->mmio) { ret = -ENOMEM; goto free; }

    pci_set_drvdata(pdev, tct);
    g_tct = tct;

    // Configuração inicial: 4.20 THz, τ = 1.0
    writel(4200000000000ULL & 0xFFFFFFFF, tct->mmio + TCT_REG_FREQ);
    writel((4200000000000ULL >> 32) & 0xFF, tct->mmio + TCT_REG_FREQ + 4);
    writeq(0x3FF0000000000000ULL, tct->mmio + TCT_REG_TAU);  // 1.0 em double

    printk(KERN_INFO "[TCT] Dispositivo físico inicializado. Freq: 4.20 THz, τ: 1.0\n");
    return 0;

free: kfree(tct);
release: pci_release_regions(pdev);
disable: pci_disable_device(pdev);
    return ret;
}

static void tct_remove(struct pci_dev *pdev) {
    struct tct_device *tct = pci_get_drvdata(pdev);
    iounmap(tct->mmio);
    kfree(tct);
    pci_release_regions(pdev);
    pci_disable_device(pdev);
    g_tct = NULL;
}

static const struct pci_device_id tct_ids[] = {
    { PCI_DEVICE(TCT_VENDOR_ID, TCT_DEVICE_ID) },
    { 0, }
};
MODULE_DEVICE_TABLE(pci, tct_ids);

static struct pci_driver tct_pci_driver = {
    .name = "tct",
    .id_table = tct_ids,
    .probe = tct_probe,
    .remove = tct_remove,
};

// ============================================================================
// Operações de Dispositivo de Caractere (/dev/tct0)
// ============================================================================
static int tct_open(struct inode *inode, struct file *filp) {
    filp->private_data = g_tct;
    return 0;
}

static long tct_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
    struct tct_device *tct = filp->private_data;
    if (!tct || !tct->mmio) return -ENODEV;

    switch (cmd) {
        case 0x01:  // TCT_SET_FREQ
            writeq(*(uint64_t*)arg, tct->mmio + TCT_REG_FREQ);
            break;
        case 0x02:  // TCT_SET_PHASE
            writeq(*(uint64_t*)arg, tct->mmio + TCT_REG_PHASE);
            break;
        case 0x03:  // TCT_SET_TAU
            writeq(*(uint64_t*)arg, tct->mmio + TCT_REG_TAU);
            break;
        case 0x04:  // TCT_TRIGGER
            writel(0x2, tct->mmio + TCT_REG_CTRL);  // Pulso único
            break;
        case 0x10:  // TCT_GET_LAMBDA2
            *(uint64_t*)arg = readq(tct->mmio + TCT_REG_LAMBDA2);
            break;
        case 0x11:  // TCT_GET_STATUS
            *(uint32_t*)arg = readl(tct->mmio + TCT_REG_STATUS);
            break;
        default:
            return -ENOTTY;
    }
    return 0;
}

static struct file_operations tct_fops = {
    .owner = THIS_MODULE,
    .open = tct_open,
    .unlocked_ioctl = tct_ioctl,
};

// ============================================================================
// Inicialização do Módulo
// ============================================================================
static int __init tct_init(void) {
    int ret;
    ret = pci_register_driver(&tct_pci_driver);
    if (ret) return ret;

    // Registra dispositivo de caractere (simplificado: major dinâmico)
    printk(KERN_INFO "[TCT] Driver PCIe carregado. Aguardando hardware CVD.\n");
    return 0;
}

static void __exit tct_exit(void) {
    pci_unregister_driver(&tct_pci_driver);
}

module_init(tct_init);
module_exit(tct_exit);
MODULE_LICENSE("GPL");
