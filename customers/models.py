from django.db import models
from users.models import BaseModel, User
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Plans(BaseModel):
    name = models.CharField(max_length=225, null=True, blank=True, verbose_name="Plan Name")
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Plan Price")
    description = models.TextField(null=True, blank=True, verbose_name=_("Plan Description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Plans'


class Offers(BaseModel):
    name = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Offer Title"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Plan Description"))
    valid = models.DateField(null=True, blank=True, verbose_name=_("Validity"), help_text="Validity In Month")

    class Meta:
        verbose_name_plural = "Offers"

    def __str__(self):
        return self.name


class PlanOffers(BaseModel):
    offer = models.ForeignKey(Offers, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Offer"))
    plan = models.ForeignKey(Plans, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Plan"))

    def __str__(self):
        return str(self.offer.name)

    class Meta:
        verbose_name_plural = "PlanOffers"


class Transactions(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=225, null=True, blank=True)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = "Transactions"


class Subscriptions(BaseModel):
    SUBSCRIPTION_STATUS = (
        ('Subscribed', _('Subscribed')),
        ('Unsubscribed', _('Unsubscribed')),
        ('Canceled', _('Canceled')),
        ('Rejected', _('Rejected')),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trial_period_start = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Trial Period Start"))
    trial_period_end = models.DateTimeField(blank=True, null=True, verbose_name=_("Trial Period End"))
    subscribeAfter = models.BooleanField(blank=True, null=True)
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    date_subscribed = models.DateTimeField(blank=True, null=True)
    date_unsubscribed = models.DateTimeField(blank=True, null=True)
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE, null=True, blank=True)
    subscription_status = models.CharField(max_length=100, choices=SUBSCRIPTION_STATUS, default="Current")
    valid_till = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return self.user.fullname() + "'s: " + self.plan.name + " Plan"


class Bookmarks(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    stock_id = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Stock Id"))
    category_id = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Category Id"))

    def __str__(self):
        return self.user.fullname()

    class Meta:
        verbose_name_plural = "Bookmarks"


class PlansHistory(BaseModel):
    subscription = models.ForeignKey(Subscriptions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_start = models.DateTimeField(blank=True, null=True)
    plan_end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.fullname() + "'s Plans History"

    class Meta:
        verbose_name_plural = "Plans History"
