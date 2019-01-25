from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

import stripe
stripe.api_key = 'pk_test_eCgtJBzEKcnlp2gw1xOr86u0'

# Create your models here.
MEMBERSHIP_CHOICES = (
    ('Enterprise', 'ent'),
    ('Professional', 'pro'),
    ('Free', 'free')
)

class Membership(models.Model):
    slug  = models.SlugField()
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, max_length=30, default='free')
    price = models.IntegerField(default=9.99)
    strip_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type
       


class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    strip_customer_id = models.CharField(max_length=40)
    membeership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
    if created:
        UserMembership.objects.get(user=instance)
    user_membership, created = UserMembership.objects.get(user=instance)

    if user_membership.stripe_customer_id is None or user_membership.strip_customer_id is '':
        new_customer_id = strip.Customer.create(email=instance.email)
        user_membership.strip_customer_id = new_customer_id['id']
        user_membership.save()

post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)        

class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    strip_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username
