from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken
from cities_light.models import City, SubRegion




class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name', 'last_name')
    exclude = ('groups', 'last_login', 'user_permissions', 'password', )
    empty_value_display = 'unknown'
    list_filter = ('is_active', 'is_superuser', 'created_at')
    search_fields = ['username', 'first_name', 'last_name']


admin.site.register(User, UserAdmin)

admin.site.site_header = 'THANKS FINANCE'
admin.site.site_title = 'THANKS FINANCE'
admin.site.index_title = "THANKS FINANCE"

admin.site.unregister(Group)


admin.autodiscover()
admin.site.unregister(AccessToken)
admin.site.unregister(Application)
admin.site.unregister(RefreshToken)
admin.site.unregister(Grant)

# admin.site.unregister(City)
# admin.site.unregister(SubRegion)
# admin.site.empty_value_display = 'None'


