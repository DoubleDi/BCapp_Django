# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BcUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('facebookurl', models.URLField()),
                ('karma', models.IntegerField(default=0)),
                ('date_of_birth', models.DateField(null=True, verbose_name=b'date of birth', blank=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('text', models.TextField(verbose_name=b'text', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'BC User',
                'verbose_name_plural': 'BC Users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=40, verbose_name=b'header')),
                ('text', models.TextField(verbose_name=b'text')),
            ],
            options={
                'verbose_name': 'Advice',
                'verbose_name_plural': 'Advices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name=b'text')),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'last modified datetime')),
                ('owner', models.ForeignKey(verbose_name=b'owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatabaseMonster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stype', models.CharField(max_length=30, verbose_name=b'type')),
                ('name', models.CharField(max_length=40, verbose_name=b'name')),
                ('karma', models.IntegerField()),
                ('picture', models.ImageField(upload_to=b'/home/doubledi/Documents/django/Mydjango/generatefiles/media/', verbose_name=b'picture', blank=True)),
                ('evolution', models.ForeignKey(related_name=b'evo', verbose_name=b'evolution', blank=True, to='bcapp.DatabaseMonster', null=True)),
                ('preevolution', models.ForeignKey(related_name=b'preevo', verbose_name=b'preevolution', blank=True, to='bcapp.DatabaseMonster', null=True)),
            ],
            options={
                'verbose_name': 'Datebase Monster',
                'verbose_name_plural': 'Database Monsters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(verbose_name=b'Like', to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(verbose_name=b'owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name=b'text')),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'time')),
                ('owner', models.ForeignKey(related_name=b'owner', verbose_name=b'owner', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name=b'sender', verbose_name=b'sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('powerraiting', models.PositiveIntegerField(null=True, blank=True)),
                ('zodiac', models.CharField(max_length=20, verbose_name=b'zodiac')),
                ('stype', models.CharField(max_length=30, verbose_name=b'type')),
                ('name', models.CharField(max_length=40, verbose_name=b'name')),
                ('active', models.CharField(max_length=40, verbose_name=b'active')),
                ('passive', models.CharField(max_length=40, verbose_name=b'passive')),
                ('picture', models.ImageField(upload_to=b'/home/doubledi/Documents/django/Mydjango/generatefiles/media/', verbose_name=b'picture', blank=True)),
                ('owner', models.ForeignKey(verbose_name=b'owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Monster',
                'verbose_name_plural': 'Monsters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=254, verbose_name=b'header')),
                ('text', models.TextField(verbose_name=b'text')),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'last modified datetime')),
                ('ptype', models.CharField(max_length=30, verbose_name=b'post type')),
                ('owner', models.ForeignKey(verbose_name=b'owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', models.CharField(max_length=40, verbose_name=b'header', blank=True)),
                ('stype', models.CharField(max_length=40, verbose_name=b'type')),
                ('is_avatar', models.BooleanField(default=False)),
                ('picture', models.ImageField(upload_to=b'/home/doubledi/Documents/django/Mydjango/generatefiles/media/', verbose_name=b'picture', blank=True)),
                ('owner', models.ForeignKey(verbose_name=b'owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'screenshot',
                'verbose_name_plural': 'screenshots',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TradePost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name=b'text')),
                ('header', models.CharField(max_length=40, verbose_name=b'header')),
                ('date', models.DateTimeField(auto_now=True, verbose_name=b'time')),
                ('monster', models.ForeignKey(verbose_name=b'monster', to='bcapp.Monster')),
            ],
            options={
                'verbose_name': 'Tradepost',
                'verbose_name_plural': 'Tradeposts',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(verbose_name=b'post', to='bcapp.Post'),
            preserve_default=True,
        ),
    ]
