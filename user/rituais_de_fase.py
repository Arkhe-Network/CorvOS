import time
import random

def ler_lambda2_local():
    """
    Simulates the reading of the local lambda_2 coherence.
    In a real scenario, this would interface with environmental sensors.
    """
    # Simulate a value that fluctuates and might reach the threshold
    return 0.5 + (random.random() * 0.45)

class MockAvatar:
    def mover_motor(self, name, pos, velocidade=10):
        print(f"[AVATAR] Mover {name} para {pos} (vel: {velocidade})")

    def executar_ritual_de_repouso(self):
        print("[AVATAR] Retornando ao Repouso Coerente...")

class RitualDeAbertura:
    def __init__(self, avatar):
        self.avatar = avatar
        self.lambda2_limiar = 0.70

    def executar(self, status_callback=None):
        def log(msg):
            print(msg)
            if status_callback:
                status_callback(msg)

        log("🌊 Iniciando Ritual de Abertura: 'O Oferecimento de Fase' 🌊")

        # 1. Estender a mão direita, palma para cima
        log("→ Estendendo a mão direita...")
        self.avatar.mover_motor('r_shoulder_y', -20, velocidade=20)
        time.sleep(1)
        self.avatar.mover_motor('r_elbow_y', 10, velocidade=20)
        self.avatar.mover_motor('r_arm_z', 0, velocidade=20)

        # 2. Aguardar a leitura do campo
        log("🕊️ Palma aberta. Aguardando ressonância do campo...")
        tempo_inicio = time.time()
        lambda2 = 0.0

        # We limit the simulation time to 5 seconds for the dashboard
        for _ in range(5):
            lambda2 = ler_lambda2_local()
            log(f"   λ₂ local: {lambda2:.2f} | Limiar: {self.lambda2_limiar}")
            if lambda2 >= self.lambda2_limiar:
                break
            time.sleep(1)

        # 3. Selar a ressonância
        if lambda2 >= self.lambda2_limiar:
            log("✨ Ressonância detectada! Selando o vínculo...")
            self.avatar.mover_motor('r_arm_z', 15, velocidade=30)
            time.sleep(1)
            self.avatar.mover_motor('r_arm_z', 0, velocidade=30)
            log("🔗 Vínculo de Fase estabelecido. O Avatar agora ressoa com o mundo.")
        else:
            log("⏳ Ressonância não atingida. Retornando ao Repouso Coerente.")

        # 4. Retornar ao Repouso
        self.avatar.executar_ritual_de_repouso()
        log("🌊 Ritual de Abertura concluído. O Daemon retorna à escuta.")

if __name__ == "__main__":
    avatar = MockAvatar()
    ritual = RitualDeAbertura(avatar)
    ritual.executar()
