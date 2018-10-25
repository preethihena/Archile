from django.shortcuts import render, redirect
#import requests
# Create your views here.
def index(request):
	return render(request,'archile/base.html')

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

def home(request,token_id):
	payload = {'token': token_id, 'secret':"6d5fc80be2b62f1eb699f1be6bfc44394de1e2e18f7fd825a7cf045e9825b5ac2d5661b924965f49b97d6827a5bbd298e1549660d43ea70c5830af0241ff3482"}
	url = "https://serene-wildwood-35121.herokuapp.com/oauth/getDetails"
	#url="/dammi/"
	response=requests.post(url, data=payload)
	p=response.text
	print(p)
	return render(request, 'archile/create_channel.html')


def new_channel_data(request,channel_data):
	if channel_data:
		print(channel_data)
	if 'channel_logo' in request.FILES:
			print(request.FILES['channel_logo'])
	return redirect('/')

def create_channel(request):

	if request.method == 'POST':
		if 'channel_logo' in request.FILES:
			print(request.FILES['channel_logo'])
		for i in request.POST:
			print(i,"\t",request.POST[i])
		return redirect(new_channel_data,request.POST)
	else:
		pass
	return render(request, 'archile/create_channel.html')