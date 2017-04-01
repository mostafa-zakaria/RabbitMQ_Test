import pika, os, logging, time, json
logging.basicConfig(filename = "example_consumer.log", level=logging.DEBUG)

def processFunction(msg):
  print( "[*]Message Received> Processing")
  time.sleep(2) # delays for 2 seconds
  print("Received> {}".format(json.loads(msg)['test']))
  return;

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  if(type(body) != bytes):
    processFunction(body)
  else:
    processFunction(body.decode('utf-8'))
  ch.basic_ack(delivery_tag = method.delivery_tag)

# Parse CLODUAMQP_URL (fallback to localhost)
params = pika.URLParameters("amqp://xcavtrsf:Z0ddLX0_IsuW_JjNRG8MVUq2XeuL15PW@penguin.rmq.cloudamqp.com/xcavtrsf")
params.socket_timeout = 2
params.heartbeat_interval = 1
params.connection_attempts = 10

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel

#set up subscription on the queue
channel.basic_consume(callback,
  queue='HelloQ',
  no_ack=True)

# start consuming (blocks)
print("[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
connection.close()
