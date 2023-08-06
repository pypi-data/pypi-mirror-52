# Pythonのライブラリ作成方法

GitHubから [pip](https://ja.wikipedia.org/wiki/Pip) で利用できるようにライブラリを開発・配布する方法を紹介します。

## 流れ

```
$ pip install -v git+https://github.com/t-cool/pylib.git
$ python -m pylib.hello
Hello, world.
```

## ライブラリ作成に必要なファイル

```
├── LICENSE.py
├── README.md
├── setup.cfg
├── entry_points.cfg
├── pylib
│   ├── __init__.py
│   └── hello.py
└── setup.py
```

### LICENSE

ライセンスの情報を書きます。

### README.md

ライブラリの基本的な利用法等を書きます。

### setup.cfg

ライブラリのメタ情報を保存するファイルです。

```
[metadata]
name = pylib
version = 0.0.1
url = https://github.com/t-cool/pylib
author = t-cool
license_file = LICENSE
description = A template to generate Python library
long_description = file: README.md

[options]
zip_safe = False
packages = find:
install_requires =
  requests
entry_points = file: entry_points.cfg
```

install_requiresには、依存ライブラリを明記します。

### entry_points.cfg

エントリーポイントを指定するためのファイルです。

```
[console_scripts]
hello.py = pylib.hello:main
```

### pylib/__init__.py

このフォルダが1つのパッケージであることを示すファイルです。 空でも良いですし、初期化処理を記述することもできます。


### pylib/hello.py

モジュールのファイルです。

```python
def main():
    import getpass
    print('Hello, ' + getpass.getuser() + '!')


if __name__ == '__main__':
    main()
```


### setup.py

新しいsetuptoolsでは setup.cfg の設定を読み込むため、 setup() に多くの引数を渡す必要は無くなりました。

```python
from setuptools import setup
setup()
```

## 参考

[setuptools — Pythonパッケージ作成](https://heavywatal.github.io/python/setuptools.html)
