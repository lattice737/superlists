Provisioning a new site
=======================

## Required packages

* nginx
* Python 3.6
* virtualenv + pip
* Git

e.g., on Ubuntu:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python36 python3.6-venv

## Nginx virtual host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.domain.com
* remote location /etc/systemd/system/gunicorn-SITENAME.service

## Folder structure

Assume user account is available at /home/username

/home/username
|__ sites
    |__ SITENAME
        |__ database
        |__ source
        |__ static
        |__ virtualenv
