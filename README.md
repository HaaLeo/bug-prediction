# bugprediction

[![Pypi](https://img.shields.io/pypi/v/bugprediction.svg?style=flat-square)](https://pypi.python.org/pypi/bugprediction) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bugprediction.svg?style=flat-square)](https://pypi.python.org/pypi/bugprediction) [![PyPI - Downloads](https://img.shields.io/pypi/dm/bugprediction.svg?style=flat-square)](https://pypistats.org/packages/bugprediction) [![Stars](https://img.shields.io/github/stars/HaaLeo/bug-prediction.svg?label=Stars&logo=github&style=flat-square)](https://github.com/HaaLeo/bug-prediction/stargazers)  
[![PyPI - License](https://img.shields.io/pypi/l/bugprediction.svg?style=flat-square)](https://raw.githubusercontent.com/HaaLeo/bug-prediction/master/LICENSE.txt) 
[![Build Status](https://img.shields.io/travis/HaaLeo/bug-prediction/master.svg?style=flat-square)](https://travis-ci.org/HaaLeo/bug-prediction) [![Codecov](https://img.shields.io/codecov/c/github/HaaLeo/bug-prediction.svg?style=flat-square)](https://codecov.io/gh/HaaLeo/bug-prediction) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)  
[![Donate](https://img.shields.io/badge/☕️-Buy%20Me%20a%20Coffee-blue.svg?&style=flat-square)](https://www.paypal.me/LeoHanisch/3eur)

## Description

This repository enables you to calculate the history complexity metric Ahmed E. Hassan introduced at the [2009 IEEE 31st International Conference on Software Engineering](https://ieeexplore.ieee.org/document/5070510) in May 200ß9 (DOI: 10.1109/ICSE.2009.5070510).  
The implementation was part of the course [Software Qualität](https://campus.tum.de/tumonline/wbLv.wbShowLVDetail?pStpSpNr=950402174) at the Technical University of Munich in summer 2019.

## Installation

### From Source

```
git clone git@github.com:HaaLeo/bug-prediction.git
cd bug-prediction

python setup.py sdist bdist_wheel
pip install dist/bugprediction-0.0.1.tar.gz

bugprediction --version
```

### From Pypi
> ❗️ The package is not released yet

You can install the package with `pip` from [pypi](https://pypi.org/project/bugprediction):

```
pip install bugprediction

bugprediction --version
```

## Usage

To print all available options:

```
bugprediction --help
```

### Features

TBD

### API

In addition to the client you can also use the API:

```python
from bugprediction import calculate_hcm

history_complexity_metric = calculate_hcm(**kwargs)
```

## Contribution

If you found a bug or are missing a feature do not hesitate to [file an issue](https://github.com/HaaLeo/bug-prediction/issues/new/choose).  
Pull Requests are welcome!

## Support
When you like this package make sure to [star the repository](https://github.com/HaaLeo/bug-prediction/stargazers). I am always looking for new ideas and feedback.  
In addition, it is possible to [donate via paypal](https://www.paypal.me/LeoHanisch/3eur).
