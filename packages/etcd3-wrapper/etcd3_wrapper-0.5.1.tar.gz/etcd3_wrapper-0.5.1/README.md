# etcd3_wrapper
A thin wrapper around Python module [etcd3](https://pypi.org/project/etcd3/) to make it a little easier to deal with etcd.

**Warning: The API isn't fully stable and can changed significantly in future.**

For Example, you want to get an entry from etcd.
You would write something like this

```python
from etcd3_wrapper import Etcd3Wrapper

client = Etcd3Wrapper()
entry = client.get("/planet/earth")

if entry:
    # It would print key and value of entry
    # in bytes format b'....'
    print(entry.key, entry.value)

```

Output

```
b'/planet/earth' b'{"population": "7.53 Billion"}'
```

```python
# If you know that the value in etcd is in JSON
# format. You can do the following

json_entry = client.get("/planet/earth", value_in_json=True)

if json_entry:
    # Now, entry.value is of type dict
    print(entry.key, entry.value)

    # So, you can do this too
    print(f"Earth population is {entry.value['population']}")

```

Output

```
/planet/earth {"population": "7.53 Billion"}
Earth population is 7.53 Billion
```