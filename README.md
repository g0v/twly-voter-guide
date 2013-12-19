twly_local
==========

Local web application of http://twly.herokuapp.com/

0.1 install pip python easy_install postgresql         
```
sudo apt-get install python-pip python-dev python-setuptools postgresql
easy_install virtualenv
```
0.2 database setting 
```
sudo -u postgres psql -c "ALTER USER postgres with encrypted PASSWORD 'put_your_password_here';"
```
1. start virtualenv and install packages
```
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
```
2. restore database
```
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d ly local_db.dump
```
3. setting.py
./ly/setting.py     
config your setting in DATABASES, SECRET_KEY(don't share with others)       

第一次接觸建議參考https://docs.djangoproject.com/en/dev/intro/tutorial01/					

授權
======
http://twly.herokuapp.com/about/
