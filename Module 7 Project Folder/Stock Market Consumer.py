"""
    This program listens for work messages contiously. 
    Monitoring the changing stock prices. I included my attempt at sending
    an email notification. Unfortunately it does not work. I think if I had more
    time, I could have figured it out. 

    Author: Ryan Shaw
    Date: February 27, 2023

"""

import pika
import sys
import time
from collections import deque
import smtplib


#Declares smoker deque
stocks_deque = deque(maxlen = 1000)
buy_percentage = 20
sell_percentage = 20
stock_email = 'nova1008@hotmail.com'
password = 'mbotf1008'
#server = smtplib.SMTP('smtp.mail.yahoo.com', 465)




# define a callback function to be called when a message is received
def stocks_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""

    #server.starttls
    #server.login(stock_email, password)
        #Adds incoming message to deque after decoding it.
    stocks_deque.append(body.decode())

    current_stocks = body.decode()

    stocks_initial_price = stocks_deque[0][16:20]
    
    stock_date = current_stocks[0:10]

    stock_low_price = current_stocks[11:15]

    stock_open_price = current_stocks[16:20]

    stock_volume = current_stocks[21:25]

    stock_high_price = current_stocks[26:30]

    stock_close_price = current_stocks[31:35]

    stock_adjusted_close_price = current_stocks[36:40]

    stock_name = current_stocks[41:45]

    email = current_stocks[46:]

    print(f'Date: {stock_date}, Open Price: ${stock_open_price}')

    if float(stock_open_price) <= ((buy_percentage/100) * float(stocks_initial_price)):
        print(f"Your stock {stock_name} is at a reasonable price. You should consider buying.")
        #Attempt at email notification. Comment out this line to see the rest of the code at work.
        #server.sendmail(stock_email, email, f"Your stock {stock_name} is at a reasonable price. You should consider buying." )
        

    if float(stock_open_price) >= ((sell_percentage/100) * float(stocks_initial_price)):
        print(f"Your stock {stock_name} price has gone up a considerable amount. You should consider selling it.")
 
    # decode the binary message body to a string
    #print(f" [x] Received {body.decode()}")
    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)


    



# define a main function to run the program
def main(hn: str, qn: str):
    """ Continuously listen for task messages on a named queue."""
    
    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:

        
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=qn, durable=True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume( queue=qn, on_message_callback=stocks_callback)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    
    

    # call the main function with the information needed
    main("localhost", "01-stock")
