===========
webvulnscan
===========

.. image:: https://travis-ci.org/SysTheron/webvulnscan.png?branch=master
   :target: https://travis-ci.org/SysTheron/webvulnscan/builds

Quickstart
----------

.. code:: sh 

 $ git clone https://github.com/SysTheron/webvulnscan.git; cd webvulnscan
 $ python -m webvulnscan http://example.target/

What is it?
-----------
As the name suggests, webvulnscan is (or wants to be someday) a security scanner for Web Applications with the intent of automatic testing, licensed under the MIT-License. It's written in Python(compatible with 2.7 and 3.3) and doesn't require any external libraries. 

Features
--------
- Link & Form Crawling
- XSS Detection
- CSRF Detection
- Authentification

Todo
----
1. Extend userinterface
2. Multitasking
3. More Attacks


Examples
--------

vulnsrv
~~~~~~~

(vulnsrv)[https://github.com/phihag/vulnsrv] is sample exploitable website for educational purposes. We will use it here as an example:

.. code:: sh

 $ wget https://raw.github.com/phihag/vulnsrv/master/vulnsrv.py
 $ python vulnsrv.py

It's running now under http://localhost:8666/ on your computer. Open now a new console for running webvulnsrv. Assuming that you are in your home directory and already cloned webvulnsrv...

.. code:: sh

 $ cd webvulnscan
 $ python -m webvulnscan http://localhost:8666/
 Vulnerability: CSRF under http://localhost:8666/csrf/send
 Vulnerability: XSS on http://localhost:8666/xss/?username=Benutzer%21 in parameter username
 
You may notice that this aren't all vulnerabilties, but webvulnsrv is still a work in progress.

Authentification
~~~~~~~~~~~~~~~~

We have a login handler under /perform_login which wants the post-fields username and password, who can we log in? The account we want to use has the username "abc" and password "123456". The command would look like the following:

.. code:: sh

 $ python -m webvulnscan --auth http://no.tld/perform_login --auth-data username=abc --auth-data password=123456 http://no.tld/

Yes, you have to use the --auth-data option for every field you want to send.
