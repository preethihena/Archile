# Website for Media Sharing-ARCHILE
This is an Django based website which is developed by my team as part of our project in 5th semester engineering in Indian Institute of Information Technology, SriCity. 


## Requirements

* [Python](https://www.python.org/)   (3.5.2 tested)
* [Django]( https://www.djangoproject.com/)
* [PIL]( https://python-pillow.org/)
* [Mysql]



## Getting Started

To clone and run this application, you'll need Git,Python, Pillow, Mysql installed on your computer. I assume you already setup the Django environment on your machine, if not yet, then follow the below steps. From your command line:

### Create a virtual environment
```
$ virtualenv -p python3 .env
```
### Activate the virtualenv
```
$ source .env/bin/activate
```
### Clone this repository
```
$ git clone https://github.com/krishnadey30/Archile.git
```

### Install the requirements
```
$ pip install -r requirements.txt
```

### Create a Database
Open mysql and create a database-archile
```
$  CREATE DATABASE archile CHARACTER SET UTF8;
```

### Update the settings file
Go to main project folder. 
``` $ cd archile ```
In settings.py file update the database user and password.

### Migrate the databse
```
$ python manage.py makemigrations && python manage.py migrate
```

### Run the app
```
$ python manage.py runserver
```

Note: If those commands is not working, please open issue with detailed error messages.
## Contributers

* [Vishakha](https://github.com/vishakhakhurangale)
* [Preethi Hena](https://github.com/preethihena)
* [Dhruv Meshram](https://github.com/DhruvMeshram)
* [Jahnavi](https://github.com/jahnavi666)
* [Adamya](https://github.com/AdamyaGupta)
