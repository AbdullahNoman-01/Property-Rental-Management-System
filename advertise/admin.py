from django.contrib import admin
from django.utils import timezone

from .models import CampaignRequest


@admin.register(CampaignRequest)
class CampaignRequestAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'user',
        'phone_number',
        'property_location',
        'campaign_package',
        'is_contacted',
        'contacted_at',
        'created_at',
    )
    list_filter = (
        'is_contacted',
        'campaign_package',
        'created_at',
        'contacted_at',
    )
    search_fields = (
        'full_name',
        'user__username',
        'user__email',
        'phone_number',
        'property_location',
        'property_note',
        'admin_note',
    )
    list_editable = ('is_contacted',)
    readonly_fields = ('created_at', 'contacted_at')
    ordering = ('-created_at',)
    actions = ['mark_contacted_and_notify']

    fieldsets = (
        (
            'User & Contact Details',
            {
                'fields': (
                    'user',
                    'full_name',
                    'phone_number',
                    'property_location',
                )
            },
        ),
        (
            'Campaign Details',
            {
                'fields': (
                    'campaign_package',
                    'property_note',
                )
            },
        ),
        (
            'Follow-up & Notification',
            {
                'fields': (
                    'is_contacted',
                    'contacted_at',
                    'admin_note',
                    'created_at',
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj._admin_sender = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description="Mark selected as Contacted & Send Notification to User")
    def mark_contacted_and_notify(self, request, queryset):
        count = 0
        for req in queryset:
            if not req.is_contacted:
                req._admin_sender = request.user
                req.is_contacted = True
                req.contacted_at = timezone.now()
                req.save()
                count += 1
        self.message_user(
            request,
            f"Successfully marked {count} request(s) as contacted and sent notifications to the users."
        )
