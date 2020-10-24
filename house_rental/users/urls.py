from django.urls import include, path
import users.views as users_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', users_views.home, name='home'),
    path('owner/home', users_views.owner_home, name='owner_home'),
    path('tenant/home', users_views.tenant_home, name='tenant_home'),
    path('tenant/update/', users_views.tenantupdate, name = 'tenantupdate'),
    path('tenant/profile/', users_views.tenant_profile, name = 'tenantprofile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/tenant/', users_views.tenant_register, name='tenant_signup'),
    path('signup/owner/', users_views.owner_register, name='owner_signup'),
    path('new_property/',users_views.new_property, name = 'new_property'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('owner/delete_property/<int:delete_id>',users_views.delete_property, name = 'delete_property'),
    path('owner/update_property/<int:update_id>',users_views.update_property, name = 'update_property'),
    path('tenant/bookmark/<int:bookmark_id>', users_views.bookmark, name = 'bookmark'),
    path('tenant/remove_bookmark/<int:bookmark_id>', users_views.remove_bookmark, name = 'remove_bookmark'),
    path('tenant/notify_owner/<int:notify_property_id>', users_views.notify_owner, name = 'notify_owner')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   