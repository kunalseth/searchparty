
import time
import pandas as pd
import numpy as np
import collections
from scipy import sparse, io
from initialize import DataImport
from sklearn.metrics.pairwise import cosine_similarity


class SearchParty(DataImport):
    
    def __init__(self, DataImport):
        """
        Inheriting data from parent class
        """
        
        self.data = DataImport.data
        self.tfidf = DataImport.tfidf
        self.length = len(self.data)
        self.df = self.data.copy()
        self.filters = collections.defaultdict(list)


    def filter(self, df, filters):
        """
        Function to filter the data based on multiple columns
        Returns: Dataframe subset with filtered values
        """
        if any(filters):
            for column, values in filters.items():
                df = df.loc[df['column'].isin(values)]

        return df

    def append_filter_values(self, column, value):
        """
        Function to store the filter criteria
        Returns: a list dictionary
        """
        return self.filters[column].append(value)

    def treat_missing_vals(self, df, treatment):
        """
        Functions takes a dataframe and treats missing values based on situation
        Returns: Dataframe without missing values
        """
        return df.fillna(treatment, inplace=False)

    def company_search(self, df, value):
        """
        Function to perform substring search by company name
        Returns: Dataframe subset of companies that match
        """
        index = df['Company Name'].str.contains(value, case=False)
        return df[index]

        
    def sort(self, df, scores):
        """
        Function to rank the data by similarity score
        Returns: Ordered Dataframe by desc score
        """
        df['scores'] = scores
        return df.sort_values(by="scores", ascending=False)


    def calculate_rank(self, df_col):
        """
        Function to calculate rank for a column
        Returns: Pandas Rank Series
        """
        return np.array(df_col.rank(ascending=1))


    def similar_comp(self, df, company_name, print_time=True):
        """
        Function Calculates Cosine similarity between a selected company with all companies
        Returns: Similarity Scores (Scale [0,1])
        """
        start = time.time()
        # index of the selected company in the data
        index = df[df['Company Name'] == company_name].index
        
        # compute cosine similarity
        similarity_scores = cosine_similarity(self.tfidf[index], self.tfidf)
        
        # Reshape array for the shape of the df
        similarity_scores = np.reshape(similarity_scores, len(df))
        
        if print_time:
            print("Time Taken to Calculate companies similar to {}: {}".format(company_name,time.time()-start))
        
        return similarity_scores
 

    def similar_investor_comp(self, df, investor, print_time=True):
        """
        Function finds all companies invested by investor and the corresponding most similar companies
        Returns: Aggregated Similarity Scores (Scale [0,1])
        """
        
        start = time.time()
        # Find all the companies invested by investor
        index = df['Active Investors'].str.contains(investor, case=False, na=False)
        companies = df['Company Name'][index]
        
        # Calculate an aggregate score of similarity
        aggregate_scores = np.zeros(len(df))
        total_companies = len(companies)
        for c in companies:
            aggregate_scores += self.similar_comp(df, c, print_time=False)
        aggregate_scores = aggregate_scores/total_companies
        
        if print_time:
            print("Time Taken to Calculate companies similar to {} companies Invested by {}: {}".format(total_companies,investor,time.time()-start))
            
        return aggregate_scores


    def relevance(self, df, column_weights, print_time=True):
        """
        Function to compute rank companies based on the weights and data
        Input: column_weights is a dictionary with col name as key and weight as value
        Returns: Final Relevance Rank (Higher means better)
        """

        start = time.time()
        rank_df = df[list(column_weights.keys())]
        rank_df = self.treat_missing_vals(rank_df, -1)

        relevance_score = np.zeros(len(rank_df))
        for column, weight in column_weights.items():

            score = self.calculate_rank(rank_df[column]) 
            relevance_score += score * weight

        relevance_score = relevance_score/len(column_weights)

        if print_time:
            print("Time Taken to Calculate Relevance for criteria {}: {}".format(column_weights,time.time()-start))
        
        return relevance_score



# if __name__=='__main__':
#
#     data = DataImport()
#     df = data.data
#     s = SearchParty(data)
#
#     ### Here we might call the functions for filters/company search and
#     ### then pass the returned filtered data to the functions below
#
#     similar_to_uber = s.similar_comp(df,'Uber Technologies')
#     similar_to_uber = s.sort(df, similar_to_uber)
#
#     similar_to_fm = s.similar_investor_comp(df,'Mackenzie Capital Management')
#     similar_to_fm = s.sort(df, similar_to_fm)
#
#     column_weights = {"Total Raised":0.2,"Employees":0.1,"Growth Rate":0.3,"# Active Investors":0.4,"Social Growth Rate":0.1}
#     relevance = s.relevance(df, column_weights)
#     relevance = s.sort(df, relevance)


