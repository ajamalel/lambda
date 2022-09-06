import json
import pandas as pd
import datetime
import os
import logging
import boto3
from authent import *
from read_data import *
from write_data import *
from usual_functions import *
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

def lambda_handler(event, context):
    
    # Récupération des information d'authentification
    site_url = os.environ["site_url"]
    relative_site_url = "/" + str(site_url.split('/',3)[3])
    client_id = os.environ["client_id"]
    client_secret = os.environ["client_secret"]
    
    # Authentification au Sharepoint
    ctx = authent(site_url,client_id,client_secret)

    # Périmètre des pays
    zone = os.environ["zone"].split(',')
    afr_countries = os.environ["afr_countries"].split(',')
    ame_countries = os.environ["ame_countries"].split(',')
    apmo_countries = os.environ["apmo_countries"].split(',')
    eur_countries = os.environ["eur_countries"].split(',')

    for area in zone:
        
        countries = []
        if area == 'AFR':
            countries = afr_countries
        elif area == 'AME':
            countries = ame_countries
        elif area == 'APMO':
            countries = apmo_countries
        elif area == 'EUR':
            countries = eur_countries
        else:
            raise Exception ('ERROR: Unknown zone in the config file')
            
        for country in countries:
            relative_url = f"{relative_site_url}/Documents%20partages/{area}/{country}"
            folder = ctx.web.get_folder_by_server_relative_url(relative_url)
            file_names = []
            files = folder.files
            ctx.load(files)
            ctx.execute_query()
            
            
            for fil in files:
                file_names.append(fil.properties["Name"])
            
            for excel in file_names:
                if excel and (excel[-4:]) == 'xlsx':
                    file_url = f"{relative_site_url}/Documents%20partages/{area}/{country}/{excel}"
                    
                    # Excel vers df
                    df = excel_to_df(ctx,file_url)
                    
                    # df vers S3
                    try:
                        bucket_name = os.environ["bucket_name"]
                        area_lowcase = area.lower()
                        folder_path = f"{area_lowcase}/inputs/"
                        date_time = dt(datetime.datetime.now())
                        df_to_s3(df,bucket_name,folder_path,area,country,date_time)
                        
                        # Deplacement du fichier source dans les archives
                        try:
                            source_file = ctx.web.get_file_by_server_relative_url(f"{file_url}")
                            source_file.moveto(f"{relative_site_url}/Documents%20partages/archives/{date_time}_{country}_{excel}", 1)
                            ctx.execute_query()
                            
                        except Exception as err:
                            return logging.error(str(err))
                    
                    except Exception as err:
                        return logging.error(str(err))         