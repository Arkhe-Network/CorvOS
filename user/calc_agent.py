#!/usr/bin/env python3
"""
CalcAgent: A Shachi-inspired Arkhe Agent specialized in phase-coherent arithmetic.
This agent monitors the 'arkhe_calc' operations and ensures high coherence for precise results.
"""

import sys
from arkhe_shachi import ArkheAgent, ArkheTool

def main():
    print("--- CalcAgent: Coherence Supervisor Initializing ---")

    config = {
        'genetic_bias': 0.15,
        'initial_lambda': 0.99
    }

    agent = ArkheAgent(agent_id="CalcAgent-01", config=config)

    # Define a tool for the agent: Trigger Phase Recovery
    def recover_phase(**kwargs):
        print(f"CalcAgent-01: [TOOL] Executing PHASE_RECOVERY for λ₂={kwargs.get('lambda_val')}")
        return "RECOVERY_COMPLETE"

    agent.add_tool(ArkheTool("PhaseRecovery", "Restores local phase coherence", recover_phase))

    # Simulate a step
    observation = {
        'summary': 'Arkhe-Calc request received.',
        'lambda_global': 0.96
    }

    decision = agent.step(observation)
    print(f"CalcAgent-01: Decision -> {decision['action']} ({decision['detail']})")

    if decision['action'] == "OPTIMIZE_LOCAL":
        agent.tools["PhaseRecovery"].call(lambda_val=decision['local_lambda'])

    print("--- CalcAgent: Supervision Cycle Complete ---")

if __name__ == "__main__":
    main()
