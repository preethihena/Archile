from django.shortcuts import render, redirect
from .models import User,Channel,Tags,Channel_tags,Post_files,Post,Post_tags
import requests,arrow
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

def index(request):
	return render(request,'archile/search_results.html')

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

		utc = arrow.utcnow()
		local = utc.to('Asia/Kolkata')
		channel_object = Channel(u_id=user,name=name,description=description,logo=logo,creation_datetime=local)
		channel_object.save()

		#saving all tags
		for tag in tags:
			try:
				tag_obj=Tags.objects.get(tag_name=tag)
				tag_obj.no_of_use+=1
			except:
				tag_obj = Tags(tag_name=tag,no_of_use = 1)
			tag_obj.save()
			post_tag=Channel_tags(c_id=channel_object,t_id=tag_obj)
			post_tag.save()
		return redirect(create_channel)
	return render(request, 'archile/create_channel.html')

def create_post(request,c_id):
	channel = Channel.objects.get(c_id=c_id)
	return render(request, 'archile/create_post.html',{'channel':channel})

def save_post(request):
	if request.method == 'POST':
		user = request.user
		title = request.POST['post_title']
		c_id = request.POST['channel']
		channel = Channel.objects.get(c_id=c_id)
		description = request.POST['post_description']
		tags = list(map(lambda tag:tag.strip().lower(),request.POST['post_tags'].split(',')))

		#getting all files
		FILES = ['AUDIO','VIDEO','IMAGES','DOCS','ARCHIVES']
		file_data={}
		for file in FILES:
			if file in request.FILES:
				file_data[file] = request.FILES.getlist(file)

		utc = arrow.utcnow()
		local = utc.to('Asia/Kolkata')
		post_object = Post(u_id=user,c_id=channel,description=description,title=title,creation_datetime=local)
		post_object.save()

		#saving all tags
		for tag in tags:
			try:
				tag_obj=Tags.objects.get(tag_name=tag)
				tag_obj.no_of_use+=1
			except:
				tag_obj = Tags(tag_name=tag,no_of_use = 1)
			tag_obj.save()
			post_tag=Post_tags(p_id=post_object,t_id=tag_obj)
			post_tag.save()


		#saving all files
		for file_name in file_data:
			for file in file_data[file_name]:
				pf_obj=Post_files(p_id=post_object,file_type=file_name,file=file,upload_datetime=local)
				pf_obj.save()

		return redirect(create_post)
	return render(request, 'archile/channel.html')

def edit_post(request):
	return render(request, 'archile/edit_post.html')
	
def post(request):
	return render(request, 'archile/post.html')

def channel(request):
	return render(request, 'archile/channel.html')
