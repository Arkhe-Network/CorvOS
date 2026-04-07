#ifndef PHI_PCIE_H
#define PHI_PCIE_H

#include <stdint.h>

void phi_pcie_init();
void phi_pcie_send(uint8_t data);
uint8_t phi_pcie_receive();

#endif
