## Akamai NetStorage API for Python
```diff
+ pip install anesto
```


#### Common Variables

`arl` or Akamai Resource Locator, here, is a NetStorage target for an operation; examples are
```
akamai://example-nsu.akamaihd.net/395007/my/path/special.log
akamai://example-nsu.akamaihd.net/395007/my/path/
example-nsu.akamaihd.net/395007/my
example-nsu.akamaihd.net/395007
```
The host name and CP code (here `395007`) are two required elements of the `arl`.
Trailing slash doesn't indicate files inside the target folder, so avoiding it is a cleaner practice.

`key` and `keyname` - a pair you must have for authentication when using NetStorage.


You can start working with NetStorage like so:
```python
import anesto

ns = anesto.Client() # this will have the same effect as :
ns = anesto.Client(retry_number=3, conn_timeout=6, read_timeout=9, url_safe_chars='/~')
```
All functions available by `ns` rely on [Requests module](https://2.python-requests.org/en/master/api/#main-interface) and return [Response object](https://2.python-requests.org/en/master/api/#requests.Response), from where you can get all request-response headers and the status code.

When renaming or removing a target you may wish to treat 404 response as success because when HTTP request is initially delivered but associated response is lost, and the client retries the same request on timeout, the server returns 404 as the job has already been done, and the old target is no longer there. You may change timeout-retry behaviour on `Client()` instance as per above.

`url_safe_chars` is exposed to let you deal with implementations being out of sync, [url-encoding of tilda](https://stackoverflow.com/questions/51334226/python-why-is-now-included-in-the-set-of-reserved-characters-in-urllib-pars) is one example.


#### Available Functions

Any function can be used like so:
```python
key = '<yourAkamaiKey>'
keyname = '<yourAkamaiKeyname>'

ns.download(arl, key, keyname, saveto)
# arl e.g. akamai://example-nsu.akamaihd.net/395007/my/path/special.log
# saveto is an existing folder or a file target, e.g. '~/Downloads'
# files only
```
We further assume that `key` and `keyname` are defined...
```python
ns.upload(arl, key, keyname, file)
# arl e.g. akamai://example-nsu.akamaihd.net/395007/my/path/special.log
# file e.g. `~/Documents/special.log`
# files only
```

```python
ns.delete(arl, key, keyname)
# files and symlinks only
```

```python
print(ns.xdir(arl, key, keyname).text)
# xdir().text returns XML string describing contents of a folder specified by arl
# folders only
```

```python
print(ns.xdu(arl, key, keyname).text)
# xdu().text returns XML string with metadata, such as total number of files and
# disk space taken by a folder specified by arl
# folders only
```

```python
ns.mkdir(arl, key, keyname)
# creates a folder
```

```python
ns.mtime(arl, key, keyname, 988888888) # cannot change folders
# changes modification time stamp to unix epoch specified e.g.
```

```python
ns.quickdelete(arl, key, keyname)
# Recursive folder remover - must be explicitly enabled by Akamai, see rmdir_rec() below
# folders only
```

```python
ns.rename(arl, key, keyname, uri):
# all path folders must exist, moves under same CP code only
# uri e.g. "/395007/mypath/dir-v-test/vtest2"
# uri e.g. "../vtest" (relative to arl)
# files and symlinks only
```

```python
ns.rmdir(arl, key, keyname)
# removes an empty folder
# folders only
```

```python
ns.rmdir_rec(arl, key, keyname)
# removes a folder recursively
# Only recursive function here with many HTTP calls. May crash on stack overflow
# folders only
```

```python
print(ns.stat(arl, key, keyname).text)
# stat().text returns XML string describing metadata of any target specified by arl
# folders, files, symlinks
```

```python
ns.symlink(arl, key, keyname, target)
# creates a symlink specified by arl
# target e.g. "/395007/my/path/dir-v-test/vtest2"
# target e.g. "../vtest/" (relative to arl)
```
Symlinks does not work as such when you access NetStorage, they are followed by Akamai CDN using them as the origin.


-----------
*Packaging*
```
pip install --upgrade setuptools wheel twine
python3 setup.py sdist bdist_wheel
twine upload dist/*
rm -r dist build anesto.egg-info
```
