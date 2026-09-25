from django.db import models
from django.conf import settings
from properties.models import Property, RentalRequest


# Create your models here.
class Review(models.Model):
    tenant = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name='reviews'
   )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'property'],
                name='unique_tenant_property_review'
            )
        ]

    def __str__(self):
        return f"{self.tenant.username} - {self.property.title} ({self.rating}/5)"