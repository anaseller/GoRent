from django.contrib import admin
from .models import History

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'action_type', 'timestamp', 'ip_address')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('user__email', 'listing__title', 'search_query', 'ip_address')
    readonly_fields = ('user', 'listing', 'action_type', 'timestamp', 'ip_address', 'search_query')