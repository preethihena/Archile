from django.shortcuts import render, redirect

# Create your views here.
def index(request):
	return render(request,'archile/index.html')

def search(request,query):
	
	if query:
		print(query)
	#if improper query....
	return render(request, 'archile/search.html')

def search_box(request):

	if request.method == 'POST':
		for i in request.POST:
			print(i,"\t",request.POST[i])
		return redirect(search,request.POST)
	else:
		pass
	return render(request, 'archile/search_box.html')