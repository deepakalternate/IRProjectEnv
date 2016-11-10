# --> IMPORTS BEGIN <--

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Users, FriendStatus
from .forms import SignUpForm, LoginForm


import os
import pickle
import csv

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

# --> USEFUL FUNCTIONS END <--

# --> VIEWS START <--

# USER REGISTRATION, AUTHENTICATION AND SESSION MANAGEMENT
# SIGNUP
def signup(request):

    if request.session.has_key('username'):
        pass

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data('username')
        password = form.cleaned_data('password1')

        user = Users(username=username, password=password)
        user.save()

        request.session['username'] = username

        interest1 = form.cleaned_data('interest1')
        interval1 = form.cleaned_data('interval1')
        interest2 = form.cleaned_data('interest2')
        interval2 = form.cleaned_data('interval2')
        interest3 = form.cleaned_data('interest3')
        interval3 = form.cleaned_data('interval3')

        with open(USER_DIR+username+'.csv', 'wb') as userfile:
            userwriter = csv.writer(userfile, delimiter=',')
            userwriter.writerow([interest1, interval1])
            userwriter.writerow([interest2, interval2])
            userwriter.writerow([interest3, interval3])

        return HttpResponseRedirect('/')

    context = {
        "form": form,
    }

    return render(request, "signup.html", context)

# LOGIN
def login(request):

    if request.session.has_key('username'):
        pass

    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        request.session['username'] = username

        return HttpResponseRedirect('/')

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

# --> VIEWS END <--
