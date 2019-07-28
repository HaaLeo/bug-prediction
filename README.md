# bugprediction

[![Stars](https://img.shields.io/github/stars/HaaLeo/bug-prediction.svg?label=Stars&logo=github&style=flat-square)](https://github.com/HaaLeo/bug-prediction/stargazers)  
[![Build Status](https://img.shields.io/travis/HaaLeo/bug-prediction/master.svg?style=flat-square)](https://travis-ci.org/HaaLeo/bug-prediction) [![Codecov](https://img.shields.io/codecov/c/github/HaaLeo/bug-prediction.svg?style=flat-square)](https://codecov.io/gh/HaaLeo/bug-prediction) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)  
[![Donate](https://img.shields.io/badge/☕️-Buy%20Me%20a%20Coffee-blue.svg?&style=flat-square)](https://www.paypal.me/LeoHanisch/3eur)

## Description

This repository enables you to calculate the history complexity metric Ahmed E. Hassan introduced at the [2009 IEEE 31st International Conference on Software Engineering](https://ieeexplore.ieee.org/document/5070510) in May 2009 (DOI: 10.1109/ICSE.2009.5070510) and use it for the prediction of the amount of bugs.
The implementation was part of the course [Software Qualität](https://campus.tum.de/tumonline/wbLv.wbShowLVDetail?pStpSpNr=950402174) at the Technical University of Munich in summer 2019.  
The training data set was derived from the data set that Marco D'Ambros, Michele Lanza and Romain Robbes used in their paper [An Extensive Comparison of Bug Prediction Approaches](https://ieeexplore.ieee.org/document/5463279). The original data set is available at http://bug.inf.usi.ch/index.php.

## Installation

### From Source

```
git clone git@github.com:HaaLeo/bug-prediction.git
cd bug-prediction

pipenv install
pipenv shell

python -m bugprediction --version
```

## Usage

To print all available options:

```
python -m bugprediction --help
```

Training is currently only possible from source. To do so run the edit the `train.py` to your needs and run it.


### API
In order to use the API you need to bundle and install the package:

```python
python setup.py sdist bdist_wheel
pip install dist/bugprediction-0.0.1.tar.gz
```

Then you can use tha API like shown bellow:

```python
from bugprediction import calculate_hcm, predict

history_complexity_metric, _ = calculate_hcm(**kwargs)
prediction_map = predict(hcm_map, **args)
```

## Contribution

If you found a bug or are missing a feature do not hesitate to [file an issue](https://github.com/HaaLeo/bug-prediction/issues/new/choose).  
Pull Requests are welcome!

## Support
When you like this package make sure to [star the repository](https://github.com/HaaLeo/bug-prediction/stargazers). I am always looking for new ideas and feedback.  
In addition, it is possible to [donate via paypal](https://www.paypal.me/LeoHanisch/3eur).
