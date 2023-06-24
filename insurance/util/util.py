import yaml

from insurance.exception import InsuranceException
import os,sys

def read_yaml_file(file_path:str)->dict:
    """
    It is used to read the YAML file
    """

    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise InsuranceException(e,sys)
    