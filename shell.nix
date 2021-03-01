let
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs { config.allowUnfree = true; };
in pkgs.mkShell {
  buildInputs = with pkgs; [
    niv
    sublime3
  ];
}
