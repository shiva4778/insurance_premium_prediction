from insurance.exception import InsuranceException
import os,sys
from insurance.logger import logging
from insurance.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from insurance.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from insurance.util.util import read_yaml_file,save_object,save_numpy_array_data,load_data
from insurance.constant import *
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
import os,sys
from sklearn.compose import ColumnTransformer



class FeatureGenerator(BaseEstimator,TransformerMixin):

    def __init__(self,bmi_category=True,
                 bmi_ix=2,columns=None):

        try:
            self.columns=columns
            if self.columns is not None:
                pass
                

        except Exception as e:
            raise InsuranceException(e,sys) from e
        
    def fit(self,X,y=None):
        return self
    
        
    def transform(self,X,y=None):
        try:
            pass
        except Exception as e:
            raise InsuranceException(e,sys) from e


class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact):
        
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact

        except Exception as e:
            raise InsuranceException(e,sys) from e
        

    def get_data_transformation_object(self)->ColumnTransformer:
        try:
            schema_file_path=self.data_validation_artifact.schema_file_path

            dataset_schema=read_yaml_file(file_path=schema_file_path)
            numerical_columns=dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns=dataset_schema[CATEGORICAL_COLUMN_KEY]

            num_pipeline=Pipeline(steps=[
                    ('imputer',SimpleImputer(strategy="median")),
                    ('scaling',StandardScaler())

            ])


            cat_pipeline=Pipeline(steps=[('imputer',SimpleImputer(strategy='most_frequent')),
                    ('onehotEncoder',OneHotEncoder()),
                ('scaling',StandardScaler(with_mean=False))])



            logging.info(f"Categorical columns :{categorical_columns}")
            logging.info(f"Numerical columns : {numerical_columns}")

            preprocessing=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_columns),
                ('cat_pipeline',cat_pipeline,categorical_columns)

            ])

            return preprocessing


        except Exception as e:
            raise InsuranceException(e,sys) from e




    def initiate_data_transformation(self)->DataTransformationArtifact:
     
     try:
          
          
          logging.info(f"Obtaining preprocessing object. ")

          preprocessing_obj=self.get_data_transformation_object()


          logging.info(f"Obtaining training an test file path .")

          train_file_path=self.data_ingestion_artifact.train_file_path

          test_file_path=self.data_ingestion_artifact.test_file_path


          schema_file_path=self.data_validation_artifact.schema_file_path


          logging.info(f"Loading training and test data as pandas dataframe")


          train_df=load_data(file_path=train_file_path,schema_file_path=schema_file_path)

          test_df=load_data(file_path=test_file_path,schema_file_path=schema_file_path)


          schema=read_yaml_file(file_path=schema_file_path)

          target_column_name=schema[TARGET_COLUMN_KEY]

          logging.info(f"Splitting the data")

          input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
          input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
          target_feature_train_df=train_df[target_column_name]

          target_feature_test_df=test_df[target_column_name]


          logging.info(f"Applying preprocessing object on training and testing data frame")


          input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)

          input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

          train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]

          test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
          print(self.data_transformation_config)


          transformed_train_dir=self.data_transformation_config.transformed_train_dir

          transformed_test_dir=self.data_transformation_config.transformed_test_dir

          #npz foramt is used to store an array in compressed format
          train_file_name=os.path.basename(train_file_path).replace('.csv','.npz')

          test_file_name=os.path.basename(test_file_path).replace('.csv','.npz')


          transformed_train_file_path=os.path.join(transformed_train_dir,train_file_name)

          transformed_test_file_path=os.path.join(transformed_test_dir,test_file_name)


          logging.info(f'Saving transformed training and testing array. ')

          save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)

          save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)


          preprocessing_obj_file_path=self.data_transformation_config.preprocessed_object_file_path

          logging.info(f'Saving preprocessing object.')

          save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)
          

          data_transformation_artifact=DataTransformationArtifact(is_transformed=True,
                 message="Data transformation successful",

                 transformed_train_file_path=transformed_train_file_path,

                 transformed_test_file_path=transformed_test_file_path,
                 preprocessed_object_file_path=preprocessing_obj_file_path                                       
                                                                  )

          logging.info(f"Data transformation artifact :{data_transformation_artifact}")

          return data_transformation_artifact
     
     except Exception as e:
          raise InsuranceException(e,sys) from e



     
            

