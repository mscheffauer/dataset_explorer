################################################################################
# Author:      Martin Scheffauer
# MatNr:       51917931
# File:        dataset_explorer.py
# Description: implements classes for the main dataset explorer 
# Comments:    the explorer prints information about the dataset and about the features
#              as well as plots the features of a dataset also vs. a target feature.
#              also quartiles and correlations can be calculated and printed
#              the explorer automatically uses the correct plot type by using 
#              the correct plotter subclass depending on the identifier of each feature 
#              that is defined in the config file
################################################################################
#%%

from plotter import Plotter
from dataset import Dataset
import numpy as np

import scipy.stats

from matplotlib.figure import Figure
import math

class DatasetExplorer:


    def __init__(self,dataset : Dataset,plot_types : dict) -> None:
        self._dataset = dataset
        self._plot_types = plot_types
     
    def __str__(self) -> str:
        return f"DatasetExplorer Info:\n\tDataset name: {self._dataset.name}"

    def print_feature_names(self) -> None:
        _feat_cnt = 0
        for feat in self._dataset.feature_names:
            if (_feat_cnt == 0):
                _temporary_string = feat
            else:
                _temporary_string += f", {feat}"
            _feat_cnt+=1
        print("Feature names:\n"+_temporary_string)
    def print_feature_description(self, feature_name = None) -> None:
        _temp_cnt = 0
        if  feature_name is None:
            
            for feat in self._dataset.feature_names:
                if _temp_cnt == 0:
                    _temporary_string =f"\t{feat}: {self._dataset.column_info[feat]}"
                else:
                    _temporary_string +=f"\n\t{feat}: {self._dataset.column_info[feat]}"
                _temp_cnt += 1        
                
            print("Features and descriptions:\n"+_temporary_string)
        elif (isinstance(feature_name,str)):
            print (f"{feature_name}: {self._dataset.column_info[feature_name]}")
    
    def plot_feature(self,feature_name:str) ->Figure:
              
        return Plotter.get_plotter_classes()[self._plot_types[feature_name]].plot_feature(feature_name,\
                                        self._dataset.get_feature_values(feature_name,remove_missing=True))
                       
           
    def plot_feature_vs_target(self,feature_name: str, target_name: str = "" ) -> Figure:
               
        return Plotter.get_plotter_classes()[self._plot_types[feature_name]].plot_feature_vs_target(feature_name,\
                                                  self._dataset.get_feature_values(feature_name,remove_missing=False),\
                                                  target_name,self._dataset.get_target_values())
                
                
        
    def calculate_correlation_between_features(self,feature_name_1: str,feature_name_2:str,\
                                               method:str = "pearson") -> tuple:
        data_1 = self._dataset.get_feature_values(feature_name_1,remove_missing=False)
        data_2 = self._dataset.get_feature_values(feature_name_2,remove_missing=False)
        data_corr_1 = list()
        data_corr_2 = list()
        #check if datas are the same length
        if len(data_1) != len(data_2):
            raise ValueError(Plotter._ERRSTR)  
           
        #only calculate correlation if both features have a value that is not nan
        for val_data_1,val_data_2 in zip(data_1,data_2):
            if not math.isnan(val_data_1) and not math.isnan(val_data_2):
                data_corr_1.append(val_data_1)
                data_corr_2.append(val_data_2)

        #perform statistics
        if method == "pearson":
            return scipy.stats.pearsonr(data_corr_1,data_corr_2)
            
        elif method == "spearman":
            return (scipy.stats.spearmanr(data_corr_1,data_corr_2,nan_policy="omit")[0],
                    scipy.stats.spearmanr(data_corr_1,data_corr_2,nan_policy="omit")[1])
            
        elif method == "kendalltau":
            return (scipy.stats.kendalltau(data_corr_1,data_corr_2,nan_policy="omit")[0],
                    scipy.stats.kendalltau(data_corr_1,data_corr_2,nan_policy="omit")[1])    
        else:
            raise ValueError("correlation method must be one of the following: pearson, spearman or kendalltau")
        
    def print_quartiles_of_feature(self,feature_name:str)->None:
        _temporary_string = "Quartiles:"
        _quartile_cnt = 1
        
        for q in np.quantile(self._dataset.get_feature_values(feature_name,remove_missing=True),(0.25,0.5,0.75)):
            _temporary_string += f"\n\tQ{_quartile_cnt}: {q:.3f}"
            _quartile_cnt += 1
        print(_temporary_string)    
           


# %%

