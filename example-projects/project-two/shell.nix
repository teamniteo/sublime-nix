let
  sources = import ../../nix/sources.nix;
  pkgs = import sources.nixpkgs {};
  customPackage = pkgs.writeShellScriptBin "custom" ''
    echo "In project two"
  '';
in pkgs.mkShell {
  buildInputs = with pkgs; [
    customPackage
  ];
}

