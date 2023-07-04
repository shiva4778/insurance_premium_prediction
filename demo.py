from insurance.pipeline.pipeline import Pipeline
from insurance.exception import InsuranceException
from insurance.logger import logging
from insurance.config.configuration import Configuration
from insurance.component.data_ingestion import DataIngestion
import pandas as pd
def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
        #Configuration().get_data_transformation_config()
        
        return 'completed'
    except Exception as e:
         logging.error(f"{e}")
         print(e)

if __name__=="__main__":
    main()