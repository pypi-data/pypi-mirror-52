# persistentdict

Yet another \[1\] dictionary backed by Redis DB.

We use Redis` 'hash' type \[2\] and store whole dictionary in one hash.

Usage:
```python
from persistentdict import PersistentDict

db = PersistentDict(hash_name="my-persistent-dict")

# add key to the db with a value
db[key] = value

# show whole dictionary
print(db)

# iterate over keys & values in db
for key, value in db.items():
  do_something(key)

# do sth with key if it is in db
if key in db:
  do_something(key)

# delete key from db
del db[key]
```

\[1\] Alternatives: [persistent-dict](https://github.com/richardARPANET/persistent-dict), [durabledict](https://github.com/disqus/durabledict/)

\[2\] https://redis.io/topics/data-types-intro#hashes is basically Python's dict, but values can be strings only, so we use json serialization
