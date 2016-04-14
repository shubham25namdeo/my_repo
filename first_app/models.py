# Create your models here.
import datetime
from django.utils.timezone import utc

from django.db import models
from django.contrib.auth.models import User
import PIL

from ckeditor.fields import RichTextField

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'

class CommentForm(models.Model):
    logged_inuser = models.CharField(max_length=30,blank=True)
    comment = models.CharField(max_length=200)
    dates = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    class Meta:
        verbose_name_plural=u'Chats'

class Note(models.Model):
    logged_user = models.CharField(max_length=30,blank=True)
    title = models.TextField(max_length=20)
    notes = models.CharField(max_length=200)
    dates = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    class Meta:
        verbose_name_plural=u'Notes'

class Art(models.Model):
    title = models.TextField(max_length=20)
    desc = models.CharField(max_length=200)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', default="")
    dates = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    class Meta:
        verbose_name_plural=u'Articles'

class Word(models.Model):
    texts = RichTextField(('Content'))
    dates = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    class Meta:
        verbose_name_plural=u'Documents'
#
class Consultant(models.Model):
    cname = models.TextField(max_length=200, blank=False)
    projtype = models.CharField(max_length=200, blank=False)
    location = models.CharField(max_length=200)
    joindate = models.DateField()
    resume = models.FileField(upload_to='documents/%Y/%m/%d', default="")
    JD = models.CharField(max_length=200)
    log_user = models.CharField(max_length=30,null=False)
    dates = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    class Meta:
        verbose_name_plural=u'Consultants'
