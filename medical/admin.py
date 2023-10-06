from django.contrib import admin
from django.contrib.auth import admin as admin_auth_django

from medical.models import  *

from .forms import UserChangeForm, UserCreationForm
from .models import Users, UserProcedure

admin.site.register(Procedure)
admin.site.register(Recommendation)
admin.site.register(UserProcedure)
admin.site.register(ProcedureReco)

class ProcedureInline(admin.TabularInline):
    model = Users.procedure.through
    extra = 1

@admin.register(Users)
class UsersAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    fieldsets = admin_auth_django.UserAdmin.fieldsets + (
        ('Extras', {'fields': ('cpf', 'birth_date', 'street', 'number', 'district', 'uf', 'phone','association','bariatric')}),
    )
    inlines = [ProcedureInline]
