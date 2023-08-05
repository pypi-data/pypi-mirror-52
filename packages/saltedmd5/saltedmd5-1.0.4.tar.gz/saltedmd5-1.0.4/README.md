
<p align="center"><img width=77% alt="" src="https://github.com/nat236919/saltedmd5/blob/master/docs/img/saltedmd5_logo_resized.png?raw=true"></p>

<p align="center">
<a href="https://pypi.org/project/saltedmd5/"><img alt="" src="https://img.shields.io/badge/pypi-1.0.3-blue.svg"></a>
<a href="https://github.com/nat236919/saltedmd5/blob/master/LICENSE"><img alt="" src="https://img.shields.io/pypi/l/saltedmd5"></a>
</p>

<p align="center"><b>To use Salted MD5:</b></p>

```python
from saltedmd5 import Salting
```

```python
# user = Salting(<password>, <grams-of-salt>)
user_1 = Salting('mypassword', <grams-of-salt>)
user_1.seasoning()
```

<p align="center"><b>Result:</b></p>

```python
user_1.showinfo()

{
	'password': 'mypassword',
	'salted_password': '45f6717a673f740c636479a9b7b98b9c',
	'salt': '8LG6et9315DjPuupKBpD'
}
```

```python
''' check_authentication(<to-be-checked-password>) '''
user_1.check_authentication('mypassword')

Passwords matched!!
```

```python
''' create_json(<name-of-file>) '''
user_1.create_json('user_1')

JSON created!!
```


### Installation

saltedmd5 can be installed from PyPI:

```bash
pip install saltedmd5
```


###  What it is
saltedmd5 is a work based on <b>hashlib</b>. It aims to provide developers with a Python functionality to generate simple **salted password hashing** which concerns the security of user account systems.


###  Changes
Please refer to <a href="https://github.com/nat236919/saltedmd5/blob/master/docs/CHANGELOG.md?raw=true">CHANGELOG</a>


###  Getting Involved
Everybody is welcome, please feel free to get on board :)
