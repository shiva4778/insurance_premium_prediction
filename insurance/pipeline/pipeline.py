from insurance.config.configuration import Configuration
from insurance.logger import logging
from insurance.exception import InsuranceException
from insurance.component.data_validation import DataValidation
from insurance.component.data_transformation import DataTransformation
from insurance.component.model_trainer import ModelTrainer,InsuranceEstimatorModel



from insurance.entity.artifact_entity import DataIngestionArtifact,ModelTrainerArtifact,DataValidationArtifact
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
        logging.info('reached data ingestion')
        try: 
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            
            logging.info('data_ingestion_completed')
            return data_ingestion.train_test_split()
        except Exception as e:
            raise InsuranceException(e,sys) from e    


    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) :
        try:

            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                                data_ingestion_artifact=self.start_data_ingestion()
                                                )
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise InsuranceException(e, sys) from e

    def start_data_transformation(self):
        try:
            data_transformation=DataTransformation(data_transformation_config=self.config.get_data_transformation_config()\
            ,data_ingestion_artifact=self.start_data_ingestion(),data_validation_artifact=self.start_data_validation(self.start_data_ingestion()))
            logging.info('initiated data transformation')
            return data_transformation.initiate_data_transformation()
        
        except Exception as e:
            raise InsuranceException(e,sys) from e
    def start_model_trainer(self):
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=self.start_data_transformation()
                                         )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise InsuranceException(e, sys) from e

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        try:
            #data ingestion
            #data_ingestion_artifact=self.start_data_ingestion()
            #data_validation_artifact=self.start_data_validation()

            data_transformation_artifact = self.start_model_trainer()

            


        except Exception as e:
            raise InsuranceException(e,sys) from e
        