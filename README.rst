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
