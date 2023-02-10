Library app
========

A django rest apis for Library application


Setup Virtual Environment
-------------------

This service is using Python 3.10.7 

#### macOS

View the available Python versions:
```
pyenv install -l
```

If version 3.8.0 is not in the available list:
```
pyenv install 3.10.7
```

Create the virtualenv:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows

Create virtualenv:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Running the Application
-----
Before running the application we need to create the needed DB tables. so activate your virtual environment and run the commands:
```
python manage.py makemigrations
python manage.py migrate
 ```

Now run the server
```
python manage.py runserver
```

create superuser
```commandline
python manage.py createsuperuser
```

To access the applications, go to the URL http://localhost:8000/v1

This will show an overview page that consist of a list of url related to curd_api

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "books": "http://127.0.0.1:8000/v1/books",
    "author": "http://127.0.0.1:8000/v1/author"
}
```

Tests
-----

To run tests, activate your virtual environment and run:
```commandline
python manage.py test
```