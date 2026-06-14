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
            (python3.withPackages (ps: with ps; [
              tkinter
              evdev
              pycairo
            ]))
          ];
          # Explicitly tell setup.py where the header files are stored in Nix
          C_INCLUDE_PATH = "${pkgs.linuxHeaders}/include";

          shellHook = ''
            echo "Nix build environment loaded with Linux headers!"
          '';
        };
      }
    );
}
