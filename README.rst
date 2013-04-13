Real-time captcha-to-text decodings
===================================


Installation:
-------------
1. From source:

.. code-block:: bash

    $ git clone https://github.com/gotlium/antigate.git

    $ cd antigate && sudo python setup.py install

**OR**

.. code-block:: bash

    $  sudo pip install antigate

Usage:
------

    >>> from antigate import AntiGate
    >>> print AntiGate('API-KEY', 'captcha.jpg')

If you wish to complain about a mismatch results, use ``abuse`` method.

**Example:**

    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY', 'captcha.jpg')
    >>> print gate
    >>> if str(gate) != 'qwerty':
    >>>     gate.abuse()

After all manipulations, you can get your balance:

    >>> print gate.balance()

Or get your statistics data:

    >>> print gate.stats()

Real time system load info:

    >>> print gate.load()


Customizing requests to API
---------------------------

Customize grab-lib preferences:

    >>> from antigate import AntiGate
    >>> config = {'connect_timeout': 5, 'timeout': 60}
    >>> gate = AntiGate('API-KEY', 'captcha.jpg', grab_config=config)
    >>> print gate

Additional options for sending Captcha:

    >>> from antigate import AntiGate
    >>> config = {'min_len': '3', 'max_len': '5', 'phrase': '2'}
    >>> gate = AntiGate('API-KEY', 'captcha.jpg', send_config=config)
    >>> print gate

Disable auto run and use methods manually:
    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY', auto_run=False)
    >>> captcha_id1 = gate.send('captcha1.jpg')
    >>> captcha_id2 = gate.send('captcha2.jpg')
    >>> print gate.get(captcha_id1)
    >>> print gate.get(captcha_id2)

Get results for multiple ids:
    >>> gate = AntiGate('API-KEY', auto_run=False)
    >>> captcha_id1 = gate.send('captcha1.jpg')
    >>> captcha_id2 = gate.send('captcha2.jpg')
    >>> print gate.get_multi([captcha_id1, captcha_id2])
