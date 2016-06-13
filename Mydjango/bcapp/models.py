from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser


class BcUser(AbstractUser):
    facebookurl = models.URLField()
    #karma = models.IntegerField(default = 0)
    date_of_birth = models.DateField(verbose_name = "date of birth",  blank = True, null = True)
    is_admin = models.BooleanField(default = False)
    text = models.TextField("text", blank = True)
    avatar = models.ImageField(upload_to="to/", blank=True, verbose_name="avatar", null = True)
    view = models.PositiveIntegerField(default = 0)
    class Meta:
        verbose_name = "BC User"
        verbose_name_plural = "BC Users"


class Monster(models.Model):
    powerraiting = models.PositiveIntegerField(blank = True, null = True)
    zodiac = models.CharField("zodiac", max_length = 20)
    stype = models.CharField("type", max_length = 30)
    name = models.CharField("name", max_length = 40)
    active = models.CharField("active", max_length = 40)
    passive = models.CharField("passive", max_length = 40)
    owner = models.ForeignKey(BcUser, verbose_name = "owner")
    picture = models.ImageField(upload_to="to/", blank=True, verbose_name="picture")

    class Meta:
        verbose_name = "Monster"
        verbose_name_plural = "Monsters"

    def __unicode__(self):
        return self.name
    

class Screenshot(models.Model):
    header = models.CharField("header", max_length = 40, blank = True)
    owner = models.ForeignKey(BcUser, verbose_name = "owner")
    stype = models.CharField("type", max_length = 40) #archive, onpage
    picture = models.ImageField(upload_to="to/", blank=True, verbose_name="picture")

    class Meta:
        verbose_name = "screenshot"
        verbose_name_plural = "screenshots"

    def __unicode__(self):
        return self.header


class DatabaseMonster(models.Model):
    stype = models.CharField("type", max_length = 30)
    name = models.CharField("name", max_length = 40)
    #karma = models.IntegerField()
    evolution = models.ForeignKey("DatabaseMonster", verbose_name = "evolution", blank = True, null = True,  related_name = 'evo')
    preevolution = models.ForeignKey("DatabaseMonster", verbose_name = "preevolution", blank = True, null = True, related_name = 'preevo')
    picture = models.ImageField(upload_to="to/", blank=True, verbose_name="picture")
          
    class Meta:
        verbose_name = "Datebase Monster"
        verbose_name_plural = "Database Monsters"

    def __unicode__(self):
        return self.name

class Like(models.Model):
    owner = models.ForeignKey(BcUser, verbose_name = "owner")
    content_type = models.ForeignKey(ContentType, verbose_name="Like")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
    
    def __unicode__(self):
        return self.owner.username


class Post(models.Model):
    header = models.CharField("header", max_length=254)
    text = models.TextField("text")
    date = models.DateTimeField("last modified datetime", auto_now = "True")
    ptype = models.CharField("post type", max_length = 30) #archive, onpage
    owner = models.ForeignKey(BcUser, verbose_name = "owner")
    view = models.PositiveIntegerField(default = 0)
    #like

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __unicode__(self):
        return self.header


class Comment(models.Model):
    text = models.TextField("text")
    date = models.DateTimeField("last modified datetime", auto_now = "True")
    owner = models.ForeignKey(BcUser, verbose_name = "owner")
    post = models.ForeignKey(Post, verbose_name = "post")
    #like

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __unicode__(self):
        return self.post.header

class TradePost(models.Model):
    text = models.TextField("text")
    header = models.CharField("header", max_length = 40)
    monster = models.ForeignKey(Monster, verbose_name = "monster")
    #owner -> Monster -> BcUser
    date = models.DateTimeField("time", auto_now = "True")

    class Meta:
        verbose_name = "Tradepost"
        verbose_name_plural = "Tradeposts"

    def __unicode__(self):
        return self.header


class Message(models.Model):
    text = models.TextField("text")
    owner = models.ForeignKey(Monster, verbose_name = "to_monster", related_name = "to_monster")
    sender = models.ForeignKey(Monster, verbose_name = "from_monster", related_name = "from_monster") 
    date = models.DateTimeField("time", auto_now = "True")
    accepted = models.CharField("accepted", max_length = 30, blank = True, null = True)
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"   
    
    def __unicode__(self):
        return self.owner.name

class Advice(models.Model):
    header = models.CharField("header", max_length = 40)
    text = models.TextField("text")

    class Meta:
        verbose_name = "Advice"
        verbose_name_plural = "Advices"   

    def __unicode__(self):
        return self.header

