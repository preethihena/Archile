from django.shortcuts import render, redirect
import datetime

# Create your views here.
def index(request):
	return render(request,'archile/index.html')

def search(request,query):
	
	def valid_date(inputDate):
		try:
			year,month,day = inputDate.split('-')
		except:
			return False

		isValidDate = True

		try :
		    datetime.datetime(int(year),int(month),int(day))
		except ValueError :
		    isValidDate = False
		
		return isValidDate
	
	def valid_search(search_query):
		if 'search_query' not in search_query:
			return False
		if 'from' in search_query:
			if valid_date(search_query['from']) == False:
				return False
		if 'to' in search_query:
			if valid_date(search_query['to']) == False:
				return False

		for i in ['channel','post','documents','videos','images','audio','archives']:
			if i in search_query:
				if search_query[i] != 'on':
					return False
		
		if 'sort' in search_query:
			if search_query['sort'] not in ['uploadDate_asc','uploadDate_dec','likes_asc','likes_dec','size_asc','size_dec']:
				return False
		return True

	#query is a string, converting it to dictionary
	query = eval(query)

	if valid_search(query):
		#Send the search reults with this query to search-results page.
		return render(request, 'archile/search.html')
	else:
		# redirect to home page, as of now redirecting to search_box(which is a dummy for our search filter)
		return redirect(search_box)
	
def search_box(request):

	if request.method == 'POST':
		query = {}
		for i in request.POST:
			query[i] = request.POST[i]

		del query['csrfmiddlewaretoken']

		if query['from'] == '':
			del query['from']

		if query['to'] == '':
			del query['to']

		return redirect(search,query)

	return render(request, 'archile/search_box.html')