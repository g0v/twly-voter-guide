twly-voter-guide
================

立委投票指南 http://twly.herokuapp.com/     

In Ubuntu
=================
0.1 install git python pip easy_install postgresql
```
sudo apt-get install git python-pip python-dev python-setuptools postgresql
easy_install virtualenv
```

0.2 set a password in your database(If you already have one, just skip this step) 
```
whoami
```

(you can use `whoami` to check your username, notice <username> below, please replace with your own username)

```
sudo -u <username> psql -c "ALTER USER <username> with encrypted PASSWORD 'put_your_password_here';"
```

1. git clone
```
git clone https://github.com/g0v/twly-voter-guide.git       
cd twly-voter-guide
```

2. start virtualenv and install packages        
choice A: if you don' mind packages installed into your local environment:        

```
pip install -r requirements.txt     
```

choice B: if you want to separate the environment:        

```
virtualenv --no-site-packages venv      
source venv/bin/activate        
pip install -r requirements.txt     
```

3. restore data into database       
Please new a database, ex: ly, below will use ly for example
```
createdb -h localhost -U <username> ly
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U <username> -d ly local_db.dump
```

4. setting.py  
create `twly-voter-guide/ly/local_settings.py`, for example:

```
touch ./ly/local_settings.py
```

config your database parameter(notice USER, PASSWORD below), and input SECRET_KEY              
Django tutorial: https://docs.djangoproject.com/en/dev/intro/tutorial01/        
or maybe use http://www.miniwebtool.com/django-secret-key-generator/ to generate SECRET_KEY for convenience				

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ly', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}
SECRET_KEY = '' # <- put random string inside and don't share it with anybody.
```

5. runserver
```
python manage.py runserver
```


For MAC
=================
0.1 install postgresql (use brew)
```
$ brew install postgresql
```
0.2 install pip
```
$ sudo install pip 
```


1. git clone
```
git clone https://github.com/g0v/twly-voter-guide.git       
cd twly-voter-guide
```
2. install dependent module
```
$ sudo pip install -r requirement.txt
```
(or use virtualenv)

3. create db (eg. ly)
```
$ createdb ly
```

4. restore data into database       
Please new a database, ex: ly, below will use ly for example
```
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U <username> -d ly local_db.dump
```
you can use `$ whoami` to check your username

5. runserver
```
$ python manage.py runserver
```

CC0 1.0 Universal
=================
CC0 1.0 Universal       
This work is published from Taiwan.     
http://twly.herokuapp.com/about/
