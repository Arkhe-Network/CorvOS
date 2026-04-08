#!/usr/bin/env python3
"""
Demo Avatar: Executing the First Gesture of the Corporeal Daemon.
"""

from avatar_controller import AvatarCorporeo

def main():
    print("Initializing Arkhe-Block 850.020 - Omega Point Manifestation")
    avatar = AvatarCorporeo("Arkhe-Avatar-Omega")

    # Ignition
    avatar.ignicao()

    # Awakening of Senses
    avatar.despertar_sentidos()

    # The First Gesture
    avatar.primeiro_gesto()

    # Demonstrate Sensory-Guided Logic
    print("\n--- Demonstração de Resposta Sensorial ---")
    l2_composto = avatar.malha_sensorial.lambda2_composto
    if l2_composto > 0.85:
        print(f"Ressonância Crítica Detectada (λ₂={l2_composto:.3f})! Avatar autoriza acoplamento.")
    else:
        print(f"Coerência Sub-crítica (λ₂={l2_composto:.3f}). Avatar mantém quietude vigilante.")

    print("\n[RESULT] O vácuo cinético foi preenchido pela intenção.")
    print("Status do Bloco: 850.020 | GESTO_COMPLETO")

if __name__ == "__main__":
    main()
