# introduction

Django database reconnect

# install

```sh
pip install django_mysql_reconnect
```

# Usage 
Note that only pymysql is supported. To enable Django to use pymysql, you need to install the package first and add the following code to _init_.py in the directory where settings.py resides

import pymysql
pymysql.install_as_MySQLdb()

add`django_mysql_reconnect` to settings.py INSTALLED_APPS
```python
INSTALLED_APPS = (
    # ...
    'django_mysql_reconnect',
)
```
