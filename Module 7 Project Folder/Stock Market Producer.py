"""
    This program monitors whichever stock you choose and sends the changing
    prices to the queue.

    Author: Ryan Shaw
    Date: February 27, 2023

"""

import pika
import sys
import webbrowser
import csv
import time

stocks = {'ABCD': '$3.65', 'CAKE': '$3.42', 'EMF': '$13.25', 'FAST': '$0.06', 'GLAD': '$17.20', 'HAWK': '$0.12', 'JACK': '$7.50', 'LCUT': '$6.59', 'MOMO': '$13.80', 'TRIP': '$24.00' }


def offer_stocks():

    print("Current stocks are: ")

    for key in stocks:

        
        print(f'Stock: {key} Price: {stocks[key]}' )

    while True:
        chosen_stock = input("What stock would you like to monitor?")
        email = input("What email address would you like to receive notifications at?")

        try:
            chosen_stock.upper() in stocks
        
        except:
            print("That was not a valid stock. Please enter one of the listed stocks.")
            
            continue

        break

    return chosen_stock, email





    

    

def send_message(host: str, queue_name: str, message: str):
    
    

    
    

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message}")
    except KeyboardInterrupt:
        print()
        print(" User interrupted process.")
        sys.exit(0)
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)

    finally:
        # close the connection to the server
        conn.close()

# Opens CSV file and cycles through it while skipping the header row
if __name__ == "__main__":
    
    chosen_stock, email = offer_stocks()

    with open(f'{chosen_stock}.csv', "r") as import_file:
        reader = csv.reader(import_file, delimiter=',')
        next(reader, None)
    
    
    

        for row in reader:
    
        
            if __name__ == "__main__":  

            
                print("To exit press CTRL+C")
        
                date, low, open, volume, high, close, adjusted_close = row

            
        
                csv_data = (date, low[0:4], open[0:4], volume[0:4], high[0:4], close[0:4], adjusted_close[0:4], chosen_stock, email)

            
            

                stock_message = ' '.join(csv_data)

                

    

        
        # send the messages to the queue
        # prints the messages to indicate success
                send_message("localhost","01-stock",stock_message.encode())
                print(f'Sent {stock_message} to 01-stock queue.')
                time.sleep(60)
        
