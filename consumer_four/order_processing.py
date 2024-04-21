import pika
import pymongo
import json
from bson import ObjectId

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='order_processing_queue')

# Set up MongoDB connections
inventory_mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
inventory_db = inventory_mongo_client["inventory"]
inventory_collection = inventory_db["items"]

orders_mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
orders_db = orders_mongo_client["orders"]
orders_collection = orders_db["orders"]

# Define message handling function
def callback(ch, method, properties, body):
    # Convert the message body to a dictionary (assuming it's JSON)
    order_data = json.loads(body)
    item_id = order_data.get("item_id")
    
    # Check if item exists in inventory and quantity > 0
    item = inventory_collection.find_one({"_id": item_id, "quantity": {"$gt": 0}})
    
    if item:
        # Decrement quantity by 1
        inventory_collection.update_one({"_id": item_id}, {"$inc": {"quantity": -1}})
        
        # Insert order into orders collection
        orders_collection.insert_one(order_data)
        
        print(" [x] Order processed and inserted into MongoDB: %r" % order_data)
    else:
        print(" [x] Item with ID %s is out of stock or does not exist in inventory. Order not processed." % item_id)

# Set up message consumption
channel.basic_consume(queue='order_processing_queue',
                      on_message_callback=callback,
                      auto_ack=True)

# Start consuming messages
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# Close connections
connection.close()
inventory_mongo_client.close()
orders_mongo_client.close()
