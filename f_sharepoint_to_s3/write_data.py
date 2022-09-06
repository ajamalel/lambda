import boto3
from io import StringIO, BytesIO
import pandas as pd
import xlsxwriter

def df_to_s3(df,bucket_name,folder_path,zone,country,datetime):

    with BytesIO() as output:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer,index=False)
        data = output.getvalue()
    

    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=f'{folder_path}{zone}_{country}_{datetime}.xlsx',
                                    Body=data,
                                    ServerSideEncryption='aws:kms',
                                    SSEKMSKeyId='alias/aws/s3')
    return None