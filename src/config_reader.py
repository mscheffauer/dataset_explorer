################################################################################
# Author:      Martin Scheffauer
# MatNr:       51917931
# File:        config_reader.py
# Description: implements classes for a complete banking system 
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################
#%%
import json
class ConfigReader: 
    @staticmethod 
    def read_json_config(config_file:str) -> dict:
        assert(isinstance(config_file,str))
        with open(f"./{config_file}", encoding="utf-8") as conf_file:
            return json.load(conf_file)   