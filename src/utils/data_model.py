import pandas as pd 
import numpy as np

class ServicenowData:
    def __init__(self) -> None:
        self.data: pd.DataFrame = None
        self.iter_index = 0

    def load_data(self, json_response: list): 
        # Data loading logic
        pass

    def load_test_data(self, df):
        self.data = df

    def insert_field(self, column_name:str):
        if column_name not in self.data.columns:
            self.data[column_name] = None
            return True
        else:
            return False
    
    def insert_data(self, index, column_name, value):
        if self.data.at[index, column_name] is None:
            self.data.at[index, column_name] = value
        else:
            raise UserWarning("Trying to modify exsisting value")
        
    def get_data(self, index:int):
        if self.data is not None and self.iter_index < len(self.data):
            row = self.data.iloc[index]
            return row
        else:
            return None
    
    def get_data(self, index:int, columns:list):
        if self.data is not None and index < len(self.data):
            return self.data.loc[index, columns]
        else:
            return None
        
    def get_data(self):
        return self.data
    
    def get_column(self, column_name:str) -> np.array:
        column_array = self.data[column_name].to_numpy()
        return column_array
    
    def filed_names(self)->list:
        if self.data is not None:
            return self.data.columns.tolist()
        else:
            return None
