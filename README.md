
## Installation before run this App

make sure you have installed these package.

Check python3 version, if you don't have python3 install by using command
```bash
  sudo apt install python3.8
```
Make sure you have installed pip library, check pip version by typing 
```bashsudo apt install python3-django
  pip --version
```
If you don't have pip library then install by using this command.
```bash
  sudo apt install python3-pip
```
Django Installation in your machine.
```bash
  sudo apt install python3-django
```
Installing virtualenv.sudo apt install python3-django
```bash
  python3 -m pip install --user virtualenv
```
Creating a virtual environment.
```bash
  python3 -m venv env
```
Activate your venv by using command.
```bash
  source venv/bin/activate
```
Now, you should install all the django packages in the venv.

Make a clone of your Django repo by using command.
```bash
  Git clone https://github.com/Rizwanul786/jiraPipeline.git
```
Type this commands make sure your venv should be activate.

```bash
  cd jiraPipeline/Xsystem/Xsystem
```

Now, install requirements.txt by typing this command.

```bash
  pip install -r requirements.txt
```
After Installation go to settings.py file and change DATABASES settings.

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB-name',
        'USER':'user_name',
        'PASSWORD':'your_sql_password',
        'HOST': '127.0.0.1'
    }
}

Run these command on command prompt make sure venv should be Activate and path should be jiraPipeline/Xsystem/Xsystem.

```bash
  python manage.py makemigrations
  python manage.py migrate
```

After that you can run for start server.
```bash
 python manage.py runserver
```