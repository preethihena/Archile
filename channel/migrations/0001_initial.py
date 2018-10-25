# Generated by Django 2.1.2 on 2018-10-25 18:03

import channel.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('user_id', models.IntegerField(unique=True, verbose_name='user_id')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('token', models.CharField(blank=True, max_length=1000, verbose_name='token')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', channel.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(default='', max_length=500)),
                ('logo', models.ImageField(blank=True, upload_to='channel_logo_images')),
                ('no_of_subscriptions', models.IntegerField(default=0)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('status', models.BooleanField(default=True, help_text='Designates whether the Channel is active or not.', verbose_name='Channel status')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='channel_actions',
            fields=[
                ('ca_id', models.AutoField(primary_key=True, serialize=False)),
                ('report_status', models.NullBooleanField()),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Channel_tags',
            fields=[
                ('ct_id', models.AutoField(primary_key=True, serialize=False)),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='channel_thread_actions',
            fields=[
                ('cta_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('ld_status', models.NullBooleanField()),
                ('report_status', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Channel_threads',
            fields=[
                ('ct_id', models.AutoField(primary_key=True, serialize=False)),
                ('typ', models.CharField(choices=[('A', 'Assertive'), ('Q', 'Question')], max_length=200)),
                ('description', models.CharField(default='', max_length=500)),
                ('no_of_likes', models.IntegerField(default=0)),
                ('no_of_dislikes', models.IntegerField(default=0)),
                ('no_of_reports', models.IntegerField(default=0)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('status', models.BooleanField(default=True, help_text='Designates whether the Channel_thread is active or not.', verbose_name='Channel_thread status')),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Channel')),
                ('ct_id_reply_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Channel_threads')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('p_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(default='', max_length=500)),
                ('no_of_likes', models.IntegerField(default=0)),
                ('no_of_dislikes', models.IntegerField(default=0)),
                ('no_of_reports', models.IntegerField(default=0)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('status', models.BooleanField(default=True, help_text='Designates whether the Post is active or not.', verbose_name='Post status')),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Channel')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='post_actions',
            fields=[
                ('pa_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('ld_status', models.NullBooleanField()),
                ('report_status', models.NullBooleanField()),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Post')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='post_file_actions',
            fields=[
                ('pfa_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('ld_status', models.NullBooleanField()),
                ('report_status', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Post_files',
            fields=[
                ('pf_id', models.AutoField(primary_key=True, serialize=False)),
                ('file_type', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='post_files/')),
                ('upload_datetime', models.DateTimeField(auto_now_add=True, verbose_name='upload date and time')),
                ('no_of_likes', models.IntegerField(default=0)),
                ('no_of_dislikes', models.IntegerField(default=0)),
                ('no_of_reports', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=True, help_text='Designates whether the File uploaded is active or not.', verbose_name='Post status')),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Post_tags',
            fields=[
                ('pt_id', models.AutoField(primary_key=True, serialize=False)),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Post')),
            ],
        ),
        migrations.CreateModel(
            name='post_thread_actions',
            fields=[
                ('pta_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('ld_status', models.NullBooleanField()),
                ('report_status', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Post_threads',
            fields=[
                ('pt_id', models.AutoField(primary_key=True, serialize=False)),
                ('typ', models.CharField(choices=[('A', 'Assertive'), ('Q', 'Question')], max_length=200)),
                ('description', models.CharField(default='', max_length=500)),
                ('no_of_likes', models.IntegerField(default=0)),
                ('no_of_dislikes', models.IntegerField(default=0)),
                ('no_of_reports', models.IntegerField(default=0)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('status', models.BooleanField(default=True, help_text='Designates whether the Post_thread is active or not.', verbose_name='Post_thread status')),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Post')),
                ('pt_id_reply_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Post_threads')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('s_id', models.AutoField(primary_key=True, serialize=False)),
                ('s_datetime', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Channel')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('t_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_name', models.CharField(max_length=200)),
                ('no_of_use', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='post_thread_actions',
            name='pt_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Post_threads'),
        ),
        migrations.AddField(
            model_name='post_thread_actions',
            name='u_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post_tags',
            name='t_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Tags'),
        ),
        migrations.AddField(
            model_name='post_file_actions',
            name='pf_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Post_files'),
        ),
        migrations.AddField(
            model_name='post_file_actions',
            name='u_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='channel_thread_actions',
            name='ct_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Channel_threads'),
        ),
        migrations.AddField(
            model_name='channel_thread_actions',
            name='u_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='channel_tags',
            name='t_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Tags'),
        ),
    ]
