from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def signup(request):
    return render(request, 'signup.html')

def register(request):
    errors = User.objects.user_validator(request.POST)
    if request.method == "POST":
        if User.objects.filter(email = request.POST['email']):
            messages.error(request, 'That email already exists!')
            return redirect('/')
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 

            new_user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'], 
                email=request.POST['email'], 
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['user_name']=f"{new_user.first_name}"
            return redirect("/main") # never render on a post, always redirect!    
    return redirect('/')

def signin(request):
    return render(request, "login.html")

def main(request):
    return render(request, "main.html")

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signin')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['user_name']=f"{user.first_name}"
        
        return redirect('/main')
    return redirect("/signin")

def logout(request):
    request.session.clear()

    return redirect('/')

def account(request):
    return render(request, 'account.html')


