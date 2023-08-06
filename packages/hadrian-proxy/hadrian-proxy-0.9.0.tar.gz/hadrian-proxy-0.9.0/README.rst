=======
Hadrian
=======

.. image:: test_fs/hadrians.jpg
   :scale: 50 %
   :alt: Hadrian's Wall
   :align: center


Hadrian is a simple proxy that requires authentication.
Stick it in front of simple ad-hoc services to protect
them from the general public.

Most people use HTTP Basic Authentication for this
(you should probably consider it, it's built into your
webserver) but password managers have issues filling
out the popup box in some browsers.


Backends
========

Hadrian supports both a filesystem backend and http
service backend. See `test_fs.conf` or `test_proxy.conf`
for examples of setting up each.


Usage
=====

::
    
    $ python -m hadrian test_fs.conf


