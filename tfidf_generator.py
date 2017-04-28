import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
from scipy import sparse, io

data = pd.read_csv("data.csv",encoding='ISO-8859-1').fillna('')

def preprocess_data(df):
    
    cols = ['Description', 'Primary Industry Sector','Primary Industry Group', 'All Industries', 'Industry Vertical']
    
    feature_string = df[cols]
    feature_string = feature_string[feature_string.columns[0:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
    df['feature_string'] = feature_string
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', stop_words = 'english',ngram_range=(1, 1))
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['feature_string'])

    return tfidf_matrix

s = time.time()
tfidf = preprocess_data(data)
io.mmwrite("tfidf.mtx", tfidf)

print("TFIDF Sparse Matrix created and saved in: ",time.time()-s)
