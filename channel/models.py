from django.db import models

class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=200,unique=True)
    status = models.BooleanField(
        'User status',
        default=True,
        help_text='Designates whether the User is active or not.',
    )
    def __str__(self):
        return str(self.username)

class Channel(models.Model):
	c_id = models.AutoField(primary_key=True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500,default="")
	logo = models.ImageField(upload_to='channel_logo_images', blank=True)
	no_of_subscriptions = models.IntegerField(default=0)
	creation_datetime = models.DateTimeField('date created',auto_now_add=True)
	status = models.BooleanField(
		'Channel status',
		default=True,
		help_text='Designates whether the Channel is active or not.',
		)
	def __str__(self):
		return str(self.name)


class Subscription(models.Model):
	s_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	c_id = models.ForeignKey(Channel,on_delete=models.CASCADE)
	s_datetime = models.DateTimeField('date created',auto_now_add=True)
	def __str__(self):
		return str(self.c_id.name + self.u_id.username)

class Post(models.Model):
	p_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	c_id = models.ForeignKey(Channel,on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=500,default="")
	no_of_likes	= models.IntegerField(default=0)
	no_of_dislikes = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	creation_datetime = models.DateTimeField('date created',auto_now_add=True)
	status = models.BooleanField(
        'Post status',
        default=True,
        help_text='Designates whether the Post is active or not.',
    )
	def __str__(self):
		return str(self.title)

class Post_files(models.Model):
	pf_id = models.AutoField(primary_key = True)
	p_id = models.ForeignKey(Post,on_delete=models.CASCADE)
	file_type = models.CharField(max_length=200)
	file = models.FileField(upload_to='post_files/')
	upload_datetime = models.DateTimeField('upload date and time',auto_now_add=True)
	no_of_likes	= models.IntegerField(default=0)
	no_of_dislikes = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	status = models.BooleanField(
        'Post status',
        default=True,
        help_text='Designates whether the File uploaded is active or not.',
    )
	def __str__(self):
		return str(self.p_id.title+self.pf_id+"status="+self.status)


QA_CHOICES =[('A','Assertive'),('Q','Question')]

class Channel_threads(models.Model):
	ct_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	c_id = models.ForeignKey(Channel,on_delete=models.CASCADE)
	ct_id_reply_to = models.ForeignKey("self",on_delete=models.CASCADE)
	typ = models.CharField(choices=QA_CHOICES,max_length=200)
	description = models.CharField(max_length=500,default="")
	no_of_likes	= models.IntegerField(default=0)
	no_of_dislikes = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	creation_datetime = models.DateTimeField('date created',auto_now_add=True)
	status = models.BooleanField(
        'Channel_thread status',
        default=True,
        help_text='Designates whether the Channel_thread is active or not.',
    )
	def __str__(self):
		return str(self.c_id.name+self.ct_id+"status="+self.status)

class Post_threads(models.Model):
	pt_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	p_id = models.ForeignKey(Post,on_delete=models.CASCADE)
	pt_id_reply_to = models.ForeignKey("self",on_delete=models.CASCADE)
	typ = models.CharField(choices=QA_CHOICES,max_length=200)
	description = models.CharField(max_length=500,default="")
	no_of_likes	= models.IntegerField(default=0)
	no_of_dislikes = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	creation_datetime = models.DateTimeField('date created',auto_now_add=True)
	status = models.BooleanField(
        'Post_thread status',
        default=True,
        help_text='Designates whether the Post_thread is active or not.',
    )
	def __str__(self):
		return str(self.p_id.name+self.pt_id+"status="+self.status)

class Tags(models.Model):
	t_id = models.AutoField(primary_key=True)
	tag_name = models.CharField(max_length=200)
	no_of_use = models.IntegerField(default=0)
	def __str__(self):
		return str(self.tag_name+self.no_of_use)


class Post_tags(models.Model):
	p_id = models.AutoField(primary_key = True)
	t_id = models.ForeignKey(Tags,on_delete=models.CASCADE)

class Channel_tags(models.Model):
	c_id = models.AutoField(primary_key = True)
	t_id = models.ForeignKey(Tags,on_delete=models.CASCADE)

class post_actions(models.Model):
	pa_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	p_id = models.ForeignKey(Post,on_delete=models.CASCADE)
	datetime = models.DateTimeField('date created',auto_now_add=True)
	ld_status = models.NullBooleanField()
	report_status = models.NullBooleanField()

class post_file_actions(models.Model):
	pfa_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	pf_id = models.ForeignKey(Post_files,on_delete=models.CASCADE)
	datetime = models.DateTimeField('date created',auto_now_add=True)
	ld_status = models.NullBooleanField()
	report_status = models.NullBooleanField()

class channel_thread_actions(models.Model):
	cta_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	ct_id = models.ForeignKey(Channel_threads,on_delete=models.CASCADE)
	datetime = models.DateTimeField('date created',auto_now_add=True)
	ld_status = models.NullBooleanField()
	report_status = models.NullBooleanField()

class post_thread_actions(models.Model):
	pta_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	pt_id = models.ForeignKey(Post_threads,on_delete=models.CASCADE)
	datetime = models.DateTimeField('date created',auto_now_add=True)
	ld_status = models.NullBooleanField()
	report_status = models.NullBooleanField()

class channel_actions(models.Model):
	ca_id = models.AutoField(primary_key=True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	report_status = models.NullBooleanField()
		
	
		