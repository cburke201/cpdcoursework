import json 
import boto3 
import os

client = boto3.client('rekognition')
    
#used to create a python dictionary for it to be stored in the database
dictionary_ppe = dict()

def lambda_handler(event, context):
    try:
        print(event.get("Message"))
        print(event.get("body"))
        print(event.get('Records'))
        record  = json.loads(event['Records'][0]['body'])
        message = json.loads(record['Message'])
        records = message['Records'][1]
        
        object_key = records['s3']['object']['key']
        
        bucket_name = records['s3']['bucket']['name']
    
        dictionary_ppe = client.detect_protective_equipment(Image={'S3Object':{'Bucket': bucket_name,'Name': object_key}},
        SummarizationAttributes={
            'MinConfidence': 0.70,
            'RequiredEquipmentTypes': [
                'FACE_COVER', 'HAND_COVER',
            ]
        })
        
        
        not_wearing = dictionary_ppe['Summary']['PersonsWithoutRequiredEquipment']
        
        indeterminate = dictionary_ppe['Summary']['PersonsIndeterminate']
        
        print(dictionary_ppe)
        
        print(not_wearing)
        # if one of the images is flaged a message will be sent. 
        #if (not_wearing):
            #print("Sending SMS")
            #send_message(object_key)
        #elif(indeterminate):
            #print("Unreconised Equipment")
        #else:
            #print("all good to start working")
    except KeyError:
        print("error")        