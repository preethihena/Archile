from django.shortcuts import render, redirect
from .models import User
import requests
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

def home(request,token_id):
	payload = {'token': token_id, 'secret':"6d5fc80be2b62f1eb699f1be6bfc44394de1e2e18f7fd825a7cf045e9825b5ac2d5661b924965f49b97d6827a5bbd298e1549660d43ea70c5830af0241ff3482"}
	url = "https://serene-wildwood-35121.herokuapp.com/oauth/getDetails"
	#url="/dammi/"
	response=requests.post(url, data=payload)
	p=response.json()
	p=p['student']
	a=User()
	a.first_name=p[0]['Student_First_Name']
	a.last_name=p[0]['Student_Last_name']
	a.email=p[0]['Student_Email']
	a.token=token_id
	a.save()
	return render(request, 'archile/search_box.html')

def create_channel(request):
	return render(request, 'archile/create_channel.html')

def create_post(request):
	return render(request, 'archile/create_post.html')

def edit_post(request):
	return render(request, 'archile/edit_post.html')