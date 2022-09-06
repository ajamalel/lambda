from office365.sharepoint.files.file import File
from io import BytesIO
import logging
import pandas as pd

def excel_to_df(ctx,file_url):
    response = File.open_binary(ctx,file_url)
    
    bytes_file_obj = BytesIO()
    bytes_file_obj.write(response.content)
    bytes_file_obj.seek(0) #set file object to start
    
    #read excel file and each sheet into pandas dataframe 
    try:
        df = pd.read_excel(bytes_file_obj,header=0,sheet_name=0,engine='openpyxl')
        return df
        
    except Exception as err:
        return logging.error(str(err))