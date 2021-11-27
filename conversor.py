import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys
import requests
import pandas as pd

aws_access_key_id = "ASIA5SZMNHBQP24ETYU3"
aws_secret_access_key = "R8u/+X3LBPJX4I9POW+bXh2EBm66jHWFzhr1TK0D"
aws_session_token = "FwoGZXIvYXdzEOD//////////wEaDD9nrfooHhY1iK4kqSLGAetNx6q0l2HqXpXN4mfiv7wv0nxskRwE8snU/JcgfNUeOsc5fi7eokHcl2uYvPVnjVDJydH9ggqhsfW3V6Cnm51XB3eWbsne3JlldNKN23r9dpkI3jEYcoIxXeyydosLK36Ny/fkDQb3zQ98xaEKxHi6fYHFKKezxxd2lfv/djfkw2yh9N5lgyOtgkLDZozV6FxD69Dy15IKdtRgqeqkG7+TFOC//IJP+2K1CX0jXO3BgKTIcpFE+L+DABxH9w6sfT2wxqtZ/Cjut4WNBjItl3VOjFCEYdV0g0prsnOyqRjooZlRsPlx5H3flW89I/cAjfSv1gZgHC4f7/gG"
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
