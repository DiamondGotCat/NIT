# Next-in-the Installer
"Next-in-the (NIT)" Installer is Simple Package Manager for Python.

## HTI
NIT using [HTI Package Index](https://github.com/DiamondGotCat/HTI).

## Operating environment

### macOS
Tested macOS: 14.4.1
Tested Python: 3.10.6
Tested PIP: 22.2.1

### Linux
Not tested, but should work.

## How to start NIT?

### Runner (macOS/Linux)
Using the runner will automate all installation steps and launch the program automatically.
```bash
/bin/bash -c "$(curl -fsSL https://diamondgotcat.github.io/NIT/install.sh)"
```

### Python File
Download nit.py from [Releases](https://github.com/DiamondGotCat/NIT/releases)

## How to Add Package to Official Index?
If you need Add Package to Official Index, Please Create Issues or Pull requests on the HTI Repository.

## How to Install HTI Package?
```
python3 nit.py install <package_name>
```
or
```
python3 nit.py install <package_name> <version>
```
or
```
python3 nit.py install <package_name> <version> <package_name> <version> ...
```
or
```
python3 nit.py install <package_name> <package_name> <package_name> ...
```
