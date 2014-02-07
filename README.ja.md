# 日本語インストールドキュメント
インストールを行うには、以下の手順を実施してください。

## まっさらな Ubunt 12.04 LTS でinstall開始
VirtualboxにUbuntu 12.04 LTSをインストールします。ここは各個人よろしくお願いします。
基本パッケージのupgrade & 一度reboot を行ってください。

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo reboot
```

## pythonで利用するパッケージをインストール

```
$ sudo apt-get install libmysqld-dev git gcc g++ make libssl-dev libsqlite3-dev libghc-zlib-dev libreadline-dev libldap2-dev libzip-dev libbz2-dev sshpass libncurses5-dev postgresql postgresql-server-dev-9.1
```

## pyenvの設定実施
```
$ cd ~/
$ git clone git://github.com/yyuu/pyenv.git .pyenv
$ cd ~/.pyenv/plugins
$ git clone git://github.com/yyuu/pyenv-virtualenv.git
$ echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.profile
$ echo 'eval "$(pyenv init -)"' >> ~/.profile
$ source ~/.bashrc
$ source ~/.profile
$ pyenv install 2.7.6
```

## pyenvにて本システム用のvirtualenvを作成
```
$ pyenv virtualenv 2.7.6 voter
```

## 本システムを動作させる場所を作成
```
$ mkdir -p ~/voter_system
$ cd ~/voter_system/
```

## 上記で作成したディレクトリに対してvirtualenv環境を設定
```
$ pyenv local 2.7.6
```

## 本システムをclone
```
$ git clone https://github.com/g0v/twly-voter-guide.git
```

## postgres 設定 & DB作成 + 流し込み
```
$ sudo /etc/init.d/postgresql start
$ sudo -u postgres psql -c "ALTER USER postgres with encrypted PASSWORD 'testtest';"
$ sudo su - 
# sudo su - postgres
$ cd /home/testuser/voter_system/twly-voter-guide/
$ createdb ly
$ pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d ly local_db.dump
$ exit # postgresユーザーのshellをexit
# exit # rootユーザーのshellをexit
```

## 本システムが利用するpythonパッケージをinstall
```
$ cd ~/voter_system/twly-voter-guide/
$ pip install -r ./requirements.txt
```

## local_settings.pyの設定
ブラウザで[Django Secret Key Generator](http://www.miniwebtool.com/django-secret-key-generator/)を開いてgenerate_keyを生成します。

```
$ vim /home/testuser/voter_system/twly-voter-guide/ly/local_settings.py 
```

SecretKeyの値は適当なものを指定しています。[Django Secret Key Generator](http://www.miniwebtool.com/django-secret-key-generator/)で生成したキーを入力してください。

```
SECRET_KEY = "WRITE_YOUR_DJANGO_SECRET_KEY_HERE"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ly', #DB名
        'USER': 'postgres', #DBのユーザー名。ここではpostgres
        'PASSWORD': 'testtest', #DBのパスワード
        'HOST': 'localhost', #DBホスト名
        'PORT': '', #DBポート
    }
}
```


## 本システムの起動
```
$ chmod 700 ./manage.py
$ ./manage.py runserver 0.0.0.0:8000
```

あとはブラウザーでアクセスしてください！
