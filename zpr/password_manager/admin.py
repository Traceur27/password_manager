from django.contrib import admin
from .models import PasswordEntry

# Register your models here.


class PasswordEntryModelAdmin(admin.ModelAdmin):
    list_display = ["name", "username","password", "user"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_editable = ["password"]

    class Meta:
        model = PasswordEntry


admin.site.register(PasswordEntry, PasswordEntryModelAdmin)
