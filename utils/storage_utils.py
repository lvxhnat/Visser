import os
import string
import datetime
import numpy as np
import pandas as pd

from typing import List
from pathlib import Path


class StorageUtility:

    def __init__(self):
        self.root_url = "resources/documents/"

    def store_items(self, dataframe: pd.DataFrame, write_type: str, endpoint_storage: str):

        dataframe_length = dataframe.shape[0]

        if dataframe_length > 250_000:  # Set max dataframe length as 250K rows
            number_of_chunks = np.ceil(dataframe_length/250_000)
            chunks = np.array_split(dataframe, number_of_chunks)
        else:
            chunks = [dataframe]

        storage_url = self.write_items(write_type=write_type)(
            chunks,
            endpoint_storage=endpoint_storage)

        return storage_url

    def write_items(self, write_type: str):
        write_type = write_type.translate(str.maketrans(
            '', '', string.punctuation)).lower().strip(" ")

        if write_type == "localstorage":
            return self.write_to_local_storage
        elif write_type == "cloudstorage":
            return self.write_to_cloud_storage
        elif write_type == "databasestorage":
            return self.write_to_database
        else:
            raise ValueError(
                f"Storage: Write type to {write_type} is invalid, wrote type should be either localstorage, databasestorage or cloudstorage")

    def write_to_cloud_storage(self, chunks: List[pd.DataFrame], endpoint_storage: str):
        pass

    def write_to_local_storage(
            self,
            chunks: List[pd.DataFrame],
            endpoint_storage: str):
        ''' Function to write data in chunks (if they are excessively large) into local storage as csv files 
        Parameters
        =============
        chunks -> List[pd.DataFrame]        : A list of pandas dataframes containing the data we want to write 
        endpoint_storage -> [str]           : The name of the endpoint e.g. followings 

        Outputs
        =============
        storage_url -> [str]                : The url string containing the path the data is written to
        '''
        now = datetime.datetime.now()
        date, hour = now.strftime("%Y%m%d"), now.strftime("%H%M")

        # e.g. twitter_followings -> ["twitter", "followings"]
        endpoint_list = endpoint_storage.split("_")
        # e.g. "twitter/output/followings"
        endpoint_storage = endpoint_list[0] + "/output/" + endpoint_list[1]
        # Creates full path e.g. "resources/documents/twitter/output/followings/..."
        storage_url = f"{self.root_url + endpoint_storage}/{date}"

        # Check if directory exists, else create it
        Path(storage_url).mkdir(parents=True, exist_ok=True)

        for chunk_no, chunk in enumerate(chunks):
            chunk.to_csv(storage_url + f"/{date + hour}_chunk_{chunk_no}.csv")

        return storage_url

    def write_to_database(self):
        pass
