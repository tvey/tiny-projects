# Simply Todo List on Flask

## Creating a db

```python
from stl import db, create_app

db.create_all(app=create_app())
```

## Running the app

```bash
export FLASK_APP=stl
export FLASK_DEBUG=1
flask run
```

## Todo

- [ ] Replace basic HTML forms with FlaskForm objects

- [ ] Maybe make items sortable
