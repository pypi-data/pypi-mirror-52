DDD Nginx Framework
===================

|Build Status| |Pypi Status| |Coveralls Status|

Installation
------------

From source code:

::

    python setup.py install

From pypi:

::

    pip install ddd-base

Usage
-----

::

    from ddd_nginx.nginx import Nginx
    from ddd_nginx.map import Map, MapKeyParis, MapDefinition
    from ddd_nginx.server import Server
    from ddd_nginx.location import Location, ReverseProxyStrategy
    from ddd_nginx.upstream import Upstream


    nginx = Nginx(host="oneapi.cc")
    nginx.namespace = "api"

    a_map = Map(MapDefinition(key="$http_apikey", value="$api_client_name"))
    a_map.append(MapKeyParis("7B5zIqmRGXmrJTFmKa99vcit", "client_one"))
    a_map.append(MapKeyParis("QzVV6y1EmQFbbxOfRCwyJs35", "client_two"))
    a_map.append(MapKeyParis("mGcjH8Fv6U9y3BVF9H3Ypb9T", "client_six"))

    a_upstream = Upstream(name="warehouse_inventory")
    a_upstream.append("10.0.0.1:80")
    a_upstream.append("10.0.0.2:80")
    a_upstream.append("10.0.0.3:80")

    b_upstream = Upstream(name="warehouse_pricing")
    b_upstream.append("10.0.0.1:80")
    b_upstream.append("10.0.0.2:80")
    b_upstream.append("10.0.0.3:80")

    a_location = Location(
        name="/api/warehouse/inventory",
        proxy=ReverseProxyStrategy('rewrite', '^ /_warehouse last')
    )
    a_location.set_var("$upstream", "warehouse_inventory")
    b_location = Location(
        name="/api/warehouse/pricing",
        proxy=ReverseProxyStrategy('rewrite', '^ /_warehouse last')
    )
    b_location.set_var("$upstream", "warehouse_pricing")
    c_location = Location(
        name="= /_warehouse",
        proxy=ReverseProxyStrategy('proxy_pass', 'http://$upstream$request_uri'),
        scope="internal"
    )
    c_location.set_var("$api_name", "Warehouse")

    a_server = Server(name=nginx.namespace)
    a_server.set_var("$api_name", "-")

    nginx.append(a_map)
    nginx.append(a_upstream)
    nginx.append(b_upstream)
    nginx.append(a_location)
    nginx.append(b_location)
    nginx.append(c_location)
    nginx.append(a_server)

    root_dir = "./dumps_dir"
    nginx.dumps(root_dir)



License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/sunwei/ddd-base/blob/master/LICENSE>`_

.. |Build Status| image:: https://travis-ci.com/sunwei/ddd-nginx.svg?branch=master
   :target: https://travis-ci.com/sunwei/ddd-nginx
.. |Pypi Status| image:: https://badge.fury.io/py/ddd-nginx.svg
   :target: https://badge.fury.io/py/ddd-nginx
.. |Coveralls Status| image:: https://coveralls.io/repos/github/sunwei/ddd-nginx/badge.svg?branch=master
   :target: https://coveralls.io/github/sunwei/ddd-nginx?branch=master
