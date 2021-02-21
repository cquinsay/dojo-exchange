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
            return redirect("/dashboard") # never render on a post, always redirect!    
    return redirect('/')

def signin(request):
    return render(request, "login.html")

def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'items': Item.objects.all(),

            }
            return render(request, 'dashboard.html', context)
    return redirect('/')

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
        
        return redirect('/dashboard')
    return redirect("/signin")

def logout(request):
    request.session.clear()

    return redirect('/')

def account(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'items': Item.objects.all(),

            }
            return render(request, 'account.html', context)
    return redirect('/')
    

def add_item(request):
    errors = Item.objects.item_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/account')
    else:
        user = User.objects.get(id=request.session['user_id'])
        request.session['user_id'] = user.id
        request.session['user_name']=f"{user.first_name}"
        item = Item.objects.create(
            item_name=request.POST['item_name'],
            price=request.POST['price'],
            condition=request.POST['condition'],
            category=request.POST['category'],
            description=request.POST['description'],
            seller=user
        )
        
        return redirect('/account')
    return redirect("/")

def edit_item(request, item_id):
    context = {
        'edit_item': Item.objects.get(id=item_id)
    }

    return render(request,'edit_item.html', context)

def update_item(request, item_id):
    if request.method=='POST':
        errors = Item.objects.update_item_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/items/{item_id}/edit')
        my_item=Item.objects.get(id=item_id)
        my_item.item_name=request.POST['new_item_name']
        my_item.price=request.POST['new_price']
        my_item.condition=request.POST['new_condition']
        my_item.category=request.POST['new_category']
        my_item.description=request.POST['new_description']
        my_item.save()

    return redirect(f'/account')

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('/account')

def item_info(request, item_id):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'item': Item.objects.get(id=item_id)
    }
    return render(request, "item.html", context)

def add_cart(request, item_id):
    user = User.objects.get(id=request.session["user_id"])
    item = Item.objects.get(id=item_id)
    user.buyer.add(item)

    return redirect('/cart')

def cart(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'items': Item.objects.all(),

            }
            return render(request, 'dashboard.html', context)
    return redirect('/')
