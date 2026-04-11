# configuration.nix - hardening para Arkhe-OS
{
  security.landlock.enable = true;

  services.arkhe-agent = {
    enable = true;
    ebpfPrograms = [
      {
        name = "telemetry_collector";
        type = "tracepoint";
        sandbox = "strict";  # Sem acesso ao host filesystem
        allowedCalls = ["map_lookup" "perf_event_output"];  # Whitelist de syscalls eBPF
      }
    ];

    # Rebuild automático via ZK-proof failure
    autoRebuild = {
      enable = true;
      trigger = "zk-verification-failed";
      rollbackConfig = "nixos-rebuild switch --rollback";
    };
  };
}
