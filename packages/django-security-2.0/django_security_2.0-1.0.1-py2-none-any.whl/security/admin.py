from django.contrib import admin

from security.models import PasswordExpiry, CspReport

@admin.register(PasswordExpiry)
class adminExpiry(admin.ModelAdmin):
    list_display = ('user_id','password_expiry_date',)
admin.site.register(CspReport)
