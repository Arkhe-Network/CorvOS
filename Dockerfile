FROM rust:1.81-slim-bookworm AS builder
WORKDIR /app
COPY arkhe-daemon /app/arkhe-daemon
COPY arkhe-ebpf /app/arkhe-ebpf
COPY arkhe-ebpf-common /app/arkhe-ebpf-common
COPY Cargo.toml Cargo.lock ./
RUN cargo build --release --bin arkhe-daemon

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y libssl-dev ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/arkhe-daemon /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/arkhe-daemon"]
