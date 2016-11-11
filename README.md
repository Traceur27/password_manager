# password_manager

## Setup:
###Clone repo
```bash
git clone https://github.com/Traceur27/password_manager.git
```

###Prepare virtual environment
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

###Install C++ module
Beafore building C++ module you must install
[Boost Python](http://www.boost.org/libs/python/doc/)
module for your system.

Enter virtualenv and type:
```bash
cd cryptopp-python-binding
python setup.py install
```
in python files write
```python
import cryptopp
```
to start using module

###Before running server for the first time
```bash
./manage.py makemigrations
./manage.py migrate
./manage.py loaddata fixtures/admin.json
```

###Starting server
```bash
./manage.py runserver
```

## PyCharm setup
```bash
Run -> Edit Configurations -> press "+" sign -> red mark "Fix"
check "Enable Django Support" -> set project root: password_manager/zpr
set paths for settings.py and manage.py -> Apply
```

## Using admin tools
Got to:
```bash
http://localhost:8000/admin
```

Username: admin

Password: admin123
