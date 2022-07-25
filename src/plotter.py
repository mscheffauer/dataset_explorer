################################################################################
# Author:      Martin Scheffauer
# MatNr:       51917931
# File:        plotter.py
# Description: implements classes for the plotter submodule 
# Comments:    the abstract class provides the general function prototype 
#              all subclasses implement each a different type of plotter (Histogram, Bar,Box)
#              different plotters are identified for each feature in the dataset using
#              the first three characters of the plotter: bar, box, his respectively
#               
################################################################################
#%%
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import math

class Plotter(ABC):
    _OCCSTR = "count"
    _TARGSTR = " vs "
    _ERRSTR = "Feature value list is not as long as target_values list"
    
    @staticmethod
    def _filter_nan(feature_values:list,target_values:list)->list:
        _features_notnan = list()
            
        if len(feature_values) != len(target_values):
            raise ValueError(Plotter._ERRSTR)  
        #first filter if features and targets are not nan
        for feat_val, target_val in zip(feature_values,target_values):
            if not math.isnan(feat_val) and not math.isnan(target_val):               
                _features_notnan.append([feat_val,target_val])
        #then create a feature value group for each target value
        # code from internet:
        # https://stackoverflow.com/questions/5695208/group-list-by-values
        # date: 18.04.2022 09:51 am
        #map = applies small lambda function to _features_notnan,
        #lambda -> takes second element = value from pair
        #set = set of unique numbers
        # then return the element pair of features if the second element of features is x
        #  where x is from value set
        values = set(map(lambda x:x[1], _features_notnan))
        return [[[y[0] for y in _features_notnan if y[1]==x],[x]] for x in values]         
             
    @staticmethod
    @abstractmethod 
    def plot_feature(feature_name : str, feature_values : list) ->Figure:
        pass
    
    @staticmethod
    @abstractmethod 
    def plot_feature_vs_target(feature_name : str, feature_values : list, 
                               target_name : str, target_values : list) -> Figure:
        pass

    @classmethod
    def get_plotter_classes(cls) -> dict:
        _list_ident = list()
        _list_cls_name = list()
        for classes in Plotter.__subclasses__():
            #take the first few characters without "plotter"
            _cls_temp_name = classes.__name__.lower()
            _cls_temp_name = _cls_temp_name.replace("plotter", "")
            _list_ident.append(_cls_temp_name)
            _list_cls_name.append(classes)
        _class_dict = dict(zip(_list_ident,_list_cls_name))
        return _class_dict
 

class BoxPlotter(Plotter):
   
    @staticmethod
    def plot_feature(feature_name : str, feature_values : list) -> Figure:
        #create boxplot
        fig, ax = plt.subplots()
        ax.set_title("Boxplot of " + feature_name)
        ax.set_ylabel("Value of " + feature_name)
        ax.set_xlabel(feature_name)
        plt.boxplot(np.array(feature_values))
         
        return fig
    @staticmethod 
    def plot_feature_vs_target(feature_name : str, feature_values : list,\
                               target_name : str, target_values : list) -> Figure: 
        #create two boxplots

        fig, ax = plt.subplots()
        for _li in Plotter._filter_nan(feature_values,target_values):

            ax.boxplot(np.array(_li[0]),positions=_li[1], widths=0.35)
                                

        if target_name == "":
            ax.set_title("Boxplot of " +feature_name)
        else:
            ax.set_title("Boxplot of " +feature_name + Plotter._TARGSTR + target_name)
       
        ax.set_ylabel("Values of " +feature_name)
        ax.set_xlabel(target_name + " target class")
        return fig

       
class BarPlotter(Plotter):
  
    @staticmethod
    def plot_feature(feature_name : str, feature_values : list) ->Figure:
        
        #find unique values and unique counts in feature_values using np.unique    
        _feat_array = np.array(feature_values)
        _unique_numbers,_unique_num_counts = np.unique(_feat_array,return_counts=True)
     
        #plot bar
        fig, ax = plt.subplots()
        ax.set_title("Barplot of "+feature_name)
    
        ax.set_ylabel(Plotter._OCCSTR)
        ax.set_xlabel(feature_name)
        ax.bar(x=_unique_numbers, height=_unique_num_counts)
          
        return fig

    @staticmethod 
    def plot_feature_vs_target(feature_name : str, feature_values : list,\
                               target_name : str, target_values : list) -> Figure:
     
        #plot barcharts
        fig, ax = plt.subplots(1,len(Plotter._filter_nan(feature_values,target_values)))
        cnt = 0
        if target_name == "":
            fig.suptitle("Barplot of "+feature_name)
        else:
            fig.suptitle("Barplot of "+feature_name + Plotter._TARGSTR + target_name)

        for _li in Plotter._filter_nan(feature_values,target_values):

            
            _pos_feats = np.array(_li[0])
            _unique_num_pos,_unique_num_counts_pos = np.unique(_pos_feats,return_counts=True)
            if cnt == 0:
                ax[cnt].set_ylabel(Plotter._OCCSTR)
            ax[cnt].set_title("Features for target class " + str(_li[1][0]))
            ax[cnt].set_xlabel(feature_name)
            ax[cnt].bar(x=_unique_num_pos, height=_unique_num_counts_pos, width=0.4)
            cnt += 1
        return fig


    
class HistogramPlotter(Plotter):

    @staticmethod
    def plot_feature(feature_name : str, feature_values : list) -> Figure:

        #plot the histogram of the data
 
        fig, ax = plt.subplots()
        ax.hist(np.array(feature_values), 50, facecolor='blue', alpha=0.9 ,align='mid')
        ax.set_title("Histogram of " + feature_name)
        ax.set_ylabel(Plotter._OCCSTR)
        ax.set_xlabel(feature_name)
        ax.grid(True)
        
        return fig
    @staticmethod 
    def plot_feature_vs_target(feature_name : str, feature_values : list,\
                               target_name : str, target_values : list) -> Figure: 
    
        #filter out nans
        #create two histograms with step mode 
        fig, ax = plt.subplots(1,len(Plotter._filter_nan(feature_values,target_values)))
        cnt = 0
        if target_name == "":
            fig.suptitle("Histogram of " + feature_name)
        else:
            fig.suptitle("Histogram of " + feature_name + Plotter._TARGSTR + target_name)
        for _li in Plotter._filter_nan(feature_values,target_values):

            
            ax[cnt].hist(_li[0], 50,alpha=0.9,align='mid')
            
            ax[cnt].set_title("Features for target class " + str(_li[1][0]))
            if cnt == 0:
                ax[cnt].set_ylabel(Plotter._OCCSTR)
            ax[cnt].set_xlabel(feature_name)
            ax[cnt].grid(True)
            cnt+=1


        return fig



#%%