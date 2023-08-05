# jup2py - Make jupyter notebook production ready
Simplest way to convert jupyter notebook to production ready .py file

## Introduction

As a data scientist or some one who loves quick proto-typing, you might be using Jupyter notebook or Ipython console to
build your data pipelines or modelling iteration. Finally when it's time for deployment, the hard time starts,
converting jupyter notebook to simple py file.

You have conventional ways to download it as a .py file from console with or by downloading as .py file from Jupyter 
Notebooks. But they never make it production ready .py file, somethings they mess with magic words or plots.

## Installation

To install Jup2Py from PyPI:

```
$ pip install jup2py
```
* Jup2Py supports Python 3.6 and above
* Only requirement as of now is  `nbconvert`

Jup2Py is still considered in "alpha" stage, and the released version may change
often; therefore, the best way to keep up-to-date with the latest development
is to clone this repository.

## Usage
Jup2Py is made to remove complexity and make it super easy.

Options:
````
Jup2Py :- Simple way to convert your Jupyter Notebook to .py
Please make sure that you have saved the Notebook before running Jup2Py
usage: jup2py [-h] [-v] [-i INPUT] [-o OUTPUT]

Jup2Py :- Simple way to convert your Jupyter Notebook to .py

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Jup2Py Version
  -i INPUT, --input INPUT
                        Input Jupyter Notebook to be converted to .py file
  -o OUTPUT, --output OUTPUT
                        [Optional]: Output python file name and location
````

## Example 

* **NOTE** - Jup2Py requires you to save the Jupyter Notebook before using jup2py

* Command Line
````
jup2py -i <<JUPYTER_NOTEBOOK.ipynb>> -o <<PYTHON_FILENAME.py>>
````

-o/ --output is totally optional, if you don't supply it will save the .py in the same directory save the .ipynb file
````
jup2py -i tests\jup2py_sample.ipynb
````

* Python Code
````
import jup2py
jup2py.jup2py("tests/jup2py_test.ipynb", "tests/test.py")
````

Second argument is totally optional, if you don't supply it will save the .py in the same directory save the .ipynb file

NOTE: - The output file is non-interactive in nature and will override if any previous same name file is found at that location.

## Conversion

Sample Jupyter Notebook -

![Sample Jupyter Notebook](https://raw.githubusercontent.com/shivam-kotwalia/jup2py/master/docs/static/images/Jupyter_sample.png)

Jup2Py converted to production ready .py file in no time -

![Production ready python code](https://raw.githubusercontent.com/shivam-kotwalia/jup2py/master/docs/static/images/Py_sample.png)


## Contact Us

Jup2Py is a very small initiative I took, there are lot of things we can improve on this and make this more stronger.

Please don't hesitate to report a bug through issues.
