import numpy as np
import pandas as pd
from dataview import mainclass
from flask import Flask, request, render_template
from relevantresults import relevant_main
app = Flask(__name__)

#Need to do this always, just change the homepage value to the page value
@app.route('/')
def index():
    return render_template('index.html')
# compulsory stuff

#Just for checking out the methods
# @app.route('/dummy', methods=['GET', 'POST'])
# def dummy():
#     return 'Medhod used %s' % request.method


@app.route('/tables', methods=['GET','POST'])
def tables():
    classinstance = mainclass()
    default_value = True
    input_num = request.form.get('inputnumber', default_value)
    # input_num = request.form['inputnumber']
    input_num_i = int(input_num)
    dataset_tab = classinstance.seedata(input_num_i)
    return render_template('view.html', tables=[dataset_tab])

@app.route('/relevancy', methods=['GET', 'POST'])
def relevancy():
    default_value1 = 'Uber'
    df = pd.read_csv("data_clean.csv")
    weight_input = [0,1,0,0,0,0,0]
    # These are quantitative columns
    col = ["Total Raised", "Employees", "Growth Rate", "# Active Investors", "Revenue", "Growth Rate Change"]
    # These are popularity based columns, a single rank is calculated oveall for these columns
    popcol = ["Social Growth Rate", "Compete Growth Rate", "Web Growth Rate", "Facebook Likes", "Twitter Followers", "Facebook Likes Change"]
    search_term = request.form.get('compname', default_value1)
    # search_term = request.form['compname']
    relevancy_tab = relevant_main(df, search_term, weight_input)
    mid_result = relevancy_tab.relevance_sort(col, popcol)
    result_df = mid_result.head().to_html()
    return render_template('relevancy.html', tables=[])


if __name__ == "__main__":
    app.run(debug=True)