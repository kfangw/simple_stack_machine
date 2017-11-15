simple_stack_machine
============

# Prerequisites
## LLVM
* brew install llvm

## llvmlite
* git clone https://github.com/numba/llvmlite.git
* cd llvmlite
* python setup.py build
* python runtests.py
* python setup.py install

## virtualenv
* sudo pip install virtualenvwrapper 
* mkdir ~/.virtualenvs
* vi ~/.bashrc ( paste bellows to the file and save )
```
export WORKON_HOME=~/.python_virtual_envs
source /usr/local/bin/virtualenvwrapper.sh
```
* mkvirtualenv --python=python2.7 {env_name}
* workon {env_name}

## requirements
* pip install pip-tools

# Project

## Build

* git clone https://github.com/kfangw/simple_stack_machine.git
* cd simple_stack_machine
* pip-compile requirements.in
* pip-sync

## Test

* pytest

## Run

* python ./smc.py {source_file} -o {executable_file} -k -d
    * {source_file}: file name to be compiled
    * -o {executable_file}: specify executable file name. it can be ommited.
    * -k: keeps intermediate files such as .ll .s
    * -d: debug option. print stack pointer and value of the stack top
    * -h[--help]: shows this messages

    