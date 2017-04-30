"""Initialize Data"""

import pandas as pd
from scipy import sparse, io
import time

class DataImport(object):
     
    def __init__(self):
        """
        Importing data from files
        """
        self.data = pd.read_csv("data.csv")
        self.tfidf = io.mmread("tfidf.mtx")
        self.tfidf = self.tfidf.tocsr()



if __name__=='__main__':
	start_time = time.time()
	data = DataImport()
	print("It takes {} seconds to import all data".format(time.time()-start_time))