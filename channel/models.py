from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
#from .managers import UserManager
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    token = models.CharField(_('token'), max_length=1000, blank=True)
    # password=models.CharField(_('password'),max_length=32,null=True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Channel(models.Model):
	c_id = models.AutoField(primary_key=True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500,default="")
	logo = models.ImageField(upload_to='channel_logo_images', blank=True)
	no_of_subscriptions = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	creation_datetime = models.DateTimeField('date created',auto_now=True)
	status = models.BooleanField(
		'Channel status',
		default=True,
		help_text='Designates whether the Channel is active or not.',
		)
	def __str__(self):
		return str(self.name+str(self.c_id))
	def logo_name(self):
		if self.logo:
			return list((self.logo.name).split('/'))[1]
		else:
			return None


class Subscription(models.Model):
	s_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	c_id = models.ForeignKey(Channel,on_delete=models.CASCADE)
	s_datetime = models.DateTimeField('date created',auto_now=True)
	def __str__(self):
		return str(self.c_id.name + self.u_id.username)
	class Meta:
		unique_together = ('c_id', 'u_id',)

class Post(models.Model):
	p_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	c_id = models.ForeignKey(Channel,on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=500,default="")
	no_of_likes	= models.IntegerField(default=0)
	no_of_dislikes = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	creation_datetime = models.DateTimeField('date created',auto_now=True)
	status = models.BooleanField(
        'Post status',
        default=True,
        help_text='Designates whether the Post is active or not.',
    )
	def __str__(self):
		return str(self.title+str(self.p_id))

	def myfiles(self):
		return Post_files.objects.all().filter(p_id=self.p_id)
	
class Post_files(models.Model):
	pf_id = models.AutoField(primary_key = True)
	p_id = models.ForeignKey(Post,on_delete=models.CASCADE)
	file_type = models.CharField(max_length=200)
	file = models.FileField(upload_to='post_files/')
	upload_datetime = models.DateTimeField('upload date and time',auto_now=True)
	no_of_likes	= models.IntegerField(default=0)
	no_of_dislikes = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	status = models.BooleanField(
        'Post status',
        default=True,
        help_text='Designates whether the File uploaded is active or not.',
    )
	def __str__(self):
		return str(str(self.p_id)+str(self.pf_id)+"status="+str(self.status))

	def myname(self):
		return list((self.file.name).split('/'))[1]

QA_CHOICES =[('A','Assertive'),('Q','Question')]

class Channel_threads(models.Model):
	ct_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	c_id = models.ForeignKey(Channel,on_delete=models.CASCADE)
	ct_id_reply_to = models.ForeignKey("self",on_delete=models.CASCADE,null=True)
	typ = models.CharField(choices=QA_CHOICES,max_length=200)
	description = models.CharField(max_length=500,default="")
	no_of_likes	= models.IntegerField(default=0)
	no_of_dislikes = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	creation_datetime = models.DateTimeField('date created',auto_now=True)
	status = models.BooleanField(
        'Channel_thread status',
        default=True,
        help_text='Designates whether the Channel_thread is active or not.',
    )
	def __str__(self):
		return str(self.c_id.name+str(self.ct_id)+"status="+self.status)

class Post_threads(models.Model):
	pt_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	p_id = models.ForeignKey(Post,on_delete=models.CASCADE)
	pt_id_reply_to = models.ForeignKey("self",on_delete=models.CASCADE,null=True)
	typ = models.CharField(choices=QA_CHOICES,max_length=200)
	description = models.CharField(max_length=500,default="")
	no_of_likes	= models.IntegerField(default=0)
	no_of_dislikes = models.IntegerField(default=0)
	no_of_reports = models.IntegerField(default=0)
	creation_datetime = models.DateTimeField('date created',auto_now=True)
	status = models.BooleanField(
        'Post_thread status',
        default=True,
        help_text='Designates whether the Post_thread is active or not.',
    )
	def __str__(self):
		return str(self.p_id.name+str(self.pt_id)+"status="+self.status)


class Tags(models.Model):
	t_id = models.AutoField(primary_key=True)
	tag_name = models.CharField(max_length=200,unique=True)
	no_of_use = models.IntegerField(default=0)
	def __str__(self):
		return str(self.tag_name+str(self.no_of_use))


class Post_tags(models.Model):
	pt_id = models.AutoField(primary_key = True)
	p_id = models.ForeignKey(Post,on_delete=models.CASCADE)
	t_id = models.ForeignKey(Tags,on_delete=models.CASCADE)
	class Meta:
		unique_together = ('p_id', 't_id',)

class Channel_tags(models.Model):
	ct_id = models.AutoField(primary_key = True)
	c_id = models.ForeignKey(Channel,on_delete=models.CASCADE)
	t_id = models.ForeignKey(Tags,on_delete=models.CASCADE)
	class Meta:
		unique_together = ('c_id', 't_id',)

class post_actions(models.Model):
	pa_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	p_id = models.ForeignKey(Post,on_delete=models.CASCADE)
	latest_datetime = models.DateTimeField('date created',auto_now=True)
	ld_status = models.NullBooleanField()
	report_status = models.NullBooleanField()
	class Meta:
		unique_together = ('u_id', 'p_id',)

class post_file_actions(models.Model):
	pfa_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	pf_id = models.ForeignKey(Post_files,on_delete=models.CASCADE)
	latest_datetime = models.DateTimeField('date created',auto_now=True)
	ld_status = models.NullBooleanField()
	report_status = models.NullBooleanField()
	class Meta:
		unique_together = ('u_id', 'pf_id',)

class channel_thread_actions(models.Model):
	cta_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	ct_id = models.ForeignKey(Channel_threads,on_delete=models.CASCADE)
	latest_datetime = models.DateTimeField('date created',auto_now=True)
	ld_status = models.NullBooleanField()
	report_status = models.NullBooleanField()
	class Meta:
		unique_together = ('u_id', 'ct_id',)

class post_thread_actions(models.Model):
	pta_id = models.AutoField(primary_key = True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	pt_id = models.ForeignKey(Post_threads,on_delete=models.CASCADE)
	latest_datetime = models.DateTimeField('date created',auto_now=True)
	ld_status = models.NullBooleanField()
	report_status = models.NullBooleanField()
	class Meta:
		unique_together = ('u_id', 'pt_id',)

class channel_actions(models.Model):
	ca_id = models.AutoField(primary_key=True)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	c_id = models.ForeignKey(Channel,on_delete=models.PROTECT)
	report_status = models.NullBooleanField()
	class Meta:
		unique_together = ('u_id', 'c_id',)


class Dowload_history(models.Model):
	dw_id = models.AutoField(primary_key=True)
	pf_id = models.ForeignKey(Post_files,on_delete=models.PROTECT)
	u_id = models.ForeignKey(User,on_delete=models.PROTECT)
	download_datetime = models.DateTimeField('date downloded',auto_now=True)
		