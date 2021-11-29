import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys
import requests
import pandas as pd

aws_access_key_id = "ASIA5SZMNHBQMXOYWEPK"
aws_secret_access_key = "vo5tw51FmTh2zGCZLX/imYlAhMkjP81qsYQpdCd2"
aws_session_token = 'FwoGZXIvYXdzEBoaDK/eCUkek8v4gQb4fiLGAcRmQcuhBintCB3cN4NI9eRMBuk7HBAFWhCjCAuWWb243Pc1rMTnOR+yPqqvXXQI2FjDbRzvg7fIjP2eSb79HpOUBlj19VMIgPy2CKfVH//Cem136t8Li9icD2LJ00EExIvOOeNZ66xNXn9wA50hl2eL+Sm9WUEC9n+xUrCXQKYucqXLXj0Tgp6oAZiw4mlsRo569GmhQB7hW/+6sThPp6uBi6LOJfRxAi+rh/L4tMl0+1Xm2m79Q0sZNrMpT3I+ntTAQRaEtSi1qJKNBjItNgdYNWqjEHub1Xdzl3TcpwaDbbimadbNz0UXYr5xItXllOe9egSRs4VJqVcv'
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


def stream(title):
    slc = len(title)
    my_bucket = S3.Bucket(name='articles-1')
    for i in my_bucket.objects.all():
        if f'{title}' == i.key[:slc]:
            
            return Stream(s3.generate_presigned_url(
                                ClientMethod="get_object",
                                ExpiresIn=3600,
                                HttpMethod='GET',
                                Params={
                                    "Bucket": "articles-1",
                                    "Key": f"{i.key}",
                                }))
    return False
