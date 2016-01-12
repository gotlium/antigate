Usage
=====

.. _highlevel:

High-level API usage
--------------------

High-level API allows to parse captcha by one line of code::

  from antigate import AntiGate
  print AntiGate('API-KEY', 'captcha.jpg')


Send abuse
----------

If captcha is not valid, you can send abuse::

  from antigate import AntiGate

  gate = AntiGate('API-KEY', 'captcha.jpg')
  if str(gate) != 'qwerty':
    gate.abuse()


Get balance
-----------

Get account balance::

  from antigate import AntiGate

  gate = AntiGate('API-KEY')
  print gate.balance()


Get statistics
--------------

Get statistics data for current account::

  from antigate import AntiGate

  gate = AntiGate('API-KEY')
  print gate.stats()


Get system load
---------------

Before request send, you can check system loads::

  from antigate import AntiGate

  gate = AntiGate('API-KEY')
  print gate.load()


.. _lowlevel:



Low-level API usage
-------------------

Disable auto run and use methods manually::

  from antigate import AntiGate

  config = {'min_len': '3', 'max_len': '5', 'phrase': '2'}

  gate = AntiGate('API-KEY', auto_run=False, send_config=config)

  captcha_id1 = gate.send('captcha1.jpg')
  captcha_id2 = gate.send('captcha2.jpg')

  print gate.get(captcha_id1)
  print gate.get(captcha_id2)


Multiple requests
-----------------

Get results for multiple ids::

  from antigate import AntiGate

  gate = AntiGate('API-KEY', auto_run=False)

  captcha_id1 = gate.send('captcha1.jpg')
  captcha_id2 = gate.send('captcha2.jpg')

  print gate.get_multi([captcha_id1, captcha_id2])


Base64 and Bytes
----------------

Bytes example::

  # Per line binary example
  print AntiGate('API-KEY', fp.read())

  # Custom requests
  gate = AntiGate('API-KEY')
  captcha_id = gate.send(b64encode(fp.read()))
  print gate.get(captcha_id)


Base64 example::

  # Per line base64 example
  print AntiGate('API-KEY', b64encode(fp.read()))

  # Custom requests
  gate = AntiGate('API-KEY')
  captcha_id = gate.send(fp.read())
  print gate.get(captcha_id)
