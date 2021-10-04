# smallsmt-openpnp
OpenPnp driver for SmallSmt machines


This is collection of OpenPnp driver and OpenPnp related scripts for SmallSmt Pick&Place machines.

## Setup
* Install python >v3.6 + pip

```bash
cd source/smallsmt_openpnp_server

# install the dependencies
pip install .
```

## Run (standalone, playground)
```bash
# run the server
python smallsmt_openpnp_server/smallsmt_openpnp_server.py

# select the serial port and connect to the machine
# run the playground from the menu and move the machine around
```

## Run (with openpnp)
* Install java + maven (see here: https://github.com/openpnp/openpnp/wiki/Developers-Guide#building-openpnp)

```bash
git clone https://github.com/jarekkt/openpnp
cd openpnp
mvn package
run ./openpnp.sh or ./openpnp.bat
```
