from django.urls import path
from.import views

urlpatterns = [
    path('',views.home,name='index'),
    path('category',views.category,name='category'),
    path('single/<int:id>/',views.single,name='single'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register',views.register_view,name='register'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_and_delete,name='logout'),
     path('store/',views.store,name='store')
 

]