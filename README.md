DARE  
=============

To achieve the goal of supporting flexible, extensible and interoperable usage of 
heterogeneous performance distributed computing  (HPDC) resources, we have
developed the Distributed Application Runtime Environment (DARE) framework. 
DARE is a standards-based, abstraction-driven middleware layer that provides these capabilities.


At the core of DARE lies SAGA and SAGA-BigJob. 
SAGA-BigJob is a flexible general purpose pilot-job implementation, which has been shown to be a powerful
abstraction for resource management. SAGA provides the interoperability layer.
Combined, SAGA and SAGA-BigJob are used to support the resource management capabilities of many tools.

Furthermore, with a suitable Web development framework, DARE supports the development of a lightweight 
but extensible, science gateway capable of using a range of distributed resources. 
Currently, DARE uses DJANGO.

DARE is an example of a Platform Independent Library, with specific support for 
a range of commonly occuring "patterns" (namely stand-alone applications (Type I),  pipelines of tasks (Type II) 
and execution patterns such as bag-of-tasks, coupled-ensembles etc (Type III)

The effectiveness of the DARE framework lies in providing a simple, scalable and sustainable  
approach to developing and supporting a wide range of patterns of execution independent of the
infrastructure, problem instance configurations and size.



Web Page & Mailing List
-----------------------

Web page: https://github.com/saga-project/DARE/wiki

Mailing list:  Use dare-users@googlegroups.com


DEMO PAGE
----------------------------
http://gw68.quarry.iu.teragrid.org


INSTALLATION
----------------------------

1) Check out the code

        $ mkdir workspace 
        $ cd workspace
        $ git clone https://github.com/saga-project/DARE/

2) Create virtualenv

        $ virtualenv /tmp/envdare
        $ source /tmp/envdare/bin/activate
    
3) INSTALL DARE-BIGJOB Env.

        $ cd DARE/DARE-BIGJOB
        $ pip install -r requirements.txt

USAGE
----------------------------
1) create/sync/update Database schema

        $ python manage.py syncdb
        $ python manage.py migrate

2) Running the django web server

        $ python manage.py runserver
