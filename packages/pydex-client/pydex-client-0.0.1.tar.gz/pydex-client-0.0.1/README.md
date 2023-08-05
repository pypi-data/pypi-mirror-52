# pydex
Python client for the *Data Exchange Server* REST service provided 
by [ADAMS](https://adams.cms.waikato.ac.nz/).

## Example usage

In the following example, a file is uploaded to the server. 
Then, the data is downloaded from the server using the obtained token.
Lastly, the data is removed from the server using the token again.

```python
from pydex import upload_file, download, remove

# upload a file
token = upload_file("/some/where/file.txt", "http://localhost:8080/upload")
print("token for upload", token)

# download data associated with token
data = download(token, "http://localhost:8080/download")
print("data received for token", token)
print(data.decode())

# remove data from server
code = remove(token, "http://localhost:8080/remove")
print("status code for removing token", token, "is", code)
```

## Authentication

Depending on the DEX backend in use, you might have to provide credentials 
as well in your calls. For instance, when using the `BasicAuthentication`
backend, you can provide user/password in your calls like this:

```python
from pydex import upload_file, download, remove

params = {
    'user': 'someuser',
    'password': 'itspassword'
}

token = upload_file("/some/where/file.txt", "http://localhost:8080/upload", params=params)
print("token for upload", token)
```

## Installation

```commandline
pip install pydex-client
```
