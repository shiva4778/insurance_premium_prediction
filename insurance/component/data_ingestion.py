from insurance.entity.config_entity import DataIngestionConfig
from insurance.config.configuration import Configuration
import os
import sys
from insurance.exception import InsuranceException
from insurance.logger import logging
import numpy as np
import pandas as pd
from pymongo import MongoClient
from insurance.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info('Data Ingestion log started')
            self.data_ingestion_config=data_ingestion_config


        except Exception as e:

            raise InsuranceException(e,sys)
        
    def connecting_database(self):
        try:
            logging.info('Creating connection with mongodb')
            client = MongoClient(self.data_ingestion_config.dataset_download_url)
            db = client['Insurance_database']
            collection = db['Insurance']
            return db,collection,client

        except Exception as e:
            raise InsuranceException(e,sys) from e
        
    def reading_data(self):
        try:
            db,collection,client=self.connecting_database()
            
            # Retrieve data from MongoDB
            data = collection.find()

            # Convert MongoDB data to a DataFrame
            df = pd.DataFrame(list(data))

            # Save DataFrame as a CSV file
            #df.to_csv('raw_data', index=False)

            # Close the MongoDB connection
            client.close()
            
            
            return df
        except Exception as e:
                raise InsuranceException(e,sys) from e
        

    def raw_data(self):
        raw=None

        raw=self.reading_data()

        raw_data_dir=self.data_ingestion_config.raw_data_dir

        os.makedirs(raw_data_dir,exist_ok=True)

        file_name='raw'

        extension='.csv'

        file_path=os.path.join(raw_data_dir,file_name+extension)

        if raw is not None:    
            #Pass the path not directory , otherwise it will return Permission error   
            raw.to_csv(file_path,index=False)
        logging.info('Raw data ingestion completed')
        return raw
    def train_test_split(self):
        logging.info('reading raw data')

        raw=self.raw_data()

        raw=raw.drop(columns=['_id'],axis=1)

        train_data,test_data=train_test_split(raw,random_state=42,test_size=.20,stratify=raw['children'])

        train_dir=self.data_ingestion_config.ingested_train_dir

        os.makedirs(train_dir,exist_ok=True)

        file_name='train'

        extension='.csv'

        train_file_path=os.path.join(train_dir,file_name+extension)

        train_data.to_csv(train_file_path)

        test_dir=self.data_ingestion_config.ingested_test_dir

        os.makedirs(test_dir,exist_ok=True)

        file_name='test'

        extension='.csv'

        test_file_path=os.path.join(test_dir,file_name+extension)

        test_data.to_csv(test_file_path)

        data_ingestion_artifact=DataIngestionArtifact(train_file_path=train_file_path,
             test_file_path=test_file_path,is_ingested=True,message='Training and testing ingestion is completed')

        logging.info('Training and testing completed')

        logging.info(f"Data Ingestion artifact :{data_ingestion_artifact}")

        return data_ingestion_artifact

        

    
        
            

            

            

            

            
               


