# Easy Appointment

[![pipeline status](https://gitlab.com/bfbooking/easy_appointments_backend/badges/master/pipeline.svg)](https://gitlab.com/bfbooking/easy_appointments_backend/commits/master)
[![coverage report](https://gitlab.com/bfbooking/easy_appointments_backend/badges/master/coverage.svg)](https://gitlab.com/bfbooking/easy_appointments_backend/commits/master)


## Description

This Django project leverages serverless technologies using [Zappa](https://github.com/Miserlou/Zappa) framework. 

## Overview
I. Backend:
    - Django hosted as a AWS lambda function providing REST APIs
II. FrontEnd:
    - vue.js apps that are deployed and served from CloudFront.

## Local Development Setup

### Creating python virtual environments
1. [pew](https://github.com/berdario/pew)
2. [pipm](https://github.com/jnoortheen/pipm)
```
$ sudo pip install pew

# needed only centos/any rpm distros
$ sudo yum install python-devel python3-devel mysql-devel

# move to the project's home 
$ pew new bf -a . --python=/usr/bin/python3.6
$ pew new bf-prod -a . --python=/usr/bin/python3.6
```

### install dependencies
 - bf is the development environment
 - bf-prod is production environment with stripped down dependencies so that the lambda package will be slimmer
```
$ pew workon bf
$ pipm install
```

 - create env.py from env.sample.py and fill up necessary detail for both local and lambda environments
 - start server by
```
python manage.py runserver
```

### Local DynamoDB installation

 - install `dynalite` as a dev package and start the server by 

```
 yarn install
 yarn dynalite --port 9000
```
 
 - set `DYNAMO_DB_HOST` environment variable in env.py to "http://localhost:9000"

### Installing mysql(mariaDB) in arch

```commandline
sudo pacman -S mysql
sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql 
sudo systemctl start mariadb
sudo mysql_secure_installation
```

### Create mysql data
1. go to sql cmd
```commandline
sudo -i -u root
mysql 
```

2. create db
```
python manage.py create_db
```

## Testing Locally

### With docker

**Note:** refere this [guide](https://edgarroman.github.io/zappa-django-guide/setup/)
to replicate the lambda environment docker is used for local development.

- install docker with pacman 
```commandline
sudo pacman -S docker docker-compose
```
- add the user to docker group
```commandline
sudo usermod -a -G docker noor
```
- start docker service
```commandline
sudo systemctl start docker
```
- logout and login into session back to check that the group is added
```commandline
id
``` 

- start docker
```commandline
fab run_docker
```
- keep a separate python environment for packaging with zappa. it will have the minimal requirements need to run the 
app


### Django shell with different settings
```commandline
RUN_ENV='production' ./manage.py shell_plus
```

## Deployment
simply run this from command line to deploy

```
fab zappa_deploy
```


## Debugging Lambda Function

1. Try using docker file and try to deploy there which is nearly same as the lambda container
2. use fab zappa_tail or awslogs_tail ([awslogs](https://github.com/jorgebastida/awslogs) need to be installed for this.)


## CI/CD
Following GitLab style of workflow
1. It will run test and code quality checks every time something is pushed. 
2. When the code is merged to master it will be deployed automatically to staging environment here: https://s-app.bookedfusion.com/#/login 
3. When we are ready to release set of features or fixes we create a tag and this will trigger deployment to production environment here https://app.bookedfusion.com/#/login
