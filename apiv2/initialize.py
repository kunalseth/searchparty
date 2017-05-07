"""Initialize Data"""

import pandas as pd
from scipy import sparse, io
import time

class DataImport(object):
     
    def __init__(self):
        """
        Importing data from files
        """
        fields = ['Company Name', 'Description', 'Primary Industry Sector', 'Primary Industry Group',  
        'Industry Vertical',   'Company Financing Status', 'Total Raised',    'Business Status', 
        'Ownership Status', 'Revenue','Gross Profit', 'Active Investors' , '# Active Investors', 
        'Last Financing Valuation','Growth Rate', 'Social Growth Rate', 'Facebook Likes', 'Twitter Followers']
        
        self.data = pd.read_csv("data.csv")[fields]
        self.tfidf = io.mmread("tfidf.mtx")
        self.tfidf = self.tfidf.tocsr()



if __name__=='__main__':
	start_time = time.time()
	data = DataImport()
	print("It takes {} seconds to import all data".format(time.time()-start_time))