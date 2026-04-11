{
  description = "Arkhe-Sync: O Hipergrafo da Atlântica";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    nixosConfigurations.arkhe-os = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ({ pkgs, lib, config, ... }: {
          imports = [
            "${nixpkgs}/nixos/modules/installer/cd-dvd/installation-cd-minimal.nix"
          ];

          security.landlock.enable = true;

          options.arkhe-sync = {
            enableERAB = lib.mkOption {
              type = lib.types.bool;
              default = true;
              description = "Ativar ponte de Einstein-Rosen-Arkhe";
            };
            erabStrength = lib.mkOption {
              type = lib.types.float;
              default = 0.95;
            };
            libp2p = {
              enable = lib.mkOption { type = lib.types.bool; default = true; };
              bootstrapNodes = lib.mkOption {
                type = lib.types.listOf lib.types.str;
                default = [ "/ip4/198.51.100.1/tcp/9000" "/ip4/198.51.100.2/udp/9000/quic" ];
              };
            };
          };

          config = {
            environment.systemPackages = with pkgs; [
              xorriso isolinux qemu rustc cargo python311 python311Packages.numpy python311Packages.rich
            ];

            networking.firewall.allowedTCPPorts = [ 9000 ];
            networking.firewall.allowedUDPPorts = [ 9000 1337 ];

            systemd.services.arkhe-daemon = {
              enable = true;
              description = "Arkhe-Sync Daemon v1.5-libp2p";
              serviceConfig.Environment = [
                "ARKHE_ERAB_ACTIVE=1"
                "ARKHE_ERAB_STRENGTH=${builtins.toString config.arkhe-sync.erabStrength}"
                "ARKHE_BOOTSTRAP_NODES=${builtins.concatStringsSep "," config.arkhe-sync.libp2p.bootstrapNodes}"
              ];
            };
          };
        })
      ];
    };
  };
}
