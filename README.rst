===========
webvulnscan
===========

.. image:: https://travis-ci.org/hhucn/webvulnscan.png?branch=master
   :target: https://travis-ci.org/hhucn/webvulnscan/builds

Quickstart
----------

.. code:: sh 

 $ git clone https://github.com/hhucn/webvulnscan.git
 $ cd webvulnscan
 $ python -m webvulnscan http://example.target/

What is it?
-----------
As the name suggests, webvulnscan is (or wants to be someday) a security scanner for Web Applications with the intent of automatic testing, licensed under the MIT-License. It's written in Python(compatible with 2.7 and 3.3) and doesn't require any external libraries. 

Features
--------
- Link & Form Crawling
- Detection for XSS, CRSF, Breach, Clickjacking and cacheable Cookies
- White- and Blacklisting of Pages
- Authentification

Examples
--------

vulnsrv
~~~~~~~

vulnsrv_ is sample exploitable website for educational purposes. We will use it here as an example:

.. _vulnsrv: https://github.com/phihag/vulnsrv

.. code:: sh

 $ wget https://raw.github.com/phihag/vulnsrv/master/vulnsrv.py
 $ python vulnsrv.py

It's running now under http://localhost:8666/ on your computer. Open now a new console for running webvulnsrv. Assuming that you are in your home directory and already cloned webvulnscan...

.. code:: sh

 $ cd webvulnscan
 $ python -m webvulnscan http://localhost:8666/
 Vulnerability: CSRF under http://localhost:8666/csrf/send
 Vulnerability: XSS on http://localhost:8666/xss/?username=Benutzer%21 in parameter username

You may notice that this aren't all vulnerabilties, but webvulnsrv is still a work in progress.

Specific scanning
~~~~~~~~~~~~~~~~~

If you want to scan only for specific vulnerabilities(for example, only for BREACH), you simply try the following:

.. code:: sh

 $ python -m webvulnscan --breach http://localhost:8666/

or you want to scan for XSS and CSRF vulnerabilities:

.. code:: sh

 $ python -m webvulnscan --xss --csrf http://localhost:8666/

What if you want to be more specific? What if you want to test only one site? Use --no-crawl

.. code:: sh

 $ python -m webvulnscan --no-crawl http://localhost:8666/

And the links will be ignored. However, Forms are not.

White- and Blacklisting
~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, you have links on a site you that you want to test to. But the default whitelist points only on the host of the given link. Here's how you can add more:

.. code:: sh

 $ python -m webvulnscan --whitelist http://ex.am.ple/ http://localhost/

However, what if you want to use Authentification and there's a /logout-Link? If the crawler hits it, the session is lost. Simply Blacklist it!

.. code:: sh

 $ python -m webvulnscan --blacklist logout http://localhost/

And the site will be never visited. Please note that the blacklist Parameter accepts Regular Expressions, the python version.

Authentification
~~~~~~~~~~~~~~~~

We have a login handler under /perform_login which wants the post-fields username and password, who can we log in? The account we want to use has the username "abc" and password "123456". The command would look like the following:

.. code:: sh

 $ python -m webvulnscan --auth http://no.tld/perform_login --auth-data username=abc --auth-data password=123456 http://no.tld/

Yes, you have to use the --auth-data option for every field you want to send.

Configuration
~~~~~~~~~~~~~

As you see, there you end up with a lot of parameters in the end. To avoid typing so much, you can add the --write-out-Option and

.. code:: sh

 $ python -m webvulnscan --write-out=example.conf http://localhost:8666/

save it to a file. If you want to rerun the test because you (think you) fixed it, simply run:

.. code:: sh

 $ python -m webvulnscan -c example.conf
