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

 $ cd webvulnsrv
 $ python -m webvulnsrv http://localhost:8666/
 Vulnerability: CSRF under http://localhost:8666/csrf/send
 Vulnerability: XSS on http://localhost:8666/xss/?username=Benutzer%21 in parameter username
 
You may notice that this aren't all vulnerabilties, but webvulnsrv is still a work in progress.

Authentification
~~~~~~~~~~~~~~~~

Assuming that under /perform_login is the post target of the login form and the username and password are "user" and "123456", we have to built a python list and struct containing it, ex.

.. code:: python

 ["http://example.site/perform_login",{"post_name":"user","pwd":"123456"}]

Please note that you have to escape any spaces and braces. Now we have to simply call webvulnscan with this list under the --auth option, ex.

.. code:: sh

 $ python -m webvulnscan.py --auth \[\"http://ex.site/", \{\"post\":\"user\",\"pwd":\"123456\"\}\] http://ex.site/

Why is it so complicated? Because I'm still searching for a better option, but don't know of any...
