import json 
import boto3 
import os
from decimal import Decimal 

client = boto3.client('rekognition')
    
dictionary_labels = dict()
labelsStore = dict()


def lambda_handler(event, context):
    record = json.loads(event['Records'][0]['body'])
    message = json.loads(record['Message'])
    records = message['Records'][0]
        
    object_key = records['s3']['object']['key']
        
    bucket_name = records['s3']['bucket']['name']
        
        
    
    dictionary_labels = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name, 
                'Name': object_key
            }
        }, MaxLabels=5) # Maximum amount of labels adhering to the brief. 
        
    for label in dictionary_labels['Labels']:
            
        label_name = label['Name']
        conf = label['Confidence']
            
        conf = Decimal(conf)
            
        labelsStore[label_name] = {"Confidence" : (conf)}
    
         
    print(dictionary_labels)
        