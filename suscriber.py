from abc import ABC, abstractmethod
import queue
from typing import List
import pika,sys,os

class Suscriber(ABC):


    @abstractmethod
    def update(self, subject) -> None:
        pass


class ClientSuscriber(Suscriber):
    def update(self) -> None:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
    
        channel.queue_declare(queue='nuevo')
    
        def callback(ch, method, properties, body):
            print(" [x] Mensaje recibido !! %r" % body)
    
        channel.basic_consume(queue='nuevo', on_message_callback=callback, auto_ack=True)
    
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


def main():

    suscriber = ClientSuscriber()
    suscriber.update()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)