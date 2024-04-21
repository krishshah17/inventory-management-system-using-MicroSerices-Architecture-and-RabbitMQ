import pika
import pymongo
import json

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='item_creation_queue')

# Set up MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["inventory"]  # Assuming 'inventory' is the name of the database
collection = db["items"]  # Assuming 'items' is the name of the collection

def callback(ch, method, properties, body):
    # Convert the message body to a dictionary (assuming it's JSON)
    message_data = json.loads(body)
    item_name = message_data.get("name")
    message_data["_id"] = item_name
    
    
    # Insert item into MongoDB collection
    collection.insert_one(message_data)
    
    print(" [x] Item created and inserted into MongoDB: %r" % message_data)

# Set up message consumption
channel.basic_consume(queue='item_creation_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# Close connections
connection.close()
mongo_client.close()
