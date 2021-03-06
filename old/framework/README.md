DARE  
=============

To achieve the goal of supporting both types of parallelism, on heterogeneous distributed computing resources, we have
developed the Dynamic Application Runtime Environment (DARE) framework.
At the core of the DARE framework, is a SAGA BigJob (which is a flexible general purpose pilot-job implementation). With a
suitable Web development framework, it supports the development of a lightweight but extensible, science gateway capable 
of using a range of distributed resources. The effectiveness of  DARE framework supports a wide range of infrastructure, 
problem instance configurations and size.



Web Page & Mailing List
-----------------------

Web page: https://github.com/saga-project/DARE/wiki

Mailing list:  Use dare-users@googlegroups.com


DEMO PAGE
----------------------------
http://dare.cct.lsu.edu/gateways/ngs


Installation
-------------

	virtualenv dareenv
	source dareenv/bin/activate
	easy_install DARE


Configuration of Coordination Backend
-------------------------------------
Edit or create ~/.darerc 

	[DEFAULT]
	COORDINATION_URL =redis://localhost:6379

Usage
-----
	wget https://raw.github.com/saga-project/DARE/master/framework/examples/simple_examples/hello.dare
	dare-run hello.dare

For more information about Coordination please visit https://github.com/saga-project/BigJob/wiki


Packaging
-------------------------------------

Requirements:

*  setuptools >0.6c11, http://pypi.python.org/pypi/setuptools


Building PyPi package

	python setup.py build

Upload to PyPi

	python setup.py sdist upload
