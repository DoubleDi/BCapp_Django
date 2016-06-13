from random import randint, choice, seed
import MySQLdb
import datetime
from bcapp.models import BcUser, Monster, Screenshot, DatabaseMonster, Like, Post, TradePost, Comment, Message, Advice
from django.core.files import File
from django.contrib.contenttypes.models import ContentType
import os
import django




def GenerateUsers(n):
    sur_file = open('generatefiles/surnames.txt', 'r')
    last_file = open('generatefiles/lastname.txt', 'r')
    game_file = open('generatefiles/gamename.txt', 'r')
    mess_file = open('generatefiles/posts.txt', 'r')
    messages = mess_file.readlines()
    surname = sur_file.readlines()
    lastname = last_file.readlines()
    gamename = game_file.readlines()
    seed()
    mail = ['yandex.ru', 'mail.ru', 'google.com']
    for i in range(n):
        t = gamename[i]
        t = t[0:-1]
        p = randint(0,1000)
        TheUser = BcUser.objects.create(facebookurl = 'https://www.facebook.com/' + t, username = t + str(p), first_name = surname[i], last_name = lastname[i], date_of_birth = datetime.datetime.now(), is_admin = False, password = t + "123", email = t + "@" + choice(mail), text = choice(messages), avatar = File(open('generatefiles/media/' + str(randint(1, 500)) + '.png')))
        t = t + str(p) + "123"
        TheUser.set_password(t)
        TheUser.save()
    sur_file.close()
    last_file.close()
    game_file.close()
    mess_file.close()


def GenerateMonsters(n):
    monst_file  = open('generatefiles/monsters.txt')
    act_file  = open('generatefiles/actives.txt')
    pass_file  = open('generatefiles/passives.txt')
    zod = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius']
    activelist = act_file.readlines()
    passivelist = pass_file.readlines()
    users = BcUser.objects.all()
    for i in range(n):
        monster = choice(DatabaseMonster.objects.all())
        Monster.objects.create(powerraiting = randint(0, 100000), stype = monster.stype, zodiac = choice(zod), name = monster.name, owner = choice(users), active = choice(activelist), passive = choice(passivelist), picture = monster.picture) 
    act_file.close()
    pass_file.close()


def GeneratePosts(n):
    post_file = open('generatefiles/posts.txt', 'r')
    posts = post_file.readlines()
    for i in range(0, n):
        Post.objects.create(header = 'post ' + str(randint(0, 1000)), text = choice(posts), date = datetime.datetime.now(), ptype = "onpage", owner = choice(BcUser.objects.all()))
    post_file.close()


def GenerateComments(n):
    comment_file = open('generatefiles/posts.txt', 'r')
    comments = comment_file.readlines()
    users = BcUser.objects.all()
    posts = Post.objects.all()
    for p in posts:
        for i in range(0, 20): 
            Comment.objects.create(text = comments[0], date = datetime.datetime.now(), owner = choice(users), post = p)
    comment_file.close()


def GenerateDatabaseMonsters():
    monst_file  = open('generatefiles/monsters.txt')
    monstername = monst_file.readlines()
    st = ['fire', 'water', 'wind', 'rock', 'leaf']
    for i in range(1, 501):
        DatabaseMonster.objects.create(stype = choice(st), name = monstername[i], picture = File(open('generatefiles/media/' + str(i) + '.png')))
#, evolution = choice(DatabaseMonster.objects.all()), preevolution = choice(DatabaseMonster.objects.all()))
    monst_file.close()


def GenerateScreenshots(n):
    for i in range(n):
        Screenshot.objects.create(header = "screenshot " + str(randint(0, 1000000)), owner = choice(BcUser.objects.all()), stype = "onpage", picture = File(open('generatefiles/media/' + str(randint(1, 500)) + '.png')))	


def GenerateLikesP(n):
    p_list = Post.objects.all()
    i = 0
    for p in p_list:
        i += 1
        if i > n:
            break
    Like.objects.create(owner = choice(BcUser.objects.all()), content_type = ContentType.objects.get_for_model(Post),  object_id = p.id) 


def GenerateLikesC(n):
    c_list = Comment.objects.all()
    i = 0
    for c in c_list:
        i += 1
        if i > n:
            break
        Like.objects.create(owner = choice(BcUser.objects.all()), content_type = ContentType.objects.get_for_model(Comment),  object_id = c.id) 


def GenerateLikesU(n):
    for i in range(n):
       Like.objects.create(owner = choice(BcUser.objects.all()), content_type = ContentType.objects.get_for_model(BcUser),  object_id = choice(BcUser.objects.all()).id) 


def GenerateLikesD(n):
    for i in range(n):
       Like.objects.create(owner = choice(BcUser.objects.all()), content_type = ContentType.objects.get_for_model(DatabaseMonster),  object_id = choice(DatabaseMonster.objects.all()).id) 


def GenerateTradePosts(n):
    mess_file = open('generatefiles/posts.txt')
    messages = mess_file.readlines()
    m_list = Monster.objects.all()
    i = 0
    for m in m_list:
        i += 1
        if (i > n):
            break
        TradePost.objects.create(text = messages[0], date = datetime.datetime.now(), header = "tradepost " + str(randint(0, 1000000)), monster = m)
    mess_file.close()


def GenerateMessages(n):
    mess_file = open('generatefiles/posts.txt')
    messages = mess_file.readlines()
    owners = Monster.objects.all().select_related('owner')
    i = 0    
    for ow in owners:
        i += 1
        if i > n:
            break
        sen = choice(Monster.objects.exclude(owner=ow.owner))
        Message.objects.create(text = messages[0], date = datetime.datetime.now(), owner = ow, sender = sen)
    mess_file.close()


def GenerateAdvice(n):
    with open('generatefiles/posts.txt') as adv_file:
        adv = adv_file.readlines()
        for i in range(n):
            Advice.objects.create(header="Battle camper rule " + str(randint(0, 1000000)), text=adv[0])


