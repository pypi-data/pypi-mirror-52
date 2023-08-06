from setuptools import setup, find_packages

setup(
    name='neptune_resolver_default',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),  # Chose the same as "name"
    version='2019.09.17.1721',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    long_description='''# Basic dns resolver for Neptune DNS Server
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
''',
    long_description_content_type='text/markdown',
    description='DNS Resolver for Neptune DNS server',  # Give a short description about your library
    author='Yury (Yurzs)',  # Type in your name
    author_email='dev@best-service.online',  # Type in your E-Mail
    url='https://git.best-service.online/yurzs/triton',  # Provide either the link to your github or to your website
    keywords=['neptune', 'DNS', 'resolver'],  # Keywords that define your package best
    install_requires=['triton-dns-client'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
    ],
)