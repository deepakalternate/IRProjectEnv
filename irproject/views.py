# --> IMPORTS BEGIN <--

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Users, FriendStatus, FriendValue, Queries, QueriesReceived, Answers
from .forms import SignUpForm, LoginForm, QueryForm, IntimacyForm, TopicForm, AnswerForm, RatingForm


import os
import pickle
import csv
import time

# --> IMPORTS END <--

# --> FILE PATHS  START<--

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP_DIR = os.path.join(BASE_DIR, "dump")
QUERY_DIR = os.path.join(DUMP_DIR, "queries")
ANS_DIR = os.path.join(DUMP_DIR, "answers")
USER_DIR = os.path.join(DUMP_DIR, "userinterests")

# --> FILE PATHS END <--

# --> USEFUL FUNCTIONS START <--


def getAllUsers():

    query_results = Users.objects.all()

    allusers = []
    for user in query_results:
        allusers.append(user.username)

    return allusers


def getAllFriends(user_id):

    friends_as_sender = FriendStatus.objects.filter(req_sender=user_id, status="ACCEPTED")
    friends_as_receiver = FriendStatus.objects.filter(req_receiver=user_id, status="ACCEPTED")

    allfriends = []
    for friend in friends_as_sender:
        allfriends.append(friend.req_receiver.username)

    for friend in friends_as_receiver:
        allfriends.append(friend.req_sender.username)

    return allfriends


def getPendingRequests(user_id):

    pendingrequests = FriendStatus.objects.filter(req_receiver=user_id, status="PENDING")

    allpending = []
    for request in pendingrequests:
        allpending.append(request.req_sender.username)

    return allpending


def getPendingSentRequests(user_id):

    sentpending = FriendStatus.objects.filter(req_sender=user_id, status="PENDING")

    allsentpending = []
    for sentreq in sentpending:
        allsentpending.append(sentreq.req_receiver.username)

    return allsentpending


def userEncodingFunction(user_id):

    userset = Users.objects.filter(username=user_id)
    encodeduser = []
    for user in userset:
        encodeduser.append(user.username)

    return encodeduser


def getRemainingUsers(user_id):
    allusers = getAllUsers()
    allfriends = getAllFriends(user_id)
    allrequests = getPendingRequests(user_id)
    allsentrequests = getPendingSentRequests(user_id)
    user = userEncodingFunction(user_id)

    temporary = set(allusers) - set(allfriends)
    temporary = set(temporary) - set(allrequests)
    temporary = set(temporary) - set(allsentrequests)
    temporary = set(temporary) - set(user)

    remainingusers = list(temporary)

    return remainingusers


def writeToPickle(path, filename, data):
    with open(path+filename+'.pkl', 'wb') as writefile:
        pickle.dump(data, writefile, pickle.HIGHEST_PROTOCOL)


def readFromPickle(path, filename):
    with open(path+filename+'.pkl', 'rb') as readfile:
        return pickle.load(readfile)


def getUserObject(user_id):

    userset = Users.objects.filter(username=user_id)

    for user in userset:
        userneeded = user

    return userneeded

# --> USEFUL FUNCTIONS END <--

# --> VIEWS START <--

# USER REGISTRATION, AUTHENTICATION AND SESSION MANAGEMENT
# SIGNUP
def signup(request):

    if request.session.has_key('username'):
        return HttpResponseRedirect('/home')

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = Users(username=username, password=password)
        user.save()

        request.session['username'] = username

        interest1 = form.cleaned_data.get('interest1')
        interval1 = form.cleaned_data.get('interval1')
        interest2 = form.cleaned_data.get('interest2')
        interval2 = form.cleaned_data.get('interval2')
        interest3 = form.cleaned_data.get('interest3')
        interval3 = form.cleaned_data.get('interval3')

        with open(USER_DIR+username+'.csv', 'wb') as userfile:
            userwriter = csv.writer(userfile, delimiter=',')
            userwriter.writerow([interest1, interval1])
            userwriter.writerow([interest2, interval2])
            userwriter.writerow([interest3, interval3])

        return HttpResponseRedirect('/home')

    context = {
        "form": form,
    }

    return render(request, "signup.html", context)

# LOGIN
def login(request):

    if request.session.has_key('username'):
        return HttpResponseRedirect('/home')

    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        request.session['username'] = username

        return HttpResponseRedirect('/home')

    context = {
        "form": form,
    }

    return render(request, "index.html", context)

# LOGOUT
def logout(request):

    try:
        del request.session['username']
    except:
        pass
    return HttpResponseRedirect('/')


# HOME
def home(request):

    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    form = QueryForm(request.POST or None)

    context = {
        'username': username,
        'form': form,
    }

    if form.is_valid():
        query_text = form.cleaned_data.get('query')

        filename = username+'$'+str(int(time.time()))

        writeToPickle(QUERY_DIR, filename, query_text)

        queryobj = Queries(q_filename=filename, asked_by=getUserObject(username))
        queryobj.save()

        HttpResponseRedirect('/query/'+str(queryobj.q_id))

    return render(request, "home.html", context)


