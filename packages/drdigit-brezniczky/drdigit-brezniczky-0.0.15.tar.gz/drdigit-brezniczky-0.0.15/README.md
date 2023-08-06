DrDigit
=======

DrDigit is a digit doctoring detection package at an early stage.
Interested in contributing? Please feel free to contact me, e.g. by
commenting on the issue "Contributors welcome!" at 
https://github.com/brezniczky/drdigit/issues/1.

Requirements
------------

DrDigit requires Python 3.5 or later.

Concept
-------

The tests are based on the statistics of digits which are assumed to have a
uniform distribution. Near-uniform distributions can be obtained by looking
at the last digits of sufficiently large values - such as vote counts
(possibly above 100).

On a smaller scale, you can query for the probablity of a digit sequence using
probability mass functions represented by Python functions.

There are larger scale tests for a sequence of digit groups. This is so to
support situations where different groups are expected to be doctored by
different people - testing for an overarching, consistent anomaly could be too
strict in such cases.

Based on the current features (entropy, digit repetition, coincident digits in
parallel sequences), it is possible to sort a data frame containing digit groups
by probability, so then it is possible to inspect if there is any apparent
sanity behind the doctoring.

A couple of hints
-----------------

* Handle results with care, **there is always some uncertainity**
* Try to **focus** on interesting groups, this should yield much sharper results
* When committing **Kaggle** scripts, switch off the on-disk caching of tests 
  before committing, e.g. via
  
    ```
    import drdigit as drd
    drd.set_option(physical_cache_path="")
    ```
  
  You can find more about it via `help(drd.set_option)`.

Quick start
-----------

DrDigit can be installed using pip:

    $ pip install drdigit-brezniczky
    $ ipython

Digit entropy behaves a little weirdly when different digit sequence lengths are 
considered - isn't the sequence 1, 2 as diverse as possible?

    Python 3.5.2 (default, Nov 12 2018, 13:43:14)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.7.0 -- An enhanced Interactive Python. Type '?' for help.
    
    In [1]: import drdigit as drd
    
    In [2]: help(drd)
    
    In [3]: print(drd.get_entropy([1, 2]))                                                                                                       
    0.6931471805599453
    
    In [4]: print(drd.get_entropy([1, 1, 2, 2]))                                                                                                 
    0.6931471805599453
    
Probabilities are often more suited for a comparison:
    
    In [6]: drd.prob_of_entr(2, drd.get_entropy([1, 2]))                                                                                   
    cdf for 2 was generated
    Out[6]: 1.0
    
    In [7]: drd.prob_of_entr(4, drd.get_entropy([1, 1, 2, 2]))                                                                                   
    cdf for 4 was generated
    Out[7]: 0.0624
    
Indeed, the latter sequence is unusually repetitive.

More examples to follow, for now you can have a look at the Kaggle notebook at 
https://www.kaggle.com/brezniczky/poland-2019-ep-elections-doctoring-quick-check
or around
https://github.com/brezniczky/ep_elections_2019_hun/blob/master/PL/
for instance in the `process_data.py` file.

Some complicated (and - sorry, sometimes unreliabe/slightly outdated) details 
about the considerations/methodology and future ideas can be found in the
[Hungarian elections document](
https://nbviewer.jupyter.org/github/brezniczky/ep_elections_2019_hun/blob/master/report.ipynb
)


Tests
-----

The few tests that there are can be run by `pytest`. 

For this, I would just use `virtualenvwrapper` and do something akin to

    $ mkvirtualenv drdigit_test
    $ pip install -r requirements/requirements_test.txt
    $ pytest
 
from the directory of the `drdigit` clone.
