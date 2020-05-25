import csv
import boto3
import json
import argparse

class Text:

    def __init__(self, bucket, photo):   
        self.bucket = bucket
        self.photo = photo

    def GetClient(self):
        with open ('credentials.csv', 'r') as input:
            next(input)
            reader = csv.reader(input)
            for line in reader:
                access_key_id = line[2]
                secret_access_key = line[3] 

        client = boto3.client('rekognition',
                aws_access_key_id = access_key_id,
                aws_secret_access_key = secret_access_key)
        return client

    def DetectText(self):
        client = self.GetClient()

        response = client.detect_text(Image={'S3Object':{'Bucket':self.bucket,'Name':self.photo}})
        
        print('Detected Text for ' + self.photo)    
        for label in response['TextDetections']:
            print (label['DetectedText'] + ' : ' + str(label['Confidence']))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--bucket", type=str, required=True,
        help="S3 bucket name")
    ap.add_argument("-p", "--photo", type=str, required=True,
        help="Photo")
    args = vars(ap.parse_args())

    obj = Text(args['bucket'], args['photo'])

    obj.DetectText()


if __name__ == "__main__":
    main()    