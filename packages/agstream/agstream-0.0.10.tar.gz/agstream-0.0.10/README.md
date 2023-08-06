AgspStream
==============
   
Agriscope data interface for python

This module allows to get data from yours Agribases programmatically
Data are retreived as an Pandas Datagrams

The development map will introduce data computing capabilities, to enhance
data analysis comming from agricultural field.


What's New
===========
- (2019/09) v0.0.10 : solve some display problems
- (2019/08) Porting to python 3
- (2018/05) Add functionnal information on Agribases (type, sampling)
- (2018/05) Solve bug on from, to date 
- (2018/02) First version 

Dependencies
=============

Agstream is written to be use with python 2.7 and python 3.6
It requires Pandas  (>= 0.12.0)::

    pip install pandas

Installations
=============

    pip install agstream
    

Uses cases
==========
	from agstream.session import AgspSession
	session = AgspSession()
	session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True)
	session.describe()
	for abs in session.agribases :
	    print (u"****************************************")
	    print (abs)
	    df = session.getAgribaseDataframe(abs)
	    print (df.tail())
    print(u"Fin du programme")

