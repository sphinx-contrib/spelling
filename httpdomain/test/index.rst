.. module:: sphinxcontrib.httpdomain

:mod:`sphinxcontrib.httpdomain` --- Documenting RESTful HTTP APIs
=================================================================

Directives
~~~~~~~~~~

.. http:patch:: /users/(int:user_id)/posts/(tag)
.. http:options:: /users/(int:user_id)/posts/(tag)
.. http:get:: /users/(int:user_id)/posts/(tag)
.. http:head:: /users/(int:user_id)/posts/(tag)
.. http:post:: /users/(int:user_id)/posts/(tag)
.. http:put:: /users/(int:user_id)/posts/(tag)
.. http:delete:: /users/(int:user_id)/posts/(tag)
.. http:trace:: /users/(int:user_id)/posts/(tag)
.. http:connect:: /users/(int:user_id)/posts/(tag)

Sourcecode
~~~~~~~~~~

.. sourcecode:: http

   GET /users/123/posts/web HTTP/1.1
   Host: example.com
   Accept: application/json, text/javascript

.. sourcecode:: http

   HTTP/1.1 200 OK
   Vary: Accept
   Content-Type: text/javascript

   [
     {
       "post_id": 12345,
       "author_id": 123,
       "tags": ["server", "web"],
       "subject": "I tried Nginx"
     },
     {
       "post_id": 12346,
       "author_id": 123,
       "tags": ["html5", "standards", "web"],
       "subject": "We go to HTML 5"
     }
   ]

Resource fields
~~~~~~~~~~~~~~~

.. http:get:: /foo

   :query resource: description for ``resource``
   :statuscode 200: description for 200
   :statuscode 404: description for 404

Roles
~~~~~

Referring to existing directives
................................

:http:patch:`/users/(int:user_id)/posts/(tag)`

:http:options:`/users/(int:user_id)/posts/(tag)`

:http:get:`/users/(int:user_id)/posts/(tag)`

:http:head:`/users/(int:user_id)/posts/(tag)`

:http:post:`/users/(int:user_id)/posts/(tag)`

:http:put:`/users/(int:user_id)/posts/(tag)`

:http:delete:`/users/(int:user_id)/posts/(tag)`

:http:trace:`/users/(int:user_id)/posts/(tag)`

:http:connect:`/users/(int:user_id)/posts/(tag)`

Method roles
............

:http:method:`patch`

:http:method:`options`

:http:method:`get`

:http:method:`head`

:http:method:`post`

:http:method:`put`

:http:method:`delete`

:http:method:`trace`

:http:method:`connect`
