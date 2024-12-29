from django.urls import path
#from django.conf.urls import handler404  # Import handler404
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile_page"),
    # path("send-money", views.send_money, name="send_money"),
    path('send-money', views.send_money, name='send_money'),
]

# Add a reference to the custom 404 view
#handler404 = "bank.views.custom_404_view"