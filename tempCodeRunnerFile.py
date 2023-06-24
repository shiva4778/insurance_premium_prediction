def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
        #data_ingestion_config = DataIngestion().initiate_data_ingestion()
        return 'completed'
    except Exception as e:
        logging.error(f"{e}")
        print(e)