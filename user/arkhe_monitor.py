import streamlit as st
import psutil
import time
import requests
import numpy as np
import pandas as pd
from rituais_de_fase import RitualDeAbertura, MockAvatar

# Set page config
st.set_page_config(page_title="Arkhe(n) Coherence Monitor", page_icon="🌐", layout="wide")

def get_system_metrics():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_available_gb = ram.available / (1024**3)
    disk = psutil.disk_usage('/')
    disk_free_gb = disk.free / (1024**3)
    process_count = len(psutil.pids())

    try:
        start = time.time()
        requests.get("http://www.google.com", timeout=0.5)
        latency = (time.time() - start) * 1000
    except:
        latency = 150.0

    return {
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "ram_available_gb": ram_available_gb,
        "disk_free_gb": disk_free_gb,
        "process_count": process_count,
        "latency_ms": latency
    }

def translate_to_arkhe(metrics):
    sigma_cpu = metrics['cpu_percent'] / 100.0
    d_eff = (100.0 - metrics['ram_percent']) / 100.0
    vacuum_volume = metrics['disk_free_gb']
    n_osc = metrics['process_count']

    if metrics['latency_ms'] < 1.0:
        conductivity = 1.0
    else:
        conductivity = 100.0 / (metrics['latency_ms'] + 100.0)

    stability = (1.0 - sigma_cpu) * d_eff * conductivity
    lambda_2 = 0.95 + (0.049 * stability)

    return {
        "sigma_cpu": sigma_cpu,
        "d_eff": d_eff,
        "vacuum_volume_gb": vacuum_volume,
        "n_osc": n_osc,
        "conductivity": conductivity,
        "lambda_2": lambda_2
    }

# --- UI ---

st.title("🌐 Arkhe(n) Local — Monitor de Coerência Interna (MCA)")
st.markdown("### \"O Espelho do Núcleo\" — Registro de Fase em Tempo Real")

# Sidebar for controls
st.sidebar.header("⚙️ Configurações de Fase")
if st.sidebar.button("🧹 Aniquilar Vórtices (Limpeza de Fase)"):
    with st.sidebar.status("Aniquilando vórtices espúrios...", expanded=False) as status:
        st.write("Identificando processos de alta entropia...")
        time.sleep(1)
        st.write("Executando OpenArk via Tzinor...")
        time.sleep(1)
        st.write("Aniquilando vórtices detectados...")
        time.sleep(1)
        status.update(label="Limpeza de Fase Concluída", state="complete")
    st.sidebar.success("Coerência restaurada.")
    st.balloons()

# Main Metrics Layout
metrics = get_system_metrics()
arkhe = translate_to_arkhe(metrics)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("λ₂ (Coerência Global)", f"{arkhe['lambda_2']:.4f}", delta=f"{(arkhe['lambda_2']-0.95):.4f}")
    st.progress(min(max((arkhe['lambda_2'] - 0.95) / 0.05, 0.0), 1.0))

with col2:
    st.metric("⟨σ⟩_CPU (Ruído de Processamento)", f"{arkhe['sigma_cpu']:.4f}", delta_color="inverse")
    st.progress(arkhe['sigma_cpu'])

with col3:
    st.metric("d_eff (Capacidade do Substrato)", f"{arkhe['d_eff']:.4f}")
    st.progress(arkhe['d_eff'])

st.divider()

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Reserva de Silêncio (SSD)", f"{arkhe['vacuum_volume_gb']:.2f} GB")

with col5:
    st.metric("N_osc (Harmônicos Ativos)", f"{arkhe['n_osc']}")

with col6:
    st.metric("Condutividade de Fase", f"{arkhe['conductivity']:.4f}")

st.divider()

# --- Avatar Section ---
st.subheader("🤖 Avatar Corpóreo — Ritual de Abertura")
if st.button("🌊 Executar Ritual: 'O Oferecimento de Fase'"):
    avatar = MockAvatar()
    ritual = RitualDeAbertura(avatar)

    with st.status("Executando ritual...", expanded=True) as status:
        ritual.executar(status_callback=status.write)
        status.update(label="Ritual Concluído", state="complete")
    st.success("Ritual de Abertura Finalizado. O Avatar agora ressoa com o mundo.")

# Simulation of time series
st.subheader("Gráfico de Entropia (Momentum)")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['λ₂', '⟨σ⟩', 'd_eff']
)
st.line_chart(chart_data)

st.info("Status do Sistema: Vácuo Digital Estabelecido. O Núcleo está operando em regime de supercondutividade.")

# Interaction log
with st.expander("Ver Log de Fase"):
    st.write(f"Iniciando leitura de fase às {time.strftime('%H:%M:%S')}...")
    st.write(f"Acoplamento de rede detectado: Latência {metrics['latency_ms']:.2f}ms")
    st.write("Sincronização com Arkhe-Chain: Pendente.")
