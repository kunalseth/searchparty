import pandas as pd

xl = pd.ExcelFile("data.xlsx")
df = xl.parse("Data")


df.reset_index(inplace=True) 	# to remove multi level index
new_header = df.iloc[6]	# rows 0-5 are not needed. header present in row 6
df=df.rename(columns = new_header) # rename columns in data frame
df = df[7:]  # remove unwanted rows

df.to_csv("data.csv")
