import numpy as np
import pandas as pd
from flask import Flask, request, render_template, flash, redirect, url_for
from relevantresults import relevant_main
from rank import SearchParty
from initialize import DataImport

app = Flask(__name__)
app.secret_key = 'some_secret'

#Need to do this always, just change the homepage value to the page value
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/relevancy', methods=['GET', 'POST'])
def relevancy():
    data = DataImport()
    df = data.data
    searchparty_inst = SearchParty(data)
    radio_default = 'relevantresults'
    radio_input = request.form.get('similar', radio_default)
    if request.method == 'GET':
        return render_template('relevancy.html', tables=[])
    else:
        if radio_input == 'relevantresults':
            #Relevancy Logic
            column_weights = {"Total Raised": 0.2, "Employees": 0.1, "Growth Rate": 0.3, "# Active Investors": 0.4,
                              "Social Growth Rate": 0.1}
            relevance_midresult = searchparty_inst.relevance(df, column_weights)
            relevance_finalresult = searchparty_inst.sort(df, relevance_midresult).head().to_html()
            return render_template('relevancy.html', tables=[relevance_finalresult])



        elif radio_input == 'similar1':
            #Similar to company logic
            # data = DataImport()
            # df = data.data
            # flash('Similar1')
            default_value2 = 'Uber Technologies'
            company_name = request.form.get('compname', default_value2)
            # searchparty_inst = SearchParty(data)
            similar1_midresult = searchparty_inst.similar_comp(df,company_name)
            similar1_finalresult = searchparty_inst.sort(df, similar1_midresult).head().to_html()
            return render_template('relevancy.html', tables=[similar1_finalresult])
            # return redirect(url_for('relevancy'))

        elif radio_input == 'similar2':
            # flash('Similar2')
            # return redirect(url_for('relevancy'))
            default_value3 = 'Mackenzie Capital Management'
            investor_name = request.form.get('compname', default_value3)
            # searchparty_inst = SearchParty(data)
            similar2_midresult = searchparty_inst.similar_investor_comp(df, investor_name)
            similar2_finalresult = searchparty_inst.sort(df, similar2_midresult).head().to_html()
            return render_template('relevancy.html', tables=[similar2_finalresult])


        else:
            # flash('Similar3')
            # return redirect(url_for('relevancy'))
            default_value4 = 'Mackenzie Capital Management'
            self_name = request.form.get('compname', default_value4)
            similar3_midresult = searchparty_inst.similar_investor_comp(df, self_name)
            similar3_finalresult = searchparty_inst.sort(df, similar3_midresult).head().to_html()
            return render_template('relevancy.html', tables=[similar3_finalresult])




if __name__ == "__main__":
    app.run(debug=True)