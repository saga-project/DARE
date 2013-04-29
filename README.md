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
