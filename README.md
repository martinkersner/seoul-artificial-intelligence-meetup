[seoulai.com](http://seoulai.com/)

# automation script

```
$ python publish.py -h
usage: publish.py [-h] <command>

positional arguments:
  <command>   automation command (test, fire, photo)

optional arguments:
  -h, --help  show this help message and exit
```

First, make sure event information is correct.

```
$ python publish.py test
```

Second, publish event to other sns.

```
$ python publish.py fire
```
