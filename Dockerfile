FROM ubuntu:24.04 AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    linux-headers-generic \
    curl \
    git \
    pkg-config \
    libssl-dev \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /build
COPY drivers/tct_driver.c drivers/Makefile-tct ./
RUN make -f Makefile-tct || echo "Kernel module build failed (expected in CI)"

COPY arkhe-sync/arkhe-daemon/ ./arkhe-daemon/
WORKDIR /build/arkhe-daemon
RUN cargo build --release

FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    kmod \
    python3 \
    python3-pip \
    netcat-openbsd \
    jq \
    socat \
    redis-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages requests redis websockets aiohttp

RUN mkdir -p /opt/covm/
COPY --from=builder /build/tct_driver.ko /opt/covm/ || echo "Driver not found"
COPY --from=builder /build/arkhe-daemon/target/release/covm-daemon /usr/local/bin/
COPY scripts/tct_twin_server.py /usr/local/bin/
COPY user/cobit-cli.py /usr/local/bin/cobit-cli
COPY scripts/tct_activate.sh /usr/local/bin/
COPY user/sensorium/ /opt/cathedral/sensorium/
RUN chmod +x /usr/local/bin/cobit-cli /usr/local/bin/tct_activate.sh /usr/local/bin/tct_twin_server.py /opt/cathedral/sensorium/*.py /opt/cathedral/sensorium/collectors/*.py

EXPOSE 42000
VOLUME /var/run
VOLUME /var/log/akasha

CMD ["/usr/local/bin/tct_activate.sh"]
