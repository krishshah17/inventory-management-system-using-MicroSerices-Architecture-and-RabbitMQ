import pika
import pymongo
import json
from bson import ObjectId

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='stock_management_queue')

# Set up MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["inventory"]  # Assuming 'inventory' is the name of the database
collection = db["items"]  # Assuming 'items' is the name of the collection

def callback(ch, method, properties, body):
    # Convert the message body to a dictionary (assuming it's JSON)
    message_data = json.loads(body)
    
    # Update stock level in MongoDB collection
    item_id = message_data.get("item_id")
    new_stock_level = message_data.get("new_stock_level")
    
    # Update stock level for the item in the MongoDB collection
    collection.update_one({"_id": item_id}, {"$set": {"quantity": new_stock_level}})
    
    print(" [x] Stock level updated for item with ID %s. New stock level: %d" % (item_id, new_stock_level))

# Set up message consumption
channel.basic_consume(queue='stock_management_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# Close connections
connection.close()
mongo_client.close()
