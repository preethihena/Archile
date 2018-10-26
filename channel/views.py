from django.shortcuts import render, redirect
import datetime
from .models import *
import requests,arrow
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def index(request):
	return render(request,'archile/search_results.html')



def login(request):
	return render(request,'archile/login.html')

#user logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return redirect(login)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
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
		text =query['search_query'].lower().split()
		
		Channels = Channel.objects.all()
		Posts = Post.objects.all()
		for word in text:
			Channels = Channels.filter(name__icontains=word)
			Posts = Posts.filter(title__icontains=word)
		
		context = {
			'channels': Channels,
			'posts': Posts
		}
		print(context)
		return render(request, 'archile/search_results.html',context)
	else:
		# redirect to home page, as of now redirecting to search_box(which is a dummy for our search filter)
		return redirect(search_box)
	
	return render(request, 'archile/search.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def search_box(request):

	if request.method == 'POST':
		query = {}
		for i in request.POST:
			query[i] = request.POST[i]

		del query['csrfmiddlewaretoken']

		# if query['from'] == '':
		# 	del query['from']

		# if query['to'] == '':
		# 	del query['to']

		return redirect(search,query)


def home(request,token_id):
	payload = {'token': token_id, 'secret':"6d5fc80be2b62f1eb699f1be6bfc44394de1e2e18f7fd825a7cf045e9825b5ac2d5661b924965f49b97d6827a5bbd298e1549660d43ea70c5830af0241ff3482"}
	url = "https://serene-wildwood-35121.herokuapp.com/oauth/getDetails"
	response=requests.post(url, data=payload)
	data=response.json()
	data=data['student']
	try:
		user_object = User.objects.get(token=token_id)
		#print(user_object)
	except:
		user_object=User()
	user_object.first_name=data[0]['Student_First_Name']
	user_object.last_name=data[0]['Student_Last_name']
	user_object.email=data[0]['Student_Email']
	user_object.token=token_id
	user_object.is_active = True
	user_object.save()
	auth_login(request,user_object)
	return redirect(index)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
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
			channel_tag=Channel_tags(c_id=channel_object,t_id=tag_obj)
			channel_tag.save()
		return redirect(create_channel)
	return render(request, 'archile/create_channel.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def create_post(request,c_id):
	channel = Channel.objects.get(c_id=c_id)
	return render(request, 'archile/create_post.html',{'channel':channel})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def save_post(request):
	if request.method == 'POST':
		user = request.user
		title = request.POST['post_title']
		c_id = request.POST['channel']
		ch = Channel.objects.get(c_id=c_id)
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
		post_object = Post(u_id=user,c_id=ch,description=description,title=title,creation_datetime=local)
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

		return redirect(channel,c_id)
	return render(request, 'archile/channel.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def edit_post(request):
	pass


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def edit_channel(request,c_id):
	pass


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')	
def subscribe_channel(request,c_id):
	Chan = Channel.objects.get(c_id=c_id)
	count =Chan.no_of_subscriptions
	user = request.user
	utc = arrow.utcnow()
	local = utc.to('Asia/Kolkata')
	try:
		subs = Subscription.objects.get(c_id=Chan,u_id=user)
		Chan.no_of_subscriptions = count -1
		subs.delete()
	except:
		subs = Subscription(c_id=Chan,u_id=user,s_datetime=local)
		if count == None:
			Chan.no_of_subscriptions = 1
		else:
			Chan.no_of_subscriptions = count + 1
		subs.save()
	Chan.save()
	return redirect(channel,c_id)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def post(request,p_id):
	pass


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def channel(request,c_id):
	channel = Channel.objects.get(c_id=c_id)
	posts=Post.objects.filter(c_id=channel)
	user = request.user
	context = {}
	context['channel'] = channel
	context['posts']=[]
	for post in posts:
		dic=to_dict(post)
		dic['creation_datetime']=arrow.get(dic['creation_datetime']).format('Do MMMM YYYY')
		dic['user']=User.objects.get(id=dic['u_id'])
		try:
			post_atc_obj = post_actions.objects.get(p_id=dic['p_id'],u_id=user.id)
			dic['ld_status'] = post_atc_obj.ld_status
		except:
			dic['ld_status'] = None
		context['posts'].append(dic)

	try:
		subs = Subscription.objects.get(c_id=channel,u_id=user)
		context['subs'] = True
	except:
		context['subs'] = False
	return render(request, 'archile/channel.html',context)
