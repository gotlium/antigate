Real-time captcha-to-text decodings
===================================

.. image:: https://api.travis-ci.org/gotlium/antigate.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/gotlium/antigate
.. image:: https://coveralls.io/repos/gotlium/antigate/badge.png?branch=master
    :target: https://coveralls.io/r/gotlium/antigate?branch=master
.. image:: https://pypip.in/v/antigate/badge.png
    :alt: Current version on PyPi
    :target: https://crate.io/packages/antigate/
.. image:: https://pypip.in/d/antigate/badge.png
    :alt: Downloads from PyPi
    :target: https://crate.io/packages/antigate/


Documentation available at `Read the Docs <http://antigate.readthedocs.org/>`_.


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

.. code-block:: python

    >>> from antigate import AntiGate
    >>> print AntiGate('API-KEY', 'captcha.jpg')

If you wish to complain about a mismatch results, use ``abuse`` method.

**Example:**

.. code-block:: python

    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY', 'captcha.jpg')
    >>> print gate
    >>> if str(gate) != 'qwerty':
    >>>     gate.abuse()

After all manipulations, you can get your balance:

.. code-block:: python

    >>> print gate.balance()


Or get your statistics data:

.. code-block:: python

    >>> print gate.stats()


Real time system load info:

.. code-block:: python

    >>> print gate.load()


Customizing requests to API
---------------------------

Customize grab-lib preferences:

.. code-block:: python

    >>> from antigate import AntiGate
    >>> config = {'connect_timeout': 5, 'timeout': 60}
    >>> gate = AntiGate('API-KEY', 'captcha.jpg', grab_config=config)
    >>> print gate

Additional options for sending Captcha:

.. code-block:: python

    >>> from antigate import AntiGate
    >>> config = {'min_len': '3', 'max_len': '5', 'phrase': '2'}
    >>> gate = AntiGate('API-KEY', 'captcha.jpg', send_config=config)
    >>> print gate

Disable auto run and use methods manually:

.. code-block:: python

    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY', auto_run=False)
    >>> captcha_id1 = gate.send('captcha1.jpg')
    >>> captcha_id2 = gate.send('captcha2.jpg')
    >>> print gate.get(captcha_id1)
    >>> print gate.get(captcha_id2)

Get results for multiple ids:

.. code-block:: python

    >>> gate = AntiGate('API-KEY', auto_run=False)
    >>> captcha_id1 = gate.send('captcha1.jpg')
    >>> captcha_id2 = gate.send('captcha2.jpg')
    >>> print gate.get_multi([captcha_id1, captcha_id2])


Compatibility:
-------------
* Python: 2.6, 2.7, 3.3


.. image:: https://d2weczhvl823v0.cloudfront.net/gotlium/antigate/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free
