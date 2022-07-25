import json
from pathlib import Path
from typing import List, Union

import pandas as pd


class Dataset:
    def __init__(self, config_info_dict: dict) -> None:
        self.name = config_info_dict["dataset_name"]
        self._data_folder_path = config_info_dict["data_folder"]
        self._na_characters = config_info_dict["na_characters"]
        self._target_feature_name = config_info_dict["target_feature"]

        with open(Path(self._data_folder_path) / config_info_dict["column_info_file"]) as column_info_file:
            self._column_info = json.load(column_info_file)

        self._load_data()
        if "binarize_threshold" in config_info_dict:
            self._binarize_targets(config_info_dict["binarize_threshold"])


    def __str__(self) -> str:
        num_samples, num_features = self._dataframe.shape
        return (f"Dataset Info:\n"
                f"\tDataset name: {self.name}\n"
                f"\tNumber of features: {num_features}, number of rows: {num_samples}")


    @property
    def name(self) -> str:
        return self._name


    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"name must be a string")
        self._name = name


    @property
    def column_info(self) -> dict:
        return self._column_info


    @property
    def feature_names(self) -> list:
        return list(self._column_info.keys())


    @property
    def target_feature_name(self) -> str:
        return self._target_feature_name


    def get_feature_values(self, *feature_names: str, remove_missing: bool = False) -> Union[list, List[list]]:
        feature_values = self._dataframe.loc[:, feature_names]
        if remove_missing:
            feature_values = feature_values.dropna()
        return feature_values.values.T.squeeze().tolist()


    def get_target_values(self) -> list:
        return self._dataframe[self._target_feature_name].tolist()


    def write_data_to_file(self, output_file: str) -> None:
        self._dataframe.to_csv(output_file,
                               index=False,
                               header=False,
                               na_rep=self._na_characters[0])


    def _binarize_targets(self, threshold: int) -> None:
        below_threshold = self._dataframe[self._target_feature_name] < threshold
        self._dataframe.loc[below_threshold, self._target_feature_name] = 0
        self._dataframe.loc[~below_threshold, self._target_feature_name] = 1


    def _load_data(self) -> None:
        data_files = Path(self._data_folder_path).glob("*.csv")
        dataframes = []
        for data_file in data_files:
            dataframes.append(pd.read_csv(data_file,
                                          names=self.feature_names,
                                          keep_default_na=False,
                                          na_values=self._na_characters))
        self._dataframe = pd.concat(dataframes)
