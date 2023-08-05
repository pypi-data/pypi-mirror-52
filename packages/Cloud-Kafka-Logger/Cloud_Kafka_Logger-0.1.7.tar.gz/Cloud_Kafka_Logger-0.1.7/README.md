
# Kafka Package

This is a simple package which sends log messages to Cloud Kafka Topic.

# Version

Python == 3.X

# Dependency 

confluent-kafka>=0.11.6

# Installation

Run the following to install

pip install cloud-kafka-logger

# Usage

import logging

from cloudKafkaLogger import KafkaHandler

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

conf = {
    
    'bootstrap.servers': 'cloud-kafka-servers',
    
    'session.timeout.ms': 6000,
    
    'default.topic.config': {'auto.offset.reset': 'smallest'},
    
    'security.protocol': 'your-protocol',
    
    'sasl.mechanisms': 'your-mechanisms',
    
    'sasl.username': 'your-username',
    
    'sasl.password': 'your-password'

}

kh = KafkaHandler(conf=conf, topic='your-topic')

logger.addHandler(kh)

# This will be written into Kafka Topic
logger.info(json.dumps({"app_name": "Test_Python_App", "message": "Am logging from application"}))