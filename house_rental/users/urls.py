from django.urls import include, path
import users.views as users_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', users_views.home, name='home'),
    path('owner/home', users_views.owner_home, name='owner_home'),
    path('tenant/home', users_views.tenant_home, name='tenant_home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/tenant/', users_views.tenant_register, name='tenant_signup'),
    path('signup/owner/', users_views.owner_register, name='owner_signup'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
]