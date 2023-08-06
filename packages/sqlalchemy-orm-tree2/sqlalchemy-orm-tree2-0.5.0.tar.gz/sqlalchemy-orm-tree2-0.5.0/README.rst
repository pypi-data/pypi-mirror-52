.. image:: https://travis-ci.org/monetizeio/sqlalchemy-orm-tree.png?branch=master
    :target: https://travis-ci.org/monetizeio/sqlalchemy-orm-tree

.. image:: https://badge.fury.io/py/SQLAlchemy-ORM-tree.png
    :target: http://badge.fury.io/py/sqlalchemy-orm-tree

.. image:: https://coveralls.io/repos/monetizeio/sqlalchemy-orm-tree/badge.png?branch=master
    :target: https://coveralls.io/r/monetizeio/sqlalchemy-orm-tree?branch=master

SQLAlchemy-ORM-tree
-------------------

An implementation for SQLAlchemy-based applications of the nested-sets /
modified-pre-order-tree-traversal technique for storing hierarchical data
in a relational database.

==============  ==========================================================
Python support  Python 2.6+, 3.3+
SQLAlchemy      SQLAlchemy >=0.7.5, >=0.8, >=0.9
Source          https://github.com/monetizeio/sqlalchemy-orm-tree
Issues          https://github.com/monetizeio/sqlalchemy-orm-tree/issues
Docs            https://sqlalchemy-orm-tree.readthedocs.org/
API             https://sqlalchemy-orm-tree.readthedocs.org/api.html
Travis          http://travis-ci.org/monetizeio/sqlalchemy-orm-tree
Test coverage   https://coveralls.io/r/monetizeio/sqlalchemy-orm-tree
pypi            https://pypi.python.org/pypi/sqlalchemy-orm-tree
ohloh           http://www.ohloh.net/p/sqlalchemy-orm-tree
License         `BSD`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/monetizeio/sqlalchemy-orm-tree.git
install         .. code-block:: bash

                    $ pip install sqlalchemy-orm-tree

install dev     .. code-block:: bash

                    $ git clone https://github.com/monetizeio/sqlalchemy-orm-tree.git sqlalchemy-orm-tree
                    $ cd ./sqlalchemy-orm-tree
                    $ virtualenv .env
                    $ source .env/bin/activate
                    $ pip install -e .
tests           .. code-block:: bash

                    $ python setup.py test
==============  ==========================================================

.. _BSD: http://opensource.org/licenses/BSD-3-Clause


Simple Example
==============

::

    import sqlalchemy_tree
    Model = declarative_base(metaclass=sqlalchemy_tree.DeclarativeMeta)

    class Page(Model):

        # This activates sqlalchemy-orm-tree.
        __tree_manager__ = 'tree'


Page.tree.register()