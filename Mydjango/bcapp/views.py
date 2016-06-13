from random import randint, choice
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
import datetime, json
from django.core.context_processors import csrf
#from django.template import Template, Context
#from django.template.loader import get_template
from django.shortcuts import render_to_response, RequestContext
from bcapp.models import BcUser, Monster, Screenshot, DatabaseMonster, Like, Post, TradePost, Comment, Message, Advice
from django.contrib import auth
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required


def hello(request):
    return HttpResponse("HI!")

def current_datetime(request):
    now = datetime.datetime.now()
    # Simple way of using templates from the filesystem.
    # This doesn't account for missing files!
#    fp = open('/home/doubledi/Documents/django/Mydjango/Mydjango/template.html')
#    t = Template(fp.read())
 #   fp.close()
# or 
#    t = get_template('template.html')
#    html = t.render(Context({'current_date': now}))
#       return HttpResponse(html)
    return render_to_response('template.html', {'current_date': now})


def user(request, offset):
    flag = False
    u = BcUser.objects.get(id = offset)
    monster_list = Monster.objects.filter(owner = u).order_by('-id')[:10]
    db = DatabaseMonster.objects.all()
    pagephoto = Screenshot.objects.filter(owner = u).order_by('-id')[0:3]
    likes = Like.objects.filter(object_id = offset, content_type = ContentType.objects.get_for_model(BcUser)).count()
    likeflag = False
    if request.user.is_authenticated():
        user = request.user
        if Like.objects.filter(owner = request.user, content_type = ContentType.objects.get_for_model(BcUser), object_id = offset).count():
            likeflag = True
        if int(user.id) == int(offset):
            flag = True
    else:
        user = 0
    u.view += 1
    u.save()
    return render_to_response('me.html', { 'monster_list': monster_list, 'user':  u, 'number_monsters': Monster.objects.filter(owner = u).count(), 'login_user': user, 'flag': flag, 'pagephoto': pagephoto, 'database': db, 'likes': likes, 'like': likeflag }, context_instance=RequestContext(request) )


def main(request, offset):
#anotate group by
    post_list = Post.objects.select_related('owner')[str(int(offset) * 5 - 5):str(int(offset) * 5)]
    a = Post.objects.all().count()
    prev = int(offset) - 1
    succ = int(offset) + 1
    current = (succ - 1) * 3 
    advice = choice(Advice.objects.all())
    likes = Like.objects.filter(content_type = ContentType.objects.get_for_model(Post))
    likeflag = False
    if request.user.is_authenticated():
        user = request.user
        if Like.objects.filter(owner = request.user, content_type = ContentType.objects.get_for_model(Post), object_id = offset).count():
            likeflag = True
    else:
        user = 0
    return render_to_response('main.html', { 'post_list': post_list, 'advice': advice, 'prev': prev, 'succ': succ, 'all': a, 'current': current, 'user': user, 'likes': likes, 'like': likeflag }, context_instance=RequestContext(request) )
    

def trade(request, offset):
    tradepost_list = TradePost.objects.order_by('-date')[str(int(offset) * 10 - 10):str(int(offset) * 10)].select_related('monster', 'monster__owner')
    a = TradePost.objects.all().count()
    prev = int(offset) - 1
    succ = int(offset) + 1
    current = (succ - 1) * 10 
    advice = choice(Advice.objects.all())
    monsters = {}
    if request.user.is_authenticated():
        user = request.user
        monsters = Monster.objects.filter(owner = user)
    else:
        user = 0
    return render_to_response('trades.html', { 'tradepost_list': tradepost_list, 'advice': advice, 'prev': prev, 'succ': succ, 'all': a, 'current': current, 'user': user, 'monsters': monsters }, context_instance=RequestContext(request))


def database(request, offset):
    db = DatabaseMonster.objects.all()[str(int(offset) * 10 - 10):str(int(offset) * 10)]
    a = DatabaseMonster.objects.all().count()
    prev = int(offset) - 1
    succ = int(offset) + 1
    current = (succ - 1) * 10 
    advice = choice(Advice.objects.all())
    likes = Like.objects.filter(object_id = offset, content_type = ContentType.objects.get_for_model(DatabaseMonster)).count()
    likeflag = False
    if request.user.is_authenticated():
        user = request.user
        if Like.objects.filter(owner = request.user, content_type = ContentType.objects.get_for_model(DatabaseMonster), object_id = offset).count():
            likeflag = True
    else:
        user = 0
    return render_to_response('database.html', { 'database': db, 'advice': advice, 'prev': prev, 'succ': succ, 'all': a, 'current': current, 'user': user }, context_instance=RequestContext(request))


