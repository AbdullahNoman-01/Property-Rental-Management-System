from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .models import CampaignRequest
from properties.models import Notification

User = get_user_model()


class CampaignRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tenant_user',
            email='tenant@example.com',
            password='testpassword123',
            role=User.Role.TENANT,
            phone='01711111111'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin_boss',
            email='admin@example.com',
            password='adminpassword123',
            role=User.Role.OWNER
        )

    def test_unauthenticated_user_cannot_submit_campaign(self):
        """Unauthenticated visitor cannot submit a campaign request."""
        post_data = {
            'full_name': 'Anonymous Visitor',
            'phone_number': '01999999999',
            'property_location': 'Gulshan 2, Dhaka',
            'campaign_package': 'pro',
            'property_note': 'Test note',
        }
        response = self.client.post(reverse('advertise:advertise'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
        self.assertEqual(CampaignRequest.objects.count(), 0)

    def test_authenticated_user_can_submit_campaign(self):
        """Authenticated user submits campaign request which links to their account."""
        self.client.login(username='tenant_user', password='testpassword123')
        post_data = {
            'full_name': 'Tenant Full Name',
            'phone_number': '01711111111',
            'property_location': 'Banani DOHS, Dhaka',
            'campaign_package': 'pro',
            'property_note': 'Luxury 4 bed apartment boost',
        }
        response = self.client.post(reverse('advertise:advertise'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('advertise:advertise'))

        campaign = CampaignRequest.objects.first()
        self.assertIsNotNone(campaign)
        self.assertEqual(campaign.user, self.user)
        self.assertEqual(campaign.property_location, 'Banani DOHS, Dhaka')
        self.assertFalse(campaign.is_contacted)

    def test_admin_contacting_creates_notification_for_user(self):
        """When admin marks is_contacted=True, user receives real-time notification."""
        campaign = CampaignRequest.objects.create(
            user=self.user,
            full_name='Tenant Full Name',
            phone_number='01711111111',
            property_location='Dhanmondi 27, Dhaka',
            campaign_package='ultra',
            property_note='Please boost ASAP'
        )

        # Before contact: 0 notifications
        self.assertEqual(Notification.objects.filter(recipient=self.user).count(), 0)

        # Admin contacts user
        campaign._admin_sender = self.admin_user
        campaign.is_contacted = True
        campaign.admin_note = 'Called and verified. Boost starts tomorrow.'
        campaign.save()

        # Notification should now be created
        notif = Notification.objects.filter(recipient=self.user).first()
        self.assertIsNotNone(notif)
        self.assertEqual(notif.notification_type, 'CAMPAIGN_CONTACTED')
        self.assertFalse(notif.is_read)
        self.assertIn('Dhanmondi 27, Dhaka', notif.message)
        self.assertIn('Called and verified', notif.message)

    def test_notification_redirect_for_campaign_contact(self):
        """Clicking campaign contact notification marks it read and redirects to advertise page."""
        campaign = CampaignRequest.objects.create(
            user=self.user,
            full_name='Tenant Full Name',
            phone_number='01711111111',
            property_location='Uttara Sector 3, Dhaka',
            campaign_package='starter',
            is_contacted=True
        )
        notif = Notification.objects.filter(recipient=self.user).first()
        self.assertIsNotNone(notif)

        self.client.login(username='tenant_user', password='testpassword123')
        redirect_url = reverse('notification_redirect', args=[notif.id])
        response = self.client.get(redirect_url)

        # Should redirect to advertise page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('advertise:advertise'))

        # Notification should be marked as read
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
