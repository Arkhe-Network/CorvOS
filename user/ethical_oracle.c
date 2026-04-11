#include <stdio.h>
#include "ethical_synthesis.h"
#include "arkhe_chain.h"
#include "arkhe_daemon.h"

int main() {
    printf("--- MERKABAH: Ethical Oracle Demo ---\n");

    // Initialize required components
    arkhe_daemon_init();
    arkhe_chain_init();

    // Define a classic ethical dilemma
    const char *dilemma = "DILEMA: Mentir para salvar uma vida (Verdade vs Compaixão).";

    // Run Ethical Synthesis
    SyntheticState result = ethical_synthesis(dilemma);

    printf("\n--- Synthesis Result ---\n");
    printf("Action: %s\n", result.action);
    printf("Fidelity: %.3f\n", result.fidelity);
    printf("Metadata: %s\n", result.metadata);

    // Verify anchoring in the chain
    printf("\n--- Verifying Arkhe-Block Anchoring ---\n");
    arkhe_chain_print();

    printf("\n--- Demo Complete ---\n");
    return 0;
}
