## API Endpoints

1. `@app.route('/similarity/', methods=['GET'])`

Parameters: Inputs from 4 drop downs (industry_sector, industry_group, financing_status , business_status) and search_criteria (input from text box). Search_criteria is mandatory input to the API Call and the other parameters are optional.

Sample URL:  `http://127.0.0.1:5000/similarity/?industry_sector=Healthcare,Financial%20Services&business_status=Profitable&search_criteria=facebook`

----

2. `@app.route('/investor/', methods=['GET'])`

Parameters: Inputs from 4 drop downs (industry_sector, industry_group, financing_status , business_status) and search_criteria (input from text box). Search_criteria is mandatory input to the API Call and the other parameters are optional.

Sample URL:  `http://127.0.0.1:5000/relevance/?industry_sector=Information%20Technology&business_status=Profitable&search_criteria=Founders%20Fund`

----

3. `@app.route('/relevance/', methods=['GET'])`

Parameters: Inputs from 4 drop downs (industry_sector, industry_group, financing_status , business_status), inputs from between 0 to 1 (default value 0.5 for all) slider for each item on the following checkboxlist (revenue, profit, valuation, growth, social_growth, facebook, twitter).

Sample URL: `http://127.0.0.1:5000/relevance/?industry_sector=Information%20Technology&revenue=0.7&growth_rate=0.3&profit=0.5&facebook=0.1&twitter=0.2`