def post_comment(request, offset):
    post_show = Post.objects.get(id = offset)
    comments = Comment.objects.filter(post = post_show).select_related('owner')
    advice = choice(Advice.objects.all())
    likes = Like.objects.filter(object_id = offset, content_type = ContentType.objects.get_for_model(Post)).count()
    likeflag = False
    if request.user.is_authenticated():
        user = request.user
        if Like.objects.filter(owner = request.user, content_type = ContentType.objects.get_for_model(Post), object_id = offset).count():
            likeflag = True
    else:
        user = 0
    likes = Like.objects.filter(content_type = ContentType.objects.get_for_model(Post), object_id = offset).count()
    post_show.view += 1
    post_show.save()
    return render_to_response('post.html', { 'post': post_show, 'advice': advice, 'number_comments': Comment.objects.filter(post = post_show).count(), 'comment_list': comments, 'user': user, 'likes': likes, 'like': likeflag }, context_instance=RequestContext(request))


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def search(request):
    advice = choice(Advice.objects.all())
    if 'q' in request.GET and request.GET['q']:
        message = 'You searched for: %r' % request.GET['q']
        q = request.GET['q']
        users = BcUser.objects.filter(username = q)
    else:
        message = 'You submitted an empty form.'
        users = {}
    if request.user.is_authenticated():
        user = request.user
    else:
        user = 0
    return render_to_response('search.html', { 'advice': advice, 'message': message, 'all': users.count(), 'user_list': users, 'login_user': user }, context_instance=RequestContext(request))
   # else:
    #    return HttpResponse("<script>alert('Search field is empty')</script>")


