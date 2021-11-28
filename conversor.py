import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys
import requests
import pandas as pd

aws_access_key_id = "ASIA5SZMNHBQDSMEWIVN"
aws_secret_access_key = "pyHEiwkqLjrjpBxDJpoSRxobEHsykL3zQgsEBm9r"
aws_session_token = 'FwoGZXIvYXdzEA0aDAqZeq6qtUbOWxBytCLGAZhnWXIFte1t9/18QEA6Pwx9X907s0DNum+bd/3Z0OFT9+8U91Ck35BUOnZuIz2LMDGRD9OAdQCkLmZbb82bBiNyi3QnVOT28tEQSFBBp6wNSZeduhRrhyYyi4TR8nPkE83SKeOhV+OcQamS5jjtEYZf7m39wOG0M29sfxOLDuG8W3igBVOKVmo9A9wE437QV+vTH5CLFj0+IonxYxACqL0tLp3rmZ5J2aJ49wW7v2+VTqWqyo4xnTVvUOnx6uPEXQ/8d6H06CjvrY+NBjItA+Ff1mJgMNhqT7UkkOJkc5IBb3hKcbykN0FYbbVaWkBpaPUdu38o55hDzOne'
session = boto3.Session(region_name='us-east-1',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        aws_session_token=aws_session_token)

polly = boto3.client("polly",
                     region_name='us-east-1',
                     aws_access_key_id=aws_access_key_id,
                     aws_secret_access_key=aws_secret_access_key,
                     aws_session_token=aws_session_token)
s3 = boto3.client('s3', region_name='us-east-1',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  aws_session_token=aws_session_token)

S3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

articles = s3.get_object(Bucket= 'articles-1', Key='csv/articles.csv')


class Stream(object):

    def __init__(self, url):
        self._file = requests.get(url, stream=True)

    def read(self, *args):
        if args:
            return self._file.raw.read(args[0])
        else:
            return self.file.raw.read()

    def close(self):
        self._file.close()

def convert_to_speech(text, title):
    try:
        polly.start_speech_synthesis_task(OutputS3KeyPrefix=title, Text=text, OutputFormat="mp3", VoiceId="Matthew",
                                          OutputS3BucketName='articles-1')
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)


def stream(index):
    my_bucket = S3.Bucket(name='articles-1')
    for i in my_bucket.objects.all():
        if f'{index}' == i.key[:2]:
            
            return Stream(s3.generate_presigned_url(
                                ClientMethod="get_object",
                                ExpiresIn=3600,
                                HttpMethod='GET',
                                Params={
                                    "Bucket": "articles-1",
                                    "Key": f"{i.key}",
                                }))
    return False
