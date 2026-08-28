{
  description = "Fretboard Visualizer";
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
            pyright

            (python3.withPackages (ps: with ps; [
              tkinter
              evdev
              pillow
            ]))
          ];

          shellHook = ''
            echo "$(python3 --version)"
          '';
        };
      }
    );
}
