from django.contrib import admin

from .models import URLRewrite


@admin.register(URLRewrite)
class URLRewriteAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("from_value", "to_value")
    ordering = ["from_value"]
