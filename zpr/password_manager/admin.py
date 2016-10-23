from django.contrib import admin
from .models import PasswordEntry

# Register your models here.


class PasswordEntryModelAdmin(admin.ModelAdmin):
    list_display = ["site", "password", "user"]
    list_display_links = ["site"]
    search_fields = ["site"]
    list_editable = ["password"]

    class Meta:
        model = PasswordEntry


admin.site.register(PasswordEntry, PasswordEntryModelAdmin)
