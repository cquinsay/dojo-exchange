from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('signin', views.signin),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('account', views.account),
    path('add_item', views.add_item),
    path('items/<int:item_id>/edit_item', views.edit_item),
    path('items/<int:item_id>/update_item', views.update_item),
    path('items/<int:item_id>/delete_item', views.delete_item),
    path('items/<int:item_id>', views.item_info),
    path('items/<int:item_id>/add_cart', views.add_cart),
    path('items/<int:item_id>/remove', views.remove),
    path('cart', views.cart),
    path('items/<int:item_id>/remove', views.remove),
    path('messages', views.messages),
    path('message/<int:item_id>', views.create_message),
    path('delete_message/<int:message_id>', views.delete_message),
    path('purchase/<int:item_id>', views.purchase),
    path('complete', views.complete),
    

]