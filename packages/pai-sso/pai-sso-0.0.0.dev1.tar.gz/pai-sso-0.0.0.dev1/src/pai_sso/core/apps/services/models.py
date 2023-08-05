import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from ...common import ROLE_CHOICES

logger = logging.getLogger('services')


class Service(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=32, unique=True, null=True)
    url = models.CharField(max_length=255, unique=True)
    picture = models.TextField(_('picture'), null=True, blank=True)

    cookie_domain = models.CharField(max_length=255, null=True, blank=True)  # unused but useful
    redirect_wait = models.PositiveIntegerField(default=2000)

    subscription_required = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    role = models.SmallIntegerField(
        choices=ROLE_CHOICES, null=True, blank=True)

    def get_tos(self, language):
        logger.debug('Service {0}, gettings tos for language {1}'.format(self, language))
        return self.terms_of_service.filter(language=language).first()

    def __str__(self):
        return self.url


class TOS(models.Model):
    language = models.CharField(max_length=3)
    text = models.TextField()

    service = models.ForeignKey(Service, related_name="terms_of_service", on_delete=models.CASCADE)


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_unsubscribed(self):
        return self.unsubscribed_at is not None

    def __str__(self):
        return self.user.username + '@' + self.service.url


# Signals

@receiver(post_save, sender=Subscription)
def update_user_subscription_state(sender, instance, **kwargs):
    # should delete user jwt only on unsubscribe
    if instance.unsubscribed_at is not None:
        logger.info('User {0} updated subscription unsubscribed_at to service {1} to: {2}'.format(instance.user,
                                                                                                  instance.service,
                                                                                                  instance.unsubscribed_at))
        instance.user.remove_all_user_devices()
