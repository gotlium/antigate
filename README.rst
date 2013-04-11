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
    >>> print AntiGate('API-KEY', 'captcha.jpg')

if you want send abuse to do not matching result, use ``abuse`` method.

**Example:**

    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY', 'captcha.jpg')
    >>> print code
    >>> if str(code) != 'qwerty':
    >>>     gate.abuse()

After all manipulations, you can get your balance:

    >>> print gate.balance()

Or full statistic:

    >>> print gate.stats()

System load:

    >>> print gate.load()

Customize grab preferences:

    >>> from antigate import AntiGate
    >>> config = {'connect_timeout': 5, 'timeout': 60}
    >>> gate = AntiGate('API-KEY', 'captcha.jpg', grab_config=config)

Additional options for sending Captcha:

    >>> from antigate import AntiGate
    >>> config = {'min_len': '3', 'max_len': '5', 'phrase': '2'}
    >>> gate = AntiGate('API-KEY', 'captcha.jpg', send_config=config)

Disable auto run and use methods manually:
    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY', auto_run=False)
    >>> captcha_id1 = gate.send('captcha1.jpg')
    >>> captcha_id2 = gate.send('captcha2.jpg')
    >>> print gate.get(captcha_id1)
    >>> print gate.get(captcha_id2)

Multi ids:
    >>> gate = AntiGate('API-KEY', auto_run=False)
    >>> captcha_id1 = gate.send('captcha1.jpg')
    >>> captcha_id2 = gate.send('captcha2.jpg')
    >>> print gate.get_multi([captcha_id1, captcha_id2])
