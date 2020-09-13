from django.contrib import admin
from .models import Tenant,User,Owner
# Register your models here.
admin.site.register(User)
admin.site.register(Tenant)
admin.site.register(Owner)