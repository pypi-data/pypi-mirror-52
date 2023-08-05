=====
Usage
=====

To use pyoadr-ven in a project::

    import pyoadr_ven

This will import the OpenAdrVENAgent class.

Register VEN
------------
If you don't have a `ven_id`, you will need to register your VEN with the VTN.  To do this call the `register` function on an initialised agent:

.. code-block:: python

    from pyoadr_ven import OpenADRVenAgent
    agent = OpenADRVenAgent(
        vtn_address="http://openadr-vtn-server.local",
        client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
        vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
        # There are more parameters but you should consult the docs for these.
        # The above ones are the minimum necessary for registration.
    )
    response = agent.register(ven_name="name_of_ven")
    # > print(response)
    # {
    #     "vtn_id": "CC_VTN",
    #     "ven_id": "09384134-1340983314",
    #     "poll_interval_secs": 40,
    # }

These values should be stored somewhere safe (i.e. persistent) and passed along to the agent instance on future initialisations.


Pre-Registered VEN
------------------
If you already know the `ven_id`, initialize an `OpenAdrVENAgent` with it:

.. code-block:: python

    agent = OpenADRVenAgent(
        ven_id="ven_id",
        vtn_id="vtn_id",
        vtn_address="http://openadr-vtn-server.local",
        poll_interval_secs=15,
        log_xml=True,
        opt_timeout_secs=3,
        opt_default_decision="optIn",
        client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
        vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
    )

The first thing you are likely to want to do is get all of the existing events that are on the VTN.

.. code-block:: python

    agent.request_events()

This will return all of the events that are on the server and addsthem to the agent's database.
This should be done once.

Then, in a long running loop, periodically run:

.. code-block:: python

    agent.tick()

