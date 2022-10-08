from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,passwordchange,setpasswordconfirm
from app import views
from app.forms import LoginForm
from .forms import PasswordReset


urlpatterns = [
    path('', views.home.as_view(),name='home'),
    # path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>', views.ProductDetails.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    
    

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileViews.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    

    path('changepassword/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=passwordchange,success_url='/changepassworddone/'), name='changepassword'),
    path('changepassworddone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/changepassworddone.html'), name='changepassworddone'),
    # path('changepass/',views.changepass,name='changepassword'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=PasswordReset),name='passwordreset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=setpasswordconfirm),name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('headphones/', views.headphones, name='headphones'),
    path('headphones/<slug:data>', views.headphones, name='headphonesdata'),
    path('camera/', views.camera, name='camera'),
    path('camera/<slug:data>', views.camera, name='cameradata'),

    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login') ,name='logout'),

    path('registration/', views.customerregistration.as_view(), name='customerregistration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
