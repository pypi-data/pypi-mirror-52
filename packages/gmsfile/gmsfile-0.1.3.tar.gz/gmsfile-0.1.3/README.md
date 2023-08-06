## XYZ to GAMESS file converter
This is a simple package You can use it by calling

>   from gmsfile import gms

>   mol=gms("mol.xyz")

>   mol.runtyp("opt")

>   mol.writefile("mol.inp")


This will convert your xyz file to a gamess input file that you can run
in GAMESS for optimization of a molecule.
