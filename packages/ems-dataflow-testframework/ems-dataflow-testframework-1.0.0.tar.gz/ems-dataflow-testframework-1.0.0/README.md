ems-dataflow-testframework
==========================

[![Codeship status](https://app.codeship.com/projects/b6f50310-b6ba-0137-4346-7a70f6e67953/status?branch=master)](https://app.codeship.com/projects/364126)
[![PyPI version](https://badge.fury.io/py/ems-dataflow-testframework.svg)](https://badge.fury.io/py/ems-dataflow-testframework)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)

Purpose of the project
======================

This framework aims to help test Google Cloud Platform dataflows in an end-to-end way.

How to develop locally
======================

Use [virtualenv](https://docs.python-guide.org/dev/virtualenvs/) preferably to manage Python dependencies.

```bash
pip install -r requirements.txt
```

How to run unit tests
=====================
```bash
make test
```

How to run statical code analysis
=================================
```bash
make check
```

How to contribute
=================
Fork the repository and apply your changes. Pull requests are welcome. Please pay attention on the commit message [conventions](https://github.com/semantic-release/semantic-release). Thanks in advance!

How to release
=================================
Releasing is managed by [python-semantic-release](https://github.com/relekang/python-semantic-release) which means your commit messages define the upgraded version number. Use the following convention during writing commit messages:
 1. fix({SCOPE}): {BODY} -> patch
 2. feat({SCOPE}): {BODY} -> minor
 3. xxx({SCOPE}): {BODY} -> BREAKING CHANGE -> major

If you are unsure how to write valid commit messages enforce yourself with using tools like [commitizen](https://github.com/commitizen/cz-cli).
 
To trigger a release merge `master` branch into `release` and push it.

License
=======
[MIT](https://choosealicense.com/licenses/mit/)

