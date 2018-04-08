import pandas as pd
import numpy as np
from collections import Counter


class User:
    def __init__(self, id, watched):
        self.id = id
        self.watched = watched

    @property
    def number_watched_films(self):
        return len(self.watched.keys())


class Users:
    def __init__(self):
        self.bigtv_dataset = None
        self.bigtv_catalog = None
        self.users = None
        self.catalog = None

    def load_dataset(self, filename, sep):
        """Load BigTV dataset"""
        self.bigtv_dataset = pd.read_csv(filename, sep=sep)

    def load_catalog(self, filename, sep):
        """Load BigTV catalog"""
        self.bigtv_catalog = pd.read_csv(filename, sep=sep)

    def prepare_dataset(self):
        self.bigtv_dataset = self.bigtv_dataset[[
            'fts', 'vts', 'uid', 'vcId', 'serverTs'
            ]]
        self.bigtv_dataset = self.bigtv_dataset.dropna(axis=0, how="any")
        pass

    def extract_users(self):
        self.users = []
        data = self.extract_column(self.bigtv_dataset, 'uid')
        for k, v in data.items():
            data[k] = self.extract_column(
                pd.concat(v, axis=1).transpose(), "vcId")

            for key, value in data[k].items():
                data[k][key] = pd.concat(value, axis=1).transpose()
                arr = np.array([int(x) for x in data[k][key]['fts']])
                data[k][key] = arr.max() - arr.min()

            user = User(k, data[k])
            self.users.append(user)

    def prepare_catalog(self):
        self.catalog = {}
        catalog = self.bigtv_catalog[['VcID', 'VcName', 'VcSeries']]
        for idx, row in catalog.iterrows():
            self.catalog[row['VcID']] = [row['VcName'], row['VcSeries']]

    def extract_column(self, df, column):
        """Extract column from pandas.DataFrame
        
        Arguments:
            df {pandas.DataFrame} -- input DataFrame
            column {str} -- df column
        """
        unique_values = list(set(df[column]))
        gen = dict()
        crop_df = df.drop(column, 1)

        for value in unique_values:
            gen[value] = []

        for idx, row in crop_df.iterrows():
            gen[df[column][idx]].append(row.to_frame())

        return gen

    def get_top_films(self, num=10):
        top_films = []
        for user in self.users:
            [top_films.append(x) for x in user.watched if x[1] != 0]
        top_films = dict(Counter(top_films))
        top_films = sorted(top_films.items(), key=lambda x: x[1])
        top_films = top_films[::-1]
        return top_films[:num]

    def find_users_by_parametrs(self, watched=2, zero_duration_permited=True):
        pass