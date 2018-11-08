# Instructions to install(in Ubuntu 16.04 and Python 3.5):

## Installing Mysql
```
sudo apt-get update
sudo apt-get install mysql-server
```
You'll be prompted to create a root password during the installation. Choose a secure one and make sure you remember it, because you'll need it later. 

`mysql -u root -p`


## Intalling Virtual environment:
Pip will automatically get installed

```
sudo python3 dependencies/pip-18.1-py2.py3-none-any.whl/pip install dependencies/virtualenv-16.1.0-py2.py3-none-any.whl
```
## Starting the virtualenv

`virtualenv .env --python=python3`	
`source .env/bin/activate`

### For rest all dependencies:
```
pip install dependencies/*
```

If error comes and shows mysql-client is having some problem
```
sudo apt-get install libmysqlclient-dev python3-dev
sudo apt-get install libmysqlclient-dev python3-dev --fix-missing (if required)
```

