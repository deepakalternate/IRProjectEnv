# --> IMPORTS BEGIN <--

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Users
from .forms import SignUpForm, LoginForm


import os
import pickle

# --> IMPORTS END <--

# --> FILE PATHS  START<--

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP_DIR = os.path.join(BASE_DIR, "dump")
QUERY_DIR = os.path.join(DUMP_DIR, "queries")
ANS_DIR = os.path.join(DUMP_DIR, "answers")

# --> FILE PATHS END <--

# --> USEFUL FUNCTIONS START <--

# --> USEFUL FUNCTIONS END <--

# --> VIEWS START <--


def signup(request):

    context = {

    }

    return render(request, "signup.html", context)


def login(request):

    print BASE_DIR
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

# --> VIEWS END <--
