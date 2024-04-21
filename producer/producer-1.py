from flask import Flask, render_template, request
import pika
import json
import atexit

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='health_check_queue')
channel.queue_declare(queue='item_creation_queue')
channel.queue_declare(queue='stock_management_queue')
channel.queue_declare(queue='order_processing_queue')

def produce_message(message):
    channel.basic_publish(exchange='',
                          routing_key='health_check_queue',
                          body=message)
    print(" [x] Sent %r" % message)

def create_item(message):
    channel.basic_publish(exchange='',
                          routing_key='item_creation_queue',
                          body=json.dumps(message))
    print(" [x] Sent %r" % message)

def update_stock(message):
    channel.basic_publish(exchange='',
                          routing_key='stock_management_queue',
                          body=json.dumps(message))
    print(" [x] Sent %r" % message)

def place_order(message):
    channel.basic_publish(exchange='',
                          routing_key='order_processing_queue',
                          body=json.dumps(message))
    print(" [x] Sent %r" % message)

# Define routes for Flask application
@app.route('/health-check')
def health_check():
    return render_template('health_check.html')

@app.route('/create-item')
def create_item_route():
    return render_template('create_item.html')

@app.route('/update-stock')
def update_stock_route():
    return render_template('update_stock.html')

@app.route('/place-order')
def place_order_route():
    return render_template('place_order.html')

@app.route('/create-item', methods=['POST'])
def create_item_post():
    item_data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "price": float(request.form['price']),
        "quantity": int(request.form['quantity'])
    }
    create_item(item_data)
    return 'Item created successfully.'


@app.route('/update-stock', methods=['POST'])
def update_stock_post():
    item_data = {
        "item_id": request.form['item-id'],
        "new_stock_level": int(request.form['new-stock-level']),
    }
    update_stock(item_data)
    return 'Item updated successfully.'

@app.route('/place-order', methods=['POST'])
def plcae_order_post():
    item_data = {
        "item_id": request.form['item-id'],
        "customer_name": request.form['customer-name'],
        "quantity": int(request.form['quantity']),
    }
    place_order(item_data)
    return 'Item updated successfully.'


def close_connection():
    connection.close()

atexit.register(close_connection)

if __name__ == '__main__':
    app.run(debug=True,port=8001)
