# Basic dns resolver for Neptune DNS Server
This is a basic dns resolver for neptune dns server
## Installation

You can install from pypi.org or clone this repo
### From PYPI
```
pip3 install neptune_resolver_default
```
### From this repo
```
git clone https://git.best-service.online/yurzs/neptune-default-resolver
cd neptune-default-resolver
python3 setup.py install
```
## How to use
In Neptune config file add 
```
NEPTUNE_RESOLVER_DEFAULT = {
    'resolvers': ['1.1.1.1', '8.8.8.8'] # Your favorite DNS resolvers
}
```