# FRIEND REQUESTS
def friendrequests(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    allfriendrequests = getPendingRequests(username)

    allremainingusers = getRemainingUsers(username)

    context = {
        'username': username,
        'friend_requests': allfriendrequests,
        'remaining_users': allremainingusers,

    }
    return render(request, "friendrequests.html", context)


# RECEIVED QUERIES
def receivedqueries(request):

    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    received_set = QueriesReceived.objects.filter(asked_to=username)

    queryset = []

    for rs in received_set:

        query = []
        qstring = readFromPickle(QUERY_DIR, rs.question_asked.q_filename)
        qstring = qstring[:30] + '...'

        query.append(rs.question_asked.q_id)
        query.append(rs.question_asked.asked_by.username)
        query.append(qstring)

        queryset.append(query)

    context = {
        'username': username,
        'queryset': queryset,
        'key': 'received',
    }

    return render(request, "questionsbase.html", context)


# ASKED QUERIES
def askedqueries(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    asked_set = Queries.objects.filter(asked_by=username)

    query_set = []

    for asked in asked_set:
        query = []
        qstring = readFromPickle(QUERY_DIR, asked.q_filename)
        qstring = qstring[:30] + '...'

        query.append(asked.q_id)
        query.append(qstring)

        query_set.append(query)

    context = {
        'username': username,
        'query_set': query_set,
        'key': 'asked',
    }

    return render(request, "questionsbase.html", context)


# ADD TOPICS OF INTEREST
def addtopics(request):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    form = TopicForm(request.POST or None)

    context = {
        'username': username,
        'form': form,
    }

    if form.is_valid():
        newinterest = form.cleaned_data.get('topic')
        newval = form.cleaned_data.get('expval')

        with open(USER_DIR+username+'.csv', 'a') as csvfile:
            csvw = csv.writer(csvfile, delimiter=',')
            csvw.writerow([newinterest, newval])

        return HttpResponseRedirect('/')

    return render(request, "addtopic.html", context)


# ACCEPT FRIEND
def acceptfriend(request, sender):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    form = IntimacyForm(request.POST or None)

    context = {
        'username': username,
        'form': form,
        'sender': sender,
        'buttontext': 'Accept Request',
    }

    if form.is_valid():
        intimacy = form.cleaned_data.get('intimacy')

        friend_group = FriendStatus.objects.filter(req_receiver=username, req_sender=sender)

        for fg in friend_group:
            friendship = fg

        friendship.status = 'ACCEPTED'
        friendship.save()

        friendval = FriendValue(friendship_no=friendship, value_by_user=getUserObject(username), value=intimacy)
        friendval.save()

        return HttpResponseRedirect('/friendrequests')

    return render(request, "basefriend.html", context)


# ADD FRIEND
def addfriend(request, receiver):
    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    form = IntimacyForm(request.POST or None)

    context = {
        'username': username,
        'form': form,
        'receiver': receiver,
        'buttontext': 'Send Request',
    }

    if form.is_valid():
        intimacy = form.cleaned_data.get('intimacy')

        friendship = FriendStatus(req_receiver=getUserObject(receiver), req_sender=getUserObject(username),status="PENDING")
        friendship.save()

        friendvalue = FriendValue(friendship_no=friendship, value_by_user=getUserObject(username), value=intimacy )
        friendvalue.save()

        return HttpResponseRedirect('/friendrequests')

    return render(request, "basefriend.html", context)


# DISPLAY QUERY
def queries(request, id):

    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    form = AnswerForm(request.POST or None)

    QueryObjects = Queries.objects.filter(q_id=id)

    for ob in QueryObjects:
        query = ob

    q_text = readFromPickle(QUERY_DIR, query.q_filename)

    AnswerObjects = Answers.objects.filter(query=query)

    answer_set = []

    for ao in AnswerObjects:

        answer = []

        a_text = readFromPickle(ANS_DIR, ao.a_filename)

        answer.append(ao.a_id)
        answer.append(ao.answered_by.username)
        answer.append(a_text)

        answer_set.append(answer)

    context = {
        'username': username,
        'query': q_text,
        'form': form,
        'answer_set': answer_set,
        'asked_by': query.asked_by.username,
    }

    if form.is_valid():
        answer_text = form.cleaned_data.get('answer')

        filename = username + '$' + str(int(time.time()))

        writeToPickle(ANS_DIR, filename, answer_text)

        answerobj = Answers(a_filename=filename, answered_by=getUserObject(username), query=query)
        answerobj.save()

        HttpResponseRedirect('/query/' + str(query.q_id))

    return render(request, "query.html", context)


def answers(request, id):

    if not request.session.has_key('username'):
        return HttpResponseRedirect('/')

    username = request.session['username']

    form = RatingForm(request.POST or None)

    AnswerObjects = Answers.objects.filter(a_id=id)

    for ao in AnswerObjects:
        answer = ao

    a_text = readFromPickle(ANS_DIR, answer.a_filename)
    q_text = readFromPickle(QUERY_DIR, answer.query.q_filename)

    context = {
        'username': username,
        'query': q_text,
        'answer': a_text,
        'form': form,
        'answered_by': answer.answered_by.username,
        'asked_by': answer.query.asked_by.username,
    }

    if form.is_valid():
        rating = form.cleaned_data.get('rating')

        # Scooby will fuck around with this code

        HttpResponseRedirect('/answer/' + str(answer.q_id))

    return render(request, "answer.html", context)

# --> VIEWS END <--
