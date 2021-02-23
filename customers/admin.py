from django.contrib import admin
from customers.models import Plans, PlansHistory, Offers, PlanOffers, Transactions, Subscriptions
# Register your models here.

admin.site.register(Plans)
admin.site.register(PlanOffers)
admin.site.register(PlansHistory)
admin.site.register(Offers)
admin.site.register(Transactions)
admin.site.register(Subscriptions)
