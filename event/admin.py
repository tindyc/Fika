from django.contrib import admin
from event.models import EventPost
# Register your models here.

class EventPostAdmin(admin.ModelAdmin):
    list_filter = ["user"]
    list_display = ["user"]
    search_fields = ["user"]

    class Meta:
        model = EventPost

admin.site.register(EventPost, EventPostAdmin)