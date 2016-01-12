Real-time captcha-to-text decodings
===================================

.. image:: https://api.travis-ci.org/gotlium/antigate.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/gotlium/antigate
.. image:: https://coveralls.io/repos/gotlium/antigate/badge.png?branch=master
    :target: https://coveralls.io/r/gotlium/antigate?branch=master
.. image:: https://img.shields.io/badge/python-2.6,2.7,3.3,3.4,3.5-blue.svg
    :alt: Python 2.6, 2.7, 3.3, 3.4, 3.5
    :target: https://pypi.python.org/pypi/antigate/
.. image:: https://img.shields.io/pypi/v/antigate.svg
    :alt: Current version on PyPi
    :target:https://pypi.python.org/pypi/antigate/
.. image:: https://img.shields.io/pypi/dm/antigate.svg
    :alt: Downloads from PyPi
    :target:https://pypi.python.org/pypi/antigate/
.. image:: https://img.shields.io/badge/license-GPLv2-green.svg
    :target: https://pypi.python.org/pypi/antigate/
    :alt: License



Documentation available `here <https://pythonhosted.org/antigate/>`_.


Installation
------------

From source:

.. code-block:: bash

    $ git clone https://github.com/gotlium/antigate.git

    $ cd antigate && python setup.py install

From PyPi:

.. code-block:: bash

    $  pip install antigate


**Requirements:**

You can use grab/requests/urllib as http backends.

`Grab` installation:

.. code-block:: bash

    pip install grab pycurl


`Requests` installation:

.. code-block:: bash

    pip install requests


`UrlLib` used by default.


Usage
-----

.. code-block:: python

    >>> from antigate import AntiGate            # AntiCaptcha

    # per line example
    >>> print AntiGate('API-KEY', 'captcha.jpg') # AntiCaptcha('API-KEY', filename or base64 or bytes)

    # or like this
    >>> gate = AntiGate('API-KEY')               # AntiCaptcha('API-KEY')
    >>> captcha_id = gate.send('captcha.jpg')
    >>> print gate.get(captcha_id)


If you wish to complain about a mismatch results, use ``abuse`` method:

.. code-block:: python

    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY', 'captcha.jpg')
    >>> if str(gate) != 'qwerty':
    >>>     gate.abuse()

After all manipulations, you can get your account balance:

.. code-block:: python

    >>> print gate.balance()


Or get your statistics data:

.. code-block:: python

    >>> print gate.stats()


System load info:

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

Use all methods manually:

.. code-block:: python

    >>> from antigate import AntiGate
    >>> gate = AntiGate('API-KEY')
    >>> captcha_id1 = gate.send('captcha1.jpg')
    >>> captcha_id2 = gate.send('captcha2.jpg')
    >>> print gate.get(captcha_id1)
    >>> print gate.get(captcha_id2)

Get results for multiple ids:

.. code-block:: python

    >>> gate = AntiGate('API-KEY')
    >>> captcha_id1 = gate.send('captcha1.jpg')
    >>> captcha_id2 = gate.send('captcha2.jpg')
    >>> print gate.get_multi([captcha_id1, captcha_id2])


If you want use bytes or base64:

.. code-block:: python

    # Per line binary example
    >>> print AntiGate('API-KEY', fp.read())

    # Per line base64 example
    >>> print AntiGate('API-KEY', b64encode(fp.read()))

    # Custom requests
    >>> gate = AntiGate('API-KEY')

    # base64
    >>> captcha_id = gate.send(b64encode(fp.read()))

    # or stream
    >>> captcha_id = gate.send(fp.read())

    >>> print gate.get(captcha_id)


Api documentation
-----------------
https://anti-captcha.com/apidoc / http://antigate.com/?action=api#algo


Compatibility
-------------
* Python: 2.6, 2.7, 3.3, 3.4, 3.5


.. image:: https://d2weczhvl823v0.cloudfront.net/gotlium/antigate/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free
