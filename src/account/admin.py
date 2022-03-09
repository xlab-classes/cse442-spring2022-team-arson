from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin

# this is only shown in the django admin section
class AccountAdmin(UserAdmin):
	list_display = ('username', 'date_joined', 'last_login', 'is_admin', 'is_staff',)
	search_fields = ('username',)
	readonly_fields = ('date_joined', 'last_login',)

	filter_horizontal = ()
	list_filter=()
	fieldsets=()

admin.site.register(Account, AccountAdmin)
