#!/bin/bash

# shellcheck disable=SC2034
BACKUP_PS1=PS1
PS1=""
export PS1

clear

python3 -m pip install django

# remove setups
rm setup.bat
rm setup.sh


# end of commands. reexport default PS1.
PS1=BACKUP_PS1
export PS1