from insurance.config.configuration import Configuration
from insurance.logger import logging
from insurance.exception import InsuranceException

from insurance.entity.artifact_entity import DataIngestionArtifact
from insurance.entity.config_entity import DataIngestionConfig
from insurance.component.data_ingestion import DataIngestion
import os,sys

class Pipeline:

    def __init__(self,config: Configuration = Configuration()) -> None:
        try:
            self.config=Configuration()

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try: 
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            
            logging.info('data_ingestion_completed')
            return data_ingestion.train_test_split()
        except Exception as e:
            raise InsuranceException(e,sys) from e    


    def start_data_validation(self):
        pass

    def start_data_transformation(self):
        pass

    def start_model_trainer(self):
        pass

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        try:
            #data ingestion

            data_ingestion_artifact = self.start_data_ingestion()

            


        except Exception as e:
            raise InsuranceException(e,sys) from e
        