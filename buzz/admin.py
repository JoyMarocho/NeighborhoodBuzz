from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile,User,Neighborhood,Business,Post
from .forms import NewUserForm,ExistingUserChangeForm
#from django.contrib.auth import get_user_model

#User = get_user_model()

# Register your models here.
class UserAdmin(UserAdmin):
    add_form = NewUserForm
    form = ExistingUserChangeForm
    model = User
    list_display = ('email', 'is_staff','is_active',)
    list_filter = ('email','is_active',)
    fieldsets = ((None,{'fields':('email','password')}),('Permissions',{'fields':('is_staff','is_active')}),)
    add_fieldsets = ((None,{'classes':('wide',),'fields':('email','password1','password2','is_staff','is_active')}),)
    search_fields = ('email',)
    ordering = ('email',)



admin.site.register(User,UserAdmin)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Neighborhood)
admin.site.register(Business)
