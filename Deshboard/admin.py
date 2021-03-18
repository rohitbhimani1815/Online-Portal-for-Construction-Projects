from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(CustomUser,UserAdmin)
admin.site.register(SuperUserProfile)
admin.site.register(GovermentUserProfile)
admin.site.register(OrganizationUserProfile)
admin.site.register(CreateForm)
admin.site.register(CreateProject)
admin.site.register(FormData)
admin.site.register(applyProject)
admin.site.register(trackProject)
admin.site.register(pastProject)