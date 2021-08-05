#!/bin/bash

# shellcheck disable=SC2034
BACKUP_PS1=PS1
PS1=""
export PS1

clear

# django requirement
python3 -m pip install django

# alternative packages
python3 -m pip install phonenumbers
python3 -m pip install django-phonenumber-field
# rest framework
python3 -m pip install djangorestframework

# remove setups
rm setup.bat
rm setup.sh


# end of commands. reexport default PS1.
PS1=BACKUP_PS1
export PS1