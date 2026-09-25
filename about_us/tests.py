from django.test import TestCase, Client
from django.urls import reverse


class AboutUsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_us_page_loads_successfully(self):
        """Test that the About Us page returns HTTP 200 and uses correct template."""
        response = self.client.get(reverse('about_us:about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us/about_us.html')
        self.assertContains(response, 'About RentNest')
        self.assertContains(response, 'Why RentNest?')
        self.assertContains(response, 'About your Search')
        self.assertContains(response, 'Latest Property Listing in Bangladesh')

