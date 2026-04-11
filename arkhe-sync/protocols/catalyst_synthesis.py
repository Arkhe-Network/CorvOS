from opentrons import protocol_api

metadata = {
    'protocolName': 'Multi-elemental Catalyst Synthesis',
    'author': 'Arkhe-Lab',
    'description': 'Synthesize catalyst libraries from molar fractions',
    'apiLevel': '2.15'
}

def run(protocol: protocol_api.ProtocolContext):
    # composition = {{COMPOSITION}}
    composition = {"Fe": 0.2, "Co": 0.3, "Ni": 0.2, "Pd": 0.15, "Pt": 0.15}
    protocol.comment(f"Starting synthesis for: {composition}")
    # Logic to transfer stock solutions based on composition
