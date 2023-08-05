# ToolStack

A collection of useful tools to speed-up the data processing, cleaning and pipelining. 
1. Built with Pandas in mind for simplicity and ease of use
2. Perform complex operations with a few method calls

Requirements
------------

-  Python 3.5 or higher
-  Pandas
-  NumPy


Installation
------------

Using PIP via PyPI

    pip install toolstack


    
Usage
--------

```python
from toolstack.text import AutomatedTextPreprocessing
import pandas as pd

df = pd.read_csv('amazon-review-300.csv', header=-1)
ap = AutomatedTextPreprocessing(df, df.columns.tolist())
ap.stack()
```



