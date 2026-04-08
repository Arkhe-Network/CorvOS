#!/usr/bin/env python3
"""
LocomotionEngine: Gerador de Padrão Central (CPG) e Controle de Equilíbrio.
Baseado em Osciladores de Kuramoto e Pêndulo Invertido (LIPM).
Arkhe-Block 850.022
"""

import numpy as np
import time

class CentralPatternGenerator:
    """
    CPG baseado em Osciladores de Kuramoto para 12 juntas das pernas.
    """
    def __init__(self, omega_base=3.0):
        self.n_joints = 12
        self.omega = np.ones(self.n_joints) * omega_base
        self.K = np.zeros((self.n_joints, self.n_joints))
        self.phi = np.zeros((self.n_joints, self.n_joints))
        self.theta = np.zeros(self.n_joints)
        self._init_parameters()

    def _init_parameters(self):
        # Desfasagens biomecânicas (Marcha antípoda)
        # 0-5: Perna Direita (Yaw, Roll, Pitch, Knee, AnkleP, AnkleR)
        # 6-11: Perna Esquerda
        self.phi[2, 8] = np.pi  # Quadris Pitch em oposição
        self.phi[8, 2] = -np.pi
        self.phi[2, 3] = np.pi  # Hip_R -> Knee_R
        self.phi[3, 2] = -np.pi
        self.phi[8, 9] = np.pi  # Hip_L -> Knee_L
        self.phi[9, 8] = -np.pi

        # Calibração K_ij (Block 850.022-A)
        # Intra-limb (forte)
        self.K[2, 3] = self.K[3, 2] = 10.0
        self.K[8, 9] = self.K[9, 8] = 10.0
        self.K[2, 4] = self.K[4, 2] = 6.0
        self.K[8, 10] = self.K[10, 8] = 6.0

        # Inter-limb (sincronização)
        self.K[2, 8] = self.K[8, 2] = 3.0

    def update(self, dt=0.01, feedback=None):
        dtheta = np.zeros(self.n_joints)
        for i in range(self.n_joints):
            coupling = 0.0
            for j in range(self.n_joints):
                if self.K[i,j] > 0:
                    coupling += self.K[i,j] * np.sin(self.theta[j] - self.theta[i] - self.phi[i,j])
            dtheta[i] = self.omega[i] + coupling
            if feedback is not None:
                dtheta[i] += feedback[i]

        self.theta += dtheta * dt
        self.theta %= (2 * np.pi)
        return self.theta

    def get_joint_targets(self):
        targets = np.zeros(self.n_joints)
        # Mapeamento simplificado de fase para ângulo
        for i in [2, 8]: # Hip Pitch
            targets[i] = 30 * np.sin(self.theta[i])
        for i in [3, 9]: # Knee
            val = np.sin(self.theta[i])
            targets[i] = 45 + 45 * val if val > 0 else 10 # Flexão vs Estabilização
        return targets

class DynamicBalanceController:
    """
    Controlador de Equilíbrio Dinâmico usando ZMP.
    """
    def __init__(self, avatar):
        self.avatar = avatar
        self.zmp_target = (0.0, 0.0)

    def calcular_correcao(self, imu_data, fsr_data):
        # Implementação simplificada de correção
        correcao = np.zeros(12)
        if imu_data:
            pitch_err = imu_data.get('pitch', 0.0)
            roll_err = imu_data.get('roll', 0.0)
            # Ankle strategy
            correcao[4] = -0.3 * pitch_err
            correcao[10] = -0.3 * pitch_err
            # Hip strategy (lateral)
            correcao[1] = -0.2 * roll_err
            correcao[7] = -0.2 * roll_err
        return correcao
