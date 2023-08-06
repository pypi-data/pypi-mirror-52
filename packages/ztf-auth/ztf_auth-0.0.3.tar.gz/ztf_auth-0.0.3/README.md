# ZTF_Auth
## Setup for handling ZTF authentication

In order to use this, we keep a json file with the credentials in a directory on the client computer in a `ztfdir` directory. `ztfdir` is `${HOME}/.ztf`, but this can be changed. 

## Installation
```
python setup.py install
``` 
### Example code
```
# After setting up a JSON file eg. at `${HOME}/.ztf/ztffps_auth.json`: 
# {"username": "myusername", "password": "mypasswd!",  "email": "my_email@myprovider"}

from ztf_auth import get_ztf_auth

auth_dict = get_ztf_auth()
```






