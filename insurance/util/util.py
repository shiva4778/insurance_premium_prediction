import yaml
import pandas as pd
import yaml
import dill
import os,sys
from insurance.constant import *
from insurance.exception import InsuranceException
import os,sys
import numpy as np


def read_yaml_file(file_path:str)->dict:
    """
    It is used to read the YAML file
    """

    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise InsuranceException(e,sys)
    



def load_data(file_path:str,schema_file_path:str)->pd.DataFrame:

    try:
        dataset_schema=read_yaml_file(schema_file_path)

        schema=dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe=pd.read_csv(file_path)
        error_message=''



        for column in dataframe.columns:

            #Typecasting it
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])



            #else:

                #error_message=f'{error_message} \ncolumn:[{column}] is not in the schema.'


        if len(error_message) > 0:
            raise Exception(error_message)
        
        return dataframe
    except Exception as e:
        raise InsuranceException(e,sys) from e
    


def save_numpy_array_data(file_path:str,array:np.array):

    """
    Save numpy array data to file
    file_path:str location of file to save
    arry:np.array data to save
    """

    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open (file_path,'wb') as file_obj:
            np.save(file_obj,array)

    except Exception as e:
        raise InsuranceException(e,sys) from e
    

def save_object(file_path:str,obj):
    '''
    file_path:str
    obj:Any sort of object
    '''

    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)


    except Exception as e:
        raise InsuranceException(e,sys) from e
    