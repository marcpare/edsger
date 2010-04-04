About
=====

edsger is a web service to evaluate mathematical expressions. On the back end is an implementation of the [Shunting-Hall](http://en.wikipedia.org/wiki/Shunting-yard_algorithm) algorithm. It's named edsger because Edsger Dijkstra came up with the algorithm.

Installation
============

edsger was written for Python 2.5. Other versions should work alright.

Design and Implementation
=========================

A straightforward implementation of the Shunting-Hall algorithm powers edsger. Expression evaluation is efficient as a result. 

Cool stuff:

* Unary minuses stack correctly. (Try '5-----6', for example)
* Error messages are lucid, for the most part.
* Operators are abstracted, allowing more to be added in the future. This was nice when I realized that I hadn't implemented negative numbers at the last minute.
* Lots of unit tests. Run them using [nosetests](http://somethingaboutorange.com/mrl/projects/nose/0.11.3/), if you like.

Limitations

* Assumes you never want to do integer division.
* Complex numbers aren't included.
* Tokenizing of the input expression relies on string splitting. To handle really long input expressions efficiently, this would have to be changed.
* Overflow is considered an error. 

Deployment of the web service
=============================

edsger can be deployed as a JSON web service using [Bottle](http://github.com/defnull/bottle). There is a little HTML console included to demonstrate its usage in AJAX, as well.

Bottle exposes the app using WSGI, so it could be plugged into any WSGI compatible multi-threaded Python serve (like gunicorn, cherryPy, fapws3, ...)