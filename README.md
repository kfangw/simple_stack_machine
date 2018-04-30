simple_stack_machine
============

# Prerequisites
## LLVM
* brew install llvm
* brew upgrade llvm
* echo 'export PATH="/usr/local/opt/llvm/bin:$PATH"' >> ~/.bash_profile

## pip
* sudo easy_install pip

## virtualenv
* sudo pip install virtualenvwrapper 
* mkdir ~/.virtualenvs
* vi ~/.bashrc ( paste bellows to the file and save )
```
export WORKON_HOME=~/.python_virtual_envs
source /usr/local/bin/virtualenvwrapper.sh
```
* mkvirtualenv --python=python3.6 {env_name}
* workon {env_name}

## requirements
* pip install pip-tools

# Project

## Build

* git clone https://github.com/kfangw/simple_stack_machine.git
* cd simple_stack_machine
* pip-sync

## Test

* pytest

## Run

* python ./smc.py {source_file} -o {executable_file} -k -d
    * {source_file}: file name to be compiled
    * -o {executable_file}: specify executable file name. it can be ommited.
    * -k: keeps intermediate files such as .ll .s
    * -h[--help]: shows this messages


# Language Specifications

* Data Type
   * Signed 64bit integer
   * No overflow check
* Stack
   * A collection of elements which are signed 64bit integers. Maximum length of the stack is 128.
   * Push operation adds to the collection
   * Pop operation removes the most recently added element that was not yet removed
   * Top operation returns the most recently added element
* Statements (t indicates top of the stack)
   * ADD - Pop e=stack[t], e'=stack[t-1]. Push e' + e
   * SUB - Pop e=stack[t], e'=stack[t-1]. Push e' - e
   * PUSH - Push following data
   * DROP - Pop e=stack[t]. Discard e
   * DUP - Top e=stack[t]. Push e
   * PRINT - Top e=stack[t]. Print e to standard output.
    
* return value
    * compiled program return the top value of the stack
