Installation of the application can be completed by running
shell script named ``setup.sh``::

  chmod +x setup.sh
  ./setup.sh

Alternatively, you can run each command manually:

.. includesh:: setup.sh


And you're down with installation. Next phase is to change
the configuration::

1. Place the initial configuration in ``/etc/app.conf``
2. Open the config in editor and change as needed::
  
     vim /etc/app.conf
     
     
   .. includesh:: app.conf
      :start-after: <changethese>
      :end-before:  </changethese>
      
      
3. After finished, start the service::
  
     /etc/init.d/app start
    

