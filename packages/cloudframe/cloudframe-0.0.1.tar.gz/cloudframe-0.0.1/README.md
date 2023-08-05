# The Cloudframe Data Scientist Simple Enabler

At Cloudframe we employ teams of Data Scientists, Data Engineers, and Software Developers.  Check us out at [http://cloudframe.io](http://cloudframe.io "Cloudframe website")

If you're interested in joining our team as a Data Scientist see here: [Bid Prediction Repo](https://github.com/cloudframe/texas-bid-prediction).  There you'll find a fun problem and more info about our evergreen positions for Data Scientists, Data Engineers, and Software Developers.

This package contains modules that are used to smooth the data science workflow.  

## Installation

`pip install cloudframe`

## Dependencies

This package uses JSON and YAML to store and fetch model objects.  

* `pyyaml`
* `json`

## Structure

```
| cloudframe/
|
|-- model_tracker/
|   |-- __init__.py
|   |-- tracker.py
|
|-- Manifest.in
|-- README.md
|-- setup.py
```

## Usage

Placeholder... where `best` below is a valid model object.


```
from cloudframe.model_tracker import tracker

tracker = tracker.project(name = 'myproject', dirpath = '\dir\to\models\')
tracker.initialize()

tracker.add(best)
```