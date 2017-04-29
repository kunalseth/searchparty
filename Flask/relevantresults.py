import pandas as pd
import numpy as np
import time
import math

class relevant_main(object):
    # df = pd.read_csv("data_clean.csv")

    def __init__(self, data, searchterm, weights):
        """
        Setting up global variables
        """
        self.starttime = time.time()
        self.order_df = data.copy()
        self.df_colnames = list(self.order_df)
        self.searchterm = searchterm
        self.rank_colname_list = []
        self.weights = weights
        # self.flag = False
        self.mostrelvdf = None

    def relevance_sort(self, colnames, popularitycolnames):

        # Ignoring search terms with character length less than 2
        if len(self.searchterm.strip()) > 2:
            # Segregating exact match results from the data to be relevantly ordered.
            # Checking the search term in Company Name and Ticker columns
            self.mostrelvdf = self.order_df[self.order_df['Company Name'].apply(
                lambda x: x.lower()).str.contains(self.searchterm.lower()) | self.order_df['Ticker'].apply(
                lambda x: str(x).lower()).str.contains(self.searchterm.lower())].reset_index()

            print(len(self.mostrelvdf))

            self.order_df = self.order_df[~self.order_df['Company Name'].apply(
                lambda x: x.lower()).str.contains(self.searchterm.lower())]
            self.order_df = self.order_df[~self.order_df['Ticker'].apply(
                lambda x: str(x).lower()).str.contains(self.searchterm.lower())].reset_index()
            print(len(self.order_df))

        # Calculating ranks for all the columns
        self.order_df, self.rank_colname_list = self.calculate_rank(self.order_df, colnames, False)

        # Calculating one rank for all the popularity based columns; as we could accept only one weight
        # self.flag = True
        self.order_df, popularity_colName = self.calculate_rank(self.order_df, popularitycolnames, True)
        # self.flag = False
        self.rank_colname_list.append(popularity_colName)

        # Multiplying individual columns with their weights
        self.order_df[self.rank_colname_list] = self.order_df[self.rank_colname_list] * self.weights

        # Calculating mean rank and adding a order column
        self.order_df.insert(0, 'order', self.order_df[self.rank_colname_list].mean(skipna=True, axis=1))

        # print(order_df) #to print order -- for reference
        print("Generated order for ", len(self.order_df), " rows in ", time.time() - self.starttime, " seconds")

        # Sorting based on order column to get relevant results on top
        self.order_df = self.order_df.sort_values(by='order', ascending=False, na_position='last')

        # Concating exact match df and order df
        if self.mostrelvdf is not None:
            self.final_df = self.mostrelvdf.append(self.order_df)[self.df_colnames]
            print(len(self.final_df))
            return (self.final_df)
        else:
            print(len(self.order_df))
            return (self.order_df)[self.df_colnames]

    def calculate_rank(self, order_df, colnames, flag):
        rank_colname_list = []
        for i in colnames:
            rank_colname_list.append(i + '_rank')
            ranking_list = order_df[i].rank(na_option='bottom')

            # In the below logic we are assigning lowest rank to the missing values so that they appear at the last

            for j in range(len(order_df[i])):
                if math.isnan(order_df[i][j]):
                    ranking_list[j] = 1

            order_df[i + '_rank'] = ranking_list

        # Creating a mean rank of all the popularity columns, so that we accept only one weight for them
        if flag:
            order_df.insert(0, 'popularity_rank', order_df[rank_colname_list].mean(skipna=True, axis=1))
            return order_df, 'popularity_rank'
        else:
            return order_df, rank_colname_list





