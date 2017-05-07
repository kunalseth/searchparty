from flask import Flask, request
from rank import SearchParty
from initialize import DataImport
import json
from collections import defaultdict

app = Flask(__name__)

def deserialize_args(args):
	"""
	Function to deserialize immutable dict to mutable python dicts
	returns: List dictionaries for column weights and filter criteria
	"""

	filters = defaultdict(list)
	column_weights = {}
	search_criteria = None
	fields = {'industry_sector':'Primary Industry Sector', 'industry_group':'Primary Industry Group',
	'financing_status':'Company Financing Status','business_status':'Business Status'}

	relevance = {'revenue':'Revenue','profit':'Gross Profit','valuation':'Last Financing Valuation',
	'growth':'Growth Rate', 'social_growth':'Social Growth Rate', 'facebook':'Facebook Likes', 'twitter':'Twitter Followers'}

	for k, v in args.items():
		if k in fields.keys():
			filters[fields[k]] = v.split(',')
		elif k in relevance.keys():
			column_weights[relevance[k]] = float(v)
		elif k == 'search_criteria':
			search_criteria = v

	return filters, search_criteria, column_weights


@app.route('/similarity/', methods=['GET'])
def similar_companies():
	"""
	Endpoint for generating companies most similar to company X
	returns: json object to the GET call
	"""

	try:
	    filters, search_criteria, column_weights = deserialize_args(request.args)
	    filtered_data = s.filter(df, filters)
	    company = s.company_search(df, search_criteria)
	    similarity_score = s.similar_comp(filtered_data, company)
	    output = s.sort(filtered_data, similarity_score).to_dict()
	    return json.dumps(str(output))
	except:
		return json.dumps({"Output":"No companies match the input criteria"})


@app.route('/investor/', methods=['GET'])
def investor_companies():
	"""
	Endpoint for generating companies most similar to companies invested by investor X
	returns: json object to the GET call
	"""

	try:
	    filters, search_criteria, column_weights = deserialize_args(request.args)
	    filtered_data = s.filter(df, filters)
	    similarity_score = s.similar_investor_comp(filtered_data, search_criteria)
	    output = s.sort(filtered_data, similarity_score).to_dict()
	    return json.dumps(str(output))
	except:
		return json.dumps({"Output":"No companies match the input criteria"})


@app.route('/relevance/', methods=['GET'])
def relevance_rank():
	"""
	Endpoint for generating a ranking based on some user input for relevance
	returns: json object to the GET call
	"""

	try:
	    filters, search_criteria, column_weights = deserialize_args(request.args)
	    print(filters, search_criteria, column_weights)
	    filtered_data = s.filter(df, filters)
	    relevance_rank = s.relevance(filtered_data, column_weights)
	    output = s.sort(filtered_data, relevance_rank).to_dict()
	    return json.dumps(str(output))
	except:
		return json.dumps({"Output":"No companies match the input criteria"})

if __name__ == '__main__':  
	global df
	global tfidf
	d = DataImport()
	df = d.data
	s = SearchParty(d)
	app.run(debug=True)