import pandas as pd
import numpy as np

class mainclass:
    def seedata(self, n):
        dataset = pd.read_csv('data.csv')
        dataset_tab = dataset.head(n).to_html()
        return dataset_tab


