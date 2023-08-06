# xinge-api-python

[![PyPI version](https://badge.fury.io/py/xinge.svg)](https://badge.fury.io/py/xinge)

## 概述

欢迎使用信鸽 ServerSDK - Python 版本封装的开发包，具有最新版本的信鸽 API 功能。

## 兼容版本

- Python 3.7
- 需要使用到 requests

```shell
➜  ~ pip install requests
```

- 如需运行测试用例，需要安装 unittest

```sbtshell
pip install unittest2
```

## 引用 SDK

```shell
  pip install xinge
```

## 代码示例

```python
from xinge_push import Xinge, Message

xinge = Xinge('app id', 'secret key')
message = Message(title="some title", content = "some content")
xinge.push_account(platform="android", account="some account", message=message)
ret_code, error_msg = xinge.push_account(platform="android", account="some account", message=message)
if ret_code:
    print "push failed! retcode: {}, msg: {}".format(ret_code, error_msg)
else:
    print "push successfully!"

```

## Publish

```shell
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
