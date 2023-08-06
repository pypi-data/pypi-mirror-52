Messaging queue library for the LHCb continuous integration system
==================================================================

Description
-----------

This python module contains an implementation of the interface to rabbitmq for the LHCb Nightly builds.

It relies on RabbitMQ priority queues to handle commands sent in the right order.

The files are the following:
* Common.py: Common tools to interface with the queue...
* CvmsfsDevExchange.py: methods to send and receive messages

Usage
-----
* With services

![Service construction architecture](http://lbinstall.web.cern.ch/lbinstall/Lbmessagin.jpg)

As described in the figure above, multiple exchanges are mapped to different services dynamically. 

The user can use this services in order to use different functionalities of the exchanges via the mapped methods. A description of the methods mapping is found in each of the service source code. 

To send a command to a queue, you need to create an instance of the CVMFSNightliesService and then call the *_send methods depending on your destination (dev\_send, prod\_send, condb\_send)

```python

from lbmessaging.CvmfsDevExchange import CvmfsDevExchange

# Send a command 
srv = CVMFSNightliesService(vhost='/lhcb-test')
srv.dev_send("mycommand", [ "args1", "args2")

# Receive a command
command_message = srv.dev_receive(QUEUE_NAME)
command = command_message.body.command)
args = command_message.body.arguments)
```

* With exchanges

To send a command to the queue, you need to create a connection to RabbitMQ using the get_connection
utility and create a 

```python

from lbmessaging.services.CVMFSNightliesService import CVMFSNightliesService

with get_connection() as connection:
    broker = CvmfsDevExchange(connection)
    broker.send_command("mycommand", [ "args1", "args2"] )

```

The *priority* (integer between 0 and 255) and *retry_count* arguments dictate the policies for handling and retrying 
the command.

To receive

```python

from lbmessaging.exchanges.CvmfsDevExchange import CvmfsDevExchange
from lbmessaging.exchanges.Common import get_connection

with get_connection() as connection:
    broker = CvmfsDevExchange(connection)
    message = broker.receive_command()
    (command, args, command_date) = message.body 

```


Handling errors
---------------

In case of error, the method *handle_processing_error* should be used.
It either retries the command  by putting it back into the queue, or sends to an error queue if the number of max retry 
been reached.

c.f. TestCommand.py for an example.


Notes
---------------

Provision a new instance of RabbitMQ can be done using LHCbProvisionRabbitMQ.sh

TODO: Document configuration for the RabbitMQ connection 




