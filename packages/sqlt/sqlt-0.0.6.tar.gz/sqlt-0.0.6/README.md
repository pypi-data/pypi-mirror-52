# sqlt

A simple SQLite3 wrapper in python.

## Example

List all `user`

```py
db.all('user')
```

List all user named `tom`

```py
db.all('user', {'name': 'tom'})
```

Insert a new `user` named `john`

```py
db.insert('user', {'name': 'john', 'age':50})
```

Update any `user` 18 years old if they name are `john`

```py
db.update('user', {'age': 18}, {'name': 'john'})
```

Delete any `user` named tom

```py
db.delete('user', {'name': 'tom'})
```

# Build + Publish package

```sh
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
