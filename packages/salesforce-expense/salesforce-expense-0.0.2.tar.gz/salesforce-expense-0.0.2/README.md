# PSE expense Entry


[![PyPI version](https://badge.fury.io/py/salesforce-expense.svg)](https://badge.fury.io/py/salesforce-expense)
[![Build Status](https://api.travis-ci.org/giuliocalzolari/salesforce-expense.svg?branch=master)](https://travis-ci.org/giuliocalzolari/salesforce-expense/)


## Install
just use pip

```bash
$ pip install salesforce-expense
```

## Config
this script is designed to create a pse_expense

create your local Config `~/.pse.json`

```bash
  {
    "username": "your-salesforce-email@login.com",
    "password": "fdgdhrx6MA==",
    "token": "afghfyfgbgnegrfbgdhtd"
  }
```

`password` must be `base64` encoded

```bash
$ echo -n "my-password" | base64
```

to get `token` please follow this [Guide](https://onlinehelp.coveo.com/en/ces/7.0/administrator/getting_the_security_token_for_your_salesforce_account.htm)

## WIP

# License

salesforce-expense is licensed under the [WTFPL](LICENSE).
