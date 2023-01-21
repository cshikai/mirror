from confluent_kafka import Producer
import json
import socket


class KafkaManager():

    def __init__(self, config):
        self.url = config['KAFKA']['URL']
        self.topic = config['KAFKA']['TOPIC']
        self.producer_config = {'bootstrap.servers': self.url,
                                'client.id': socket.gethostname()}
        self.producer = Producer(self.producer_config)

    def receipt(self,err,msg):
        if err is not None:
            print('Error: {}'.format(err))
        else:
            message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
            print(message)
    
    def enqueue_kafka(self, es_id, queue):
        data = {'es_id': es_id}
        data_str = json.dumps(data)
        self.producer.produce(queue, data_str.encode('utf-8'), callback=self.receipt)
        self.producer.flush()
