{
  description = "A flake for Python including uv";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.systems.url = "github:nix-systems/default";
  inputs.flake-utils = {
    url = "github:numtide/flake-utils";
    inputs.systems.follows = "systems";
  };
  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            bashInteractive
            uv
            python3
            gcc
            linuxHeaders
            alsa-lib
            pkg-config
            stdenv.cc.cc.lib
            (python3.withPackages (ps: with ps; [
              tkinter
              evdev
              pycairo
              simpleaudio
            ]))
          ];
          # Explicitly tell setup.py where the header files are stored in Nix
          C_INCLUDE_PATH = "${pkgs.linuxHeaders}/include:${pkgs.alsa-lib}/include";
          PKG_CONFIG_PATH = "${pkgs.alsa-lib}/lib/pkgconfig";
          LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.alsa-lib}/lib";

          shellHook = ''
            echo "Nix build environment loaded with Linux headers!"
          '';
        };
      }
    );
}
