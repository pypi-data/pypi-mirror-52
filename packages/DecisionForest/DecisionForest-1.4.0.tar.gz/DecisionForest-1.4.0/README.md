# DecisionForest Python ![CI status](https://img.shields.io/badge/DecisionForest-v1.1.1-blue.svg) ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

Python package for DecisionForest API access

### Installation

The installation process varies depending on your python version and system used. However in most cases the following should work:

```
pip install decisionforest
```

### Configuration

Sign up at [DecisionForest](https://www.decisionforest.com/) and get the API key

```
import decisionforest
decisionforest.Config.KEY = 'testkey890123456789012345678901234567890'
```

### Getting Data

The most basic call needed to retrieve a dataset (returns all the data available for a dataset):

```
python
import decisionforest
decisionforest.Config.KEY = 'testkey890123456789012345678901234567890'
df = decisionforest.get('SMD')
```

Another example that returns data by date and symbol:

```
python
import decisionforest
decisionforest.Config.KEY = 'testkey890123456789012345678901234567890'
df = decisionforest.get('SMD', date='2018-12-28', symbol='AAPL')
```
