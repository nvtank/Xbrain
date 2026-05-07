with import <nixpkgs> {};

mkShell {

  buildInputs = [

    python311

    python311Packages.pip

    python311Packages.virtualenv

    awscli2

    gcc

    stdenv.cc.cc.lib
  ];

  LD_LIBRARY_PATH = lib.makeLibraryPath [
    stdenv.cc.cc.lib
  ];
}
