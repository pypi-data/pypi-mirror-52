.. MorpFramework documentation master file, created by
   sphinx-quickstart on Sat Sep 22 18:36:43 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=========================================
Welcome to MorpFramework's documentation!
=========================================

Introduction
===============

Morp is a python web development framework for developers who need a framework
that provides some assistance in building applications that support distributed
processing. Other web frameworks are primarily designed for standard wsgi
processing, while distributed worker processing is primarily a feature that is
added as a plugin, Morp is different in this sense because we try to make it a
first class citizen of the framework.

Morp, built on top of Morepath, provides a highly extensible
framework which supports:

 * REST API framework

   * `JSL <https://jsl.readthedocs.io/>`_ schema model definition 
     (deprecated, to be ported to Avro/JSONObject)
   * CRUD endpoints
   * Search endpoint, powered by `rulez
     <https://github.com/morpframework/rulez>`_ query
   * Aggregation endpoint
   * State machine / transition engine powered by `pytransitions
     <https://github.com/pytransitions/transitions>`_
   * Soft delete 

 * Modular storage engine

   * `SQLAlchemy <http://www.sqlalchemy.org/>`_ (primary)
   * `Elasticsearch <https://www.elastic.co/>`_

 * Authentication engine

   * JWT token with refresh support
   * Pluggable authentication system

 * Authorization engine

   * Group & role management

 * Distributed processing & task scheduling

   * Powered by `celery <http://www.celeryproject.org/>`_
   * Future plan to support `Streamparse <http://www.celeryproject.org/>`_

 * Plugin based architecture

   * Powered by `morepath <https://morepath.readthedocs.io>`_, `dectate
     <https://dectate.readthedocs.io>`_ and `reg <https://reg.readthedocs.io>`_

.. note:: Morp at the moment is still highly experimental, there is no promise of

Documentation
==============

.. toctree::
   :maxdepth: 2

   usingmorpfw



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
