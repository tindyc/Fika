from django.contrib import admin
from event.models import EventPost
# Register your models here.

class EventPostAdmin(admin.ModelAdmin):
    list_filter = ["author"]
    list_display = ["author"]
    search_fields = ["author"]

    class Meta:
        model = EventPost

admin.site.register(EventPost, EventPostAdmin)