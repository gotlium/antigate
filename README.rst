Real-time captcha-to-text decodings
===================================


Installation:
-------------
1. Package:

.. code-block:: bash

    $ git clone https://github.com/gotlium/antigate.git

    $ cd antigate && sudo python setup.py install

**OR**

.. code-block:: bash

    $  sudo pip install antigate

Usage:
------

    >>> from antigate import AntiGate
    >>> print AntiGate('API-KEY','captcha.jpg')

if you want send abuse to do not matching result, use ``abuse`` method.
**Example:**

    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY','captcha.jpg')
    >>> print code
    >>> if str(code) != 'qwerty':
    >>>     gate.abuse()

After all manipulations, you can get your balance:

    >>> print gate.balance()

Or full statistic:

    >>> print gate.stats()

