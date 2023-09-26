### Libraries

`PyMYSQL`
`Flask`

### Installation

```
python3 -m pip install PyMySQL
```

```
python3 pip install Flask
```

### Set up MySQL Database

In main folder, change the `config.py` file, the content is

```

MYSQL_HOST = 'yourdbhostname'
MYSQL_USER = 'yourdbusername'
MYSQL_PASSWORD = 'yourdbpassword'
MYSQL_DATABSE = 'grocerydb'

```

### Run application

`flask --app main run`
