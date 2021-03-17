from django.shortcuts import render, redirect
from .models import User, UserManager, Item, ItemManager, Message, MessageManager
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.user_validator(request.POST)
    if request.method != "POST":
        return redirect('/')
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
        return redirect("/account") # never render on a post, always redirect!    

def signin(request):
    return render(request, "login.html")

def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'items': Item.objects.all(),
                'saved_item': User.objects.get(id=request.session['user_id']).saved_item.all()
            }
            return render(request, 'dashboard.html', context)
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['user_name']=f"{user.first_name}"
        
        return redirect('/account')
    return redirect("/")

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
                'messages': Message.objects.all(),
                
            }
            return render(request, 'account.html', context)
    return redirect('/')

def messages(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'items': Item.objects.all(),
                'messages': Message.objects.all(),
                
            }
            return render(request, 'messages.html', context)
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
            image=request.FILES['image'], 
            seller=user
        )
        request.session['item_id'] = item.id
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
        if 'new_image' not in request.FILES:
            my_item.image = my_item.image
        else:
            my_item.image = request.FILES['new_image']
        my_item.save()
    return redirect(f'/account')

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('/account')

def item_info(request, item_id):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'item': Item.objects.get(id=item_id),
        
    }
    return render(request, "item.html", context)

def add_cart(request, item_id):
    user = User.objects.get(id=request.session["user_id"])
    item = Item.objects.get(id=item_id)
    user.saved_item.add(item)
    return redirect('/cart')

def cart(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])

        if user:
            context = {
                'user': user[0],
                'items': Item.objects.all(),
            }
            return render(request, 'cart.html', context)
    return redirect('/')

def remove(request, item_id):
    user = User.objects.get(id=request.session["user_id"])
    item = Item.objects.get(id=item_id)
    user.saved_item.remove(item)

    return redirect('/cart')

def send_message(request, item_id):
    if request.method == "POST":
        if 'user_id' in request.session:
            user = User.objects.get(id=request.session['user_id'])
            item = Item.objects.get(id=item_id)
            receiver = User.objects.get(id=request.POST['seller_id'])
            Message.objects.create(
                message=request.POST['message'],
                subject=request.POST['subject'],
                sender=user,
                receiver=receiver
            )
    return redirect(f'/messages')
    # sender = User.objects.get(id=request.session['user_id'])
    # seller = User.objects.get(id=request.POST['receiver'])
    # new_message = Message.objects.create(
    #     subject = request.POST['subject'],
    #     message = request.POST['message'],
    #     sender = user_id,
    #     seller = recipient
    # )
    # user_id=request.session['user_id']
    # return redirect(f'/messages')

def delete_received_message(request, message_id):
    trash = Message.objects.get(id=message_id)
    user = User.objects.get(id=request.session['user_id'])
    if trash.recipient == user:
        trash.delete()
    user_id=request.session['user_id']
    return redirect(f'/messages')

def delete_sent_message(request, message_id):
    trash = Message.objects.get(id=message_id)
    user = User.objects.get(id=request.session['user_id'])
    if trash.sender == user:
        trash.delete()
    user_id=request.session['user_id']
    return redirect(f'/messages')

def messages(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'messages': Message.objects.all(),
        'all_users': User.objects.all(),
    }
    return render(request, 'messages.html', context)

def view_message(request, message_id):
    user = User.objects.get(id=request.session['user_id'])
    message = Message.objects.get(id=message_id)
    context = {
        'user': user,
        'message': message,
    }
    return render(request, 'view_message.html', context)

def purchase(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('/complete')

def complete(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])

        if user:
            context = {
                'user': user[0],
                

            }
            return render(request, 'complete.html', context)
    return redirect('/')
    
    



# def purchase()
