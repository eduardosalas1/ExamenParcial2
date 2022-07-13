from abc import ABC, abstractmethod
from typing import List
import pika
import sys

class Publisher(ABC):
    
    @abstractmethod
    def attach(self, observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass



class ClientPublisher(Publisher):

    _state: int = None
    
    _suscribers = []
    
    def attach(self, observer) -> None:
        self._suscribers.append(observer)

    def detach(self, observer) -> None:
        self._suscribers.remove(observer)


    def notify(self) -> None:
        
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='nuevo')

        message = ' '.join(sys.argv[1:]) or "info: Hello World!"
        channel.basic_publish(exchange='', routing_key='nuevo', body=message)
        print(" [x] Mensaje Enviado !", message)
        connection.close()

def main():

    publisher = ClientPublisher()
    publisher.notify()

main()