def regform(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = 0
    return render_to_response('regform.html', {'user': user	})


def a(request):
    return render_to_response('a.html', { })


def login(request):
    #c.update(csrf(request))
    username = request.POST.get('usernamee', False)
    password = request.POST.get('passworde', False)
    if not request.user.is_authenticated():
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
 #           messages.success(request, 'You have successfully logged in as %s' % username)
        else:
  #          messages.error(request, 'You have failed to log in as %s' % username)
            user = 0
    else:
        user = request.user
   #     messages.error(request, 'You are already logged in as %s' % username)
    #return render_to_response('regform.html', {'user': user}, context_instance=RequestContext(request))
    return HttpResponseRedirect("%s" % request.META['HTTP_REFERER'])

def logout(request):
    auth.logout(request)
    #return HttpResponseRedirect("%s" % request.META['HTTP_REFERER'])
    return HttpResponseRedirect("/main/1")
    

def me(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/auth/?=next%s' % request.path)
    else:
        return HttpResponseRedirect('/user/%s' % request.user.id)


def register(request):
    us = request.POST.get('username', False)
    pas = request.POST.get('password', False)
    fb = request.POST.get('facebookurl', False)
    pas_confirm = request.POST.get('password_confirm', False)
    if str(pas) == str(pas_confirm):
        if (BcUser.objects.filter(username = us)):
            p = "There already is a user with such a username! Maybe you should login?"
        else:
            TheUser = BcUser.objects.create(username = us, password = pas, facebookurl = fb, last_login = datetime.datetime.now())
            TheUser.set_password(pas)
            TheUser.save()
            p = "You have Successfully registered!"
    else:
        p = "Passwords don't match"
    return HttpResponse(p)


def addcomment(request, offset):
    t = request.POST.get('text', False)
    comment = Comment.objects.create(owner = request.user, post = Post.objects.get(id = offset), date = datetime.datetime.now(), text = t)
    st = '<div class="media"><p class="pull-right blog-post-meta"><small>' + str(comment.date) + '</small></p><a class="media-left" href="/user/' + str(comment.owner.id) + '"><img src="/media/' + str(comment.owner.avatar) + '"></a><div class="media-body"><a href="/user/' + str(comment.owner.id) + '"><h4 class="media-heading user_name">' + str(comment.owner.username) + '</h4></a>' + str(comment.text) + '<p class="blog-post-meta">Likes: <a class="btn btn btn-primary pull-right" id="hide">Like</a></p></div></div>'    
    return HttpResponse(st)


def edittext(request):
    t = request.POST['text']
    user = request.user
    user.text = t
    user.save()
    return HttpResponseRedirect("%s" % request.META['HTTP_REFERER'])

def addmonster(request):
    mname = request.POST.get('monster', False)
    mname = mname+'\n'
    pas = request.POST.get('passive', False)
    act = request.POST.get('active', False)
    zod = request.POST.get('zodiac', False)
    pr = request.POST.get('pr', False)
    m = DatabaseMonster.objects.get(name = mname)
    monster = Monster.objects.create(owner = request.user, passive = pas, active = act, name = mname, picture = m.picture, stype = m.stype, zodiac = zod, powerraiting = int(pr))
    st = """      
       <div class="media mon_ster id""" + str(monster.id) + """">
       <div class="media">
        <div class="media-left">
         <img class="media-object monster" src="/media/""" + str(monster.picture) +"""" alt="monster">
        </div>
        <div class="media-body">
          <h4 class="media-heading"> """ + str(monster.name) + """ 
          <a class="btn btn-lg btn-primary edit_button" data-id = '""" + str(monster.id) + """' data-toggle="modal" data-target=".editmonster" role="button"> Edit Monster</a>
          <a class="btn btn-lg btn-primary delete_button" data-id = '""" + str(monster.id) + """' role="button"> Delete Monster</a>
          </h4>
            <br>
          <div class="mo id""" + str(monster.id) + """">
          <p>Powerraiting: """ + str(monster.powerraiting) + """</p>
          <p>""" + str(monster.zodiac) +""", """ + str(monster.active) +""" /  """ + str(monster.passive) +"""</p>
        </div>
       </div>
      </div>
      </div>""" 
    return HttpResponse(st)



def addtradepost(request):
    txt = request.POST.get('text', False)
    head = request.POST.get('header', False)
    i = request.POST.get('monster', False)
    i = i + '\n';
    m = Monster.objects.get(owner = request.user, name = i)
    tradepost = TradePost.objects.create(text = txt, date = datetime.datetime.now(), header = head, monster = m)
    st = """ <div class="media blog-post trade_post id""" +  str(tradepost.id) +"""">
        <div class="media-left">
         <img class="media-object monster" src="/media/""" +  str(tradepost.monster.picture) +"""" alt="monster">
        </div>
        <div class="media-body">
          <h4 class="media-heading">""" +  str(tradepost.monster.name) +""" 
          <a class="btn btn-lg btn-primary edit_button" data-id = '""" +  str(tradepost.id) +"""' href="#signup" data-toggle="modal" data-target=".edittradepost" role="button">Edit</a>
          <a class="btn btn-lg btn-primary delete_button" href="#deletemonster" data-id = '""" +  str(tradepost.id) +"""' data-toggle="modal" data-target=".deletemonster" role="button"> Delete</a>
          </h4>
          <p>""" +  str(tradepost.monster.stype) +""", """ +  str(tradepost.monster.active) +""" / """ +  str(tradepost.monster.passive) +"""</p>
          <div class = "tp id""" +  str(tradepost.id) +"""">
          <h2><p>""" +  str(tradepost.header) +"""</p></h2>
          <p>""" +  str(tradepost.text) +"""</p>
          </div>
          <p>Posted by <a href = "/user/""" +  str(tradepost.monster.owner.id) +"""">""" +  str(tradepost.monster.owner.username) +"""</a></p>
        </div>
      </div>"""
    return HttpResponse(st)


def search_monster(request):
        phrase = request.POST.get('phrase')
        if phrase:
            searchmonsters = Monster.objects.filter(name__icontains=phrase, owner = request.user)
            return render(request, {'searchmonsters': searchmonsters})

def edittradepost(request):
    txt = request.POST.get('text', False)
    head = request.POST.get('header', False)
    i = request.POST.get('id', False)
    tradepost = TradePost.objects.get(id = i)
    if head:
        tradepost.header = head
    if txt:
        tradepost.text = txt
    tradepost.save()
    st = """ <h2><p>""" + str(tradepost.header) + """</p></h2>
          <p>""" + str(tradepost.text) + """</p>"""
    return HttpResponse(st)


def editmonster(request):
    zod = request.POST.get('zodiac', False)
    pas = request.POST.get('passive', False)
    act = request.POST.get('active', False)
    pr = request.POST.get('pr', False)
    i = request.POST.get('id', False)
    monster = Monster.objects.get(id = i)
    if zod:
        monster.zodiac = zod
    if pas:
        monster.passive = pas
    if act:
        monster.active = act
    if pr:
        monster.powerraiting = pr
    monster.save()
    st = """<p>Powerraiting: """ + str(monster.powerraiting) + """</p>
          <p>""" + str(monster.zodiac) + """, """ + str(monster.active) + """ / """ + str(monster.passive) + """</p>"""
    return HttpResponse(st)


def deletetradepost(request):
    i = request.POST.get('id', False)
    tradepost = TradePost.objects.get(id = i)
    tradepost.delete()
    st = "success"
    return HttpResponse(st)


def deletemonster(request):
    i = request.POST.get('id', False)
    monster = Monster.objects.get(id = i)
    monster.delete()
    st = "success"
    return HttpResponse(st)


def addlikeu(request):
    i = request.POST.get('id', False)
    like = Like.objects.create(owner = request.user, content_type = ContentType.objects.get_for_model(BcUser),  object_id = i)
    likes = "Likes: " + str(Like.objects.filter(content_type = ContentType.objects.get_for_model(BcUser),  object_id = i).count()) 
    return HttpResponse(likes)


def removelikeu(request):
    i = request.POST.get('id', False)
    like = Like.objects.get(owner = request.user, content_type = ContentType.objects.get_for_model(BcUser),  object_id = i)
    like.delete()
    likes = "Likes: " + str(Like.objects.filter(content_type = ContentType.objects.get_for_model(BcUser),  object_id = i).count()) 
    return HttpResponse(likes)


def addliked(request):
    i = request.POST.get('id', False)
    like = Like.objects.create(owner = request.user, content_type = ContentType.objects.get_for_model(DatabaseMonster),  object_id = i)
    likes = "<br>Likes: " + str(Like.objects.filter(content_type = ContentType.objects.get_for_model(DatabaseMonster),  object_id = i).count()) 
    return HttpResponse(likes)


def addlikep(request):
    i = request.POST.get('id', False)
    like = Like.objects.create(owner = request.user, content_type = ContentType.objects.get_for_model(Post),  object_id = i)
    likes = "Likes: " + str(Like.objects.filter(content_type = ContentType.objects.get_for_model(Post),  object_id = i).count()) 
    return HttpResponse(likes)


def removelikep(request):
    i = request.POST.get('id', False)
    like = Like.objects.get(owner = request.user, content_type = ContentType.objects.get_for_model(Post),  object_id = i)
    like.delete()
    likes = "Likes: " + str(Like.objects.filter(content_type = ContentType.objects.get_for_model(Post),  object_id = i).count()) 
    return HttpResponse(likes)


def screenshots(request, offset):
    flag = False
    u = BcUser.objects.get(id = offset)
    pagephoto = Screenshot.objects.filter(stype = 'onpage', owner = u).order_by('-id')
    if request.user.is_authenticated():
        user = request.user
        if int(user.id) == int(offset):
            flag = True
    else:
        user = 0
    return render_to_response('screenshots.html', { 'user':  u, 'login_user': user, 'flag': flag, 'pagephoto': pagephoto }, context_instance=RequestContext(request) )


def deletescreenshot(request):
    i = request.POST.get('id', False)
    screenshot = Screenshot.objects.get(id = i)
    screenshot.delete()
    st = "success"
    return HttpResponse(st)


def addscreenshot(request):
    scr = request.POST.get('screenshot', False)
    scr = scr.replace("C:\\fakepath\\", "")
    screenshot = Screenshot.objects.create(header = "screenshot " + str(randint(0, 1000)), owner = request.user, stype = "onpage", picture = scr)
    st = """<span class="delete_screenshot id""" + str(screenshot.id) + """">
          <a class="btn btn-lg btn-primary delete_button" data-id = '""" + str(screenshot.id) + """' role="button">delete</a>
          <a href="#">
            <img class="screenshot" src="/media/""" + str(screenshot.picture) + """" alt="monster">
          </a>
        </span>
         
"""
    return HttpResponse(st)


def messages_mine(request, offset):
    flag = False
    u = BcUser.objects.get(id = offset)
    monst = Monster.objects.filter(owner = u)
    messages = []
    mymessages = Message.objects.filter(sender__owner = request.user).select_related('owner', 'owner__owner', 'sender', 'sender__owner').order_by('-date')
    if request.user.is_authenticated():
        user = request.user
        if int(user.id) == int(offset):
            flag = True
    else:
        user = 0
    return render_to_response('messages.html', { 'user':  u, 'login_user': user, 'flag': flag, 'message_list': messages, 'mymessage_list': mymessages }, context_instance=RequestContext(request))


def messages_other(request, offset):
    flag = False
    u = BcUser.objects.get(id = offset)
    monst = Monster.objects.filter(owner = u)
    messages = Message.objects.filter(owner__owner = u).select_related('owner', 'owner__owner', 'sender', 'sender__owner').order_by('-date')
    mymessages = []
    if request.user.is_authenticated():
        user = request.user
        if int(user.id) == int(offset):
            flag = True
    else:
        user = 0
    return render_to_response('messages.html', { 'user':  u, 'login_user': user, 'flag': flag, 'message_list': messages, 'mymessage_list': mymessages }, context_instance=RequestContext(request))


def accepttrade(request):
    i = request.POST.get('id', False)
    g = request.POST.get('goal', False)
    message = Message.objects.get(id = i)
    message.accepted = g
    message.save()
    if g == "yes":
        st = """<a class='btn btn-lg btn-success' href="" role='button'>Offer is accepted</a><br><br><br>"""
    else:
        st = """<a class='btn btn-lg btn-danger' href="" role='button'>Offer is declined	</a><br><br><br>"""
    return HttpResponse(st)

def addoffer(request):
    i = request.POST.get('id', False)
    txt = request.POST.get('text', False)
    m = request.POST.get('monster', False)
    m = m + '\n'
    message = Message.objects.create(owner = Monster.objects.get(id = i), sender = Monster.objects.get(name = m, owner = request.user), text = txt, date = datetime.datetime.now())
    st = "success"
    return HttpResponse(st)


def moremonsters(request):
    st = ""
    i = request.POST.get('id', False)
    u = request.POST.get('user', False)
    monster_list = Monster.objects.filter(owner = u).order_by('-id')[10*(int(i) - 1):10 * int(i)]
    for monster in monster_list:
        st += """<div class="media mon_ster id""" + str(monster.id) +"""">
        <div class="media-left">
         <img class="media-object monster" src="/media/""" + str(monster.picture) +"""" alt="monster">
        </div>
        <div class="media-body">
          <h4 class="media-heading"> """ + str(monster.name) +""" 
          <a class="btn btn-lg btn-primary edit_button" data-id = '""" + str(monster.id) +"""' data-toggle="modal" data-target=".editmonster" role="button"> Edit Monster</a>
          <a class="btn btn-lg btn-primary delete_button" data-id = '""" + str(monster.id) +"""' role="button"> Delete Monster</a>
          <a class="btn btn-lg btn-primary" href="../../components/#navbar" role="button"> Send an offer</a>
          </h4>
            <br>
          <div class="mo id""" + str(monster.id) +"""">
          <p>Powerraiting: """ + str(monster.powerraiting) +"""</p>
          <p>""" + str(monster.zodiac) +""", """ + str(monster.active) +""" / """ + str(monster.passive) +"""</p>
          </div>
        </div>
      </div>
""" 
    if (Monster.objects.filter(owner = u).count() > 10 * int(i)):
        i = int(i) + 1
        st +=  """<div class="text-center"><a class="btn btn-lg btn-primary moremonsters" role = "button" data-id = '"""+ str(i) +"""'>More</a></div>"""
    return HttpResponse(st)



def morecomments(request):
    st = ""
    i = request.POST.get('id', False)
    p = request.POST.get('post', False)
    comment_list = Comment.objects.filter(post = p).order_by('-id')[10*(int(i) - 1):10 * int(i)]
    for comment in comment_list:
        st += """<div class="media">
                           <p class="pull-right blog-post-meta"><small>""" + str(comment.date) + """</small></p>
                            <a class="media-left" href="/user/""" + str(comment.owner.id) + """">
                              <img src="/media/""" + str(comment.owner.avatar) + """">
                            </a>
                  <div class="media-body">
                                
                              <a href="/user/""" + str(comment.owner.id) + """"><h4 class="media-heading user_name">""" + str(comment.owner.username) + """</h4></a>
                              """ + str(comment.text) + """
                              <p class="blog-post-meta">Likes: <a class="btn btn btn-primary pull-right" id="hide">Like</a></p>
                  </div>
                </div>""" 
    if (Comment.objects.filter(post = p).count() > 10 * int(i)):
        i = int(i) + 1
        st +=  """<div class="text-center"><a class="btn btn-lg btn-primary moremonsters" role = "button" data-id = '"""+ str(i) +"""'>More</a></div>"""
    return HttpResponse(st)


