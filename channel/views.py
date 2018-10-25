from django.shortcuts import render, redirect
from .models import User,Channel,Tags,Channel_tags
import requests
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

def index(request):
	return render(request,'archile/base.html')


def login(request):
	return render(request,'archile/login.html')

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
	response=requests.post(url, data=payload)
	data=response.json()
	data=data['student']
	try:
		user_object = User.objects.get(token=token_id)
	except:
		user_object=User()
	user_object.first_name=data[0]['Student_First_Name']
	user_object.last_name=data[0]['Student_Last_name']
	user_object.email=data[0]['Student_Email']
	user_object.token=token_id
	user_object.is_active = True
	user_object.save()
	login(request, user_object)
	return redirect('/')



# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url='/login')
def create_channel(request):
	if request.method == 'POST':
		name = request.POST['channel_name']
		if 'channel_logo' in request.FILES:
			logo = request.FILES['channel_logo']
		description = request.POST['channel_description']
		tags = list(map(lambda tag:tag.strip(),request.POST['channel_tags'].split(',')))
		user = request.user
		return redirect(create_channel)
	return render(request, 'archile/create_channel.html')