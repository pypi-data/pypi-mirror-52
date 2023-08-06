Overview
========

Provides functions to access HBASE. For example, connect to Hortonworks (HDP).
This package exposes the `com.ibm.streamsx.hbase` toolkit as Python methods.


Sample
======

A simple Streams application that scans a HBASE table and prints
the scanned rows::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema, StreamSchema
    from streamsx.topology.context import submit
    import streamsx.hbase as hbase

    topo = Topology('hbase_scan_sample')

    scanned_rows = hbase.scan(topo, table_name='sample', max_versions=1 , init_delay=2)
    scanned_rows.print()

    cfg = {}
    cfg[streamsx.topology.context.ConfigParams.SSL_VERIFY] = False     
    submit ('DISTRIBUTED', topo, cfg) 


Documentation
=============

* `streamsx.hbase package documentation <http://streamsxhbase.readthedocs.io/>`_


