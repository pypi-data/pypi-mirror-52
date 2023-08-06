Pockethernet
============

This is a python module that implements the bluetooth protocol used by the Pockethernet network tester. It also includes
a basic command line client.

.. code-block:: console

    $ pockethernet 00:13:43:xx:xx:xx
    Straight cable
    Pair voltages:
    - 0V
    - 0V
    - 0V
    - 0V
    PoE A: 0V
    PoE B: 0V
    No link established

    $ pockethernet 00:13:43:xx:xx:xx
    Cable inserted into ethernet port
    Pair voltages:
    - 0V
    - 0V
    - 0V
    - 0V
    PoE A: 0V
    PoE B: 0V
    Got 1000BASE-T full duplex link
    Link partner advertises:
                HD  FD
      10 MBIT   1   1
     100 MBIT   1   1
    1000 MBIT   1   1

The python API so far:

.. code-block:: python

    from pockethernet import Pockethernet, WiremapResult, PoEResult, LinkResult
    bluething = Pockethernet()
    bluething.connect("00:13:43:xx:xx:xx")
    wiremap = bluething.get_wiremap()
    print(wiremap.connections) # [0, 1, 2, 3, 4, 5, 6, 7, 8]

    link = bluething.get_link()
    print(link.speed) # 1000BASE-T