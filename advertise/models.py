from django.conf import settings
from django.db import models
from django.utils import timezone


class CampaignRequest(models.Model):
    PACKAGE_STARTER = 'starter'
    PACKAGE_PRO = 'pro'
    PACKAGE_ULTRA = 'ultra'

    PACKAGE_CHOICES = [
        (PACKAGE_STARTER, 'Starter Boost (3 Days - 5,000+ Reach)'),
        (PACKAGE_PRO, 'Pro Growth (7 Days - 20,000+ Reach - Recommended)'),
        (PACKAGE_ULTRA, 'Ultra Reach (15 Days - 50,000+ Reach + Social Ads)'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='campaign_requests',
        null=True,
        blank=True,
        help_text="User who requested the advertising campaign"
    )
    full_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=30)
    property_location = models.CharField(max_length=200)
    campaign_package = models.CharField(
        max_length=20,
        choices=PACKAGE_CHOICES,
        default=PACKAGE_PRO,
    )
    property_note = models.TextField(blank=True)
    is_contacted = models.BooleanField(default=False)
    contacted_at = models.DateTimeField(null=True, blank=True)
    admin_note = models.TextField(
        blank=True,
        help_text="Optional message/note sent to the user upon contacting."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Campaign Request'
        verbose_name_plural = 'Campaign Requests'

    def __str__(self):
        return f'{self.full_name} — {self.property_location}'

    def save(self, *args, **kwargs):
        is_newly_contacted = False
        if self.pk:
            prev = CampaignRequest.objects.filter(pk=self.pk).values('is_contacted').first()
            if prev and not prev['is_contacted'] and self.is_contacted:
                is_newly_contacted = True
        elif self.is_contacted:
            is_newly_contacted = True

        if is_newly_contacted and not self.contacted_at:
            self.contacted_at = timezone.now()

        super().save(*args, **kwargs)

        if is_newly_contacted and self.user:
            from properties.models import Notification
            from django.contrib.auth import get_user_model
            User = get_user_model()
            sender = getattr(self, '_admin_sender', None)
            if not sender:
                sender = User.objects.filter(is_superuser=True).first() or self.user

            msg = f"RentNest Team has contacted you regarding your campaign request for {self.property_location} ({self.get_campaign_package_display()})."
            if self.admin_note:
                msg += f" Note: {self.admin_note}"

            Notification.objects.create(
                recipient=self.user,
                sender=sender,
                notification_type='CAMPAIGN_CONTACTED',
                message=msg[:250]
            )

