# password_manager

## Setup:
[Clone repo]
```bash
git clone https://github.com/Traceur27/password_manager.git
```

[Prepare virtual environment]
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

[Before running server for the first time]
```bash
./manage.py migrate
./manage.py loaddata fixtures/admin.json
```

[Starting server]
```bash
./manage.py runserver
```

## Using admin tools
Got to:
```bash
http://localhost:8000/admin
```
Username: admin  
Password: admin123
