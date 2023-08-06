GD-rabbitMQ
---
**Right now this package is only for ```greendeck's``` internal use. This will help to publish and consume messages with your rabbitMQ**

![Greendeck](https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/gd_transparent_blue_bg.png)  ![RabbitMQ](https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/rabbitmq.png)
### Install from pip
https://pypi.org/project/greendeck-rabbitmq/

```pip install greendeck-rabbitmq```

Read details about all default parameters and core functions here in RabbitMQ official website. (https://www.rabbitmq.com)


### How to use ?
##### import the library
```python
import greendeck_rabbitmq
```

##### import ```RabbitMQ``` class
```python
from greendeck_rabbitmq import RabbitMQ
```

##### initialize ```RabbitMQ``` client connection

Here default values of some arguments are 
* RMQ_PORT=5672
* RMQ_VHOST='/'
* username=Null
* password=Null


```python
from greendeck_rabbitmq import RabbitMQ

# declare variables
RMQ_HOST = <YOUR_RMQ_HOST>  # RabbitMQ host address
RMQ_PORT = <YOUR_RMQ_PORT>  # RabbitMQ port
RMQ_VHOST = <YOUR_RMQ_VHOST>  # RabbitMQ virtual host 
username = <YOUR_USERNAME>  # RabbitMQ username
password = <YOUR_PASSWORD>  # RabbitMQ password

```Here default values are RMQ_PORT=5672, RMQ_VHOST='/', username=Null, password=Null```

rabbitmq_client = RabbitMQ(RMQ_HOST, RMQ_PORT, RMQ_VHOST = RMQ_VHOST, username = username, password = password)

```


##### close ```RabbitMQ``` client connection
```python
rabbitmq_client.rabbitmq_close_connection()
```
##### check size of a rabbitmq queue
```python

queue = "test_library"
print(rabbitmq_client.size(queue))
```
##### check if a size of queue is empty or not
```python

queue = "test_library"

print(rabbitmq_client.is_empty(queue))
```

##### consume all messages of a queue
```python
queue = "test_library"
rabbitmq_client.rabbitmq_get_all(queue)

```

##### single message producer

Here default parameters and their values are:
* exchange=""
* delivery_mode=2
* mode="single"

```python
message = "hello world"
queue = "test_library"
routing_key = "test_library"
exchange = ''
delivery_mode = 2
mode = "single"

```The routing key is a message attribute. The exchange might look at this key when deciding how to route the message to queues (depending on exchange type). ```
``` delivery mode = 1 means non persistent, and delivery mode = 2 means persistent```

```available modes are 'single' & 'multi' and in 'multi' mode it expects message as list of messages

rabbitmq_client.rabbitmq_publisher(message, queue, routing_key, exchange = exchange, delivery_mode = delivery_mode, mode = mode)
rabbitmq_client.rabbitmq_close_connection()
```

##### multi messages producer

Here default parameters and their values are:
* exchange=""
* delivery_mode=2
* mode="single"

```python
message = ["hello world"] * 100  #list of messages
queue = "test_library"
routing_key = "test_library"
exchange = ''
delivery_mode = 2
mode = "multi"

rabbitmq_client.rabbitmq_publisher(message, queue, routing_key, exchange = exchange, delivery_mode = delivery_mode, mode = mode)
rabbitmq_client.rabbitmq_close_connection()
```

##### messages consumer
Here default parameters and their values are:
* size=1

```python
queue = "test_library"
size = 1 # mention number of required messages

results = rabbitmq_client.rabbitmq_consumer(queue, size)
print("number of messages", len(results))
rabbitmq_consumer.rabbitmq_close_connection()

```

##### create an exchange
This will create an exchange and bind the list of queues to the same exchange.
Default arguments and their values are:
* exchange_type = "fanout"
* routing_key = ""


```python
exchange = "test_exchange"
queues = ["queue1", "queue2", "queue3"]
exchange_type = "fanout" # for now exchange_type only supports 'fanout'
routing_key = "" # make sure to keep this one same in your project for easy use

```Here default arguments are exchange_type="fanout", routing_key=""```

rabbitmq_client.make_rabbitmq_exchange(exchange, queues, exchange_type=exchange_type, routing_key=routing_key)

```

##### produce single message to an exchange
Produce a single message to an exchange

Default arguments and their values are:
* exchange_type = "fanout"
* routing_key = ""
* mode = "single"

```python
exchange = "test_exchange"
message = "hello" 
exchange_type = "fanout"
routing_key = ""
mode = "single"

``` Here avilable modes are single or multi . When it is in multi mode it expects type of message field as list```

rabbitmq_client.rabbitmq_exchange_publisher(exchange ,message, exchange_type=exchange_type, routing_key=routing_key,
                                            mode=mode)

```

##### produce single message to an exchange
Produce a single message to an exchange

Default arguments and their values are:
* exchange_type = "fanout"
* routing_key = ""
* mode = "single"

```python
exchange = "test_exchange"
message = ["hello1", "hello2", "hello3"] 
exchange_type = "fanout"
routing_key = ""
mode = "multi"

``` Here avilable modes are single or multi . When it is in single mode it expects type of message field as a string```

rabbitmq_client.rabbitmq_exchange_publisher(exchange ,message, exchange_type=exchange_type, routing_key=routing_key,
                                            mode=mode)

```

---
How to build your pip package

* open an account here https://pypi.org/

In the parent directory
* ```python setup.py sdist bdist_wheel```
* ```twine upload dist/*```

Update your package
* ```python setup.py sdist```
* ```twine upload dist/*```

references
* https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5
* https://packaging.python.org/tutorials/packaging-projects/RabbitMQ

# Thank You