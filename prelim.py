import pandas as pd
print("Extractig data from file..")
xl = pd.ExcelFile("data.xlsx")
print("Parsing data..")
df = xl.parse("Data")
print("Minor data cleaning")
df.reset_index(inplace=True) 	# to remove multi level index
new_header = df.iloc[6]	# rows 0-5 are not needed. header present in row 6
df=df.rename(columns = new_header) # rename columns in data frame
df = df[7:]  # remove unwanted rows
print("Saving as csv")
df.to_csv("data.csv",encoding="utf-8")
