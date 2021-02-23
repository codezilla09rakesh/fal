from rest_framework import serializers
from .models import Plans, Transactions, Subscriptions, Bookmarks, Offers, PlanOffers, PlansHistory


class PlanSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.CharField(required=True)
    # description = serializers.CharField(required=True)
    class Meta:
        model = Plans
        fields = "__all__"


class SubscriptionsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    class Meta:
        model = Subscriptions
        fields = "__all__"


class UpdateSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ['plan', 'transaction', 'status', 'valid_till']


class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    stock = serializers.CharField(required=True)
    category = serializers.CharField(required=True)
    class Meta:
        model = Bookmarks
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description =serializers.CharField(required=True)
    valid = serializers.CharField(required=True)
    class Meta:
        model = Offers
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    stripe_id = serializers.CharField(required=True)
    plan = serializers.CharField(required=True)
    transaction_id = serializers.CharField(required=True)
    class Meta:
        model = Transactions
        fields = "__all__"

class PlanHistorySerialzier(serializers.ModelSerializer):
    class Meta:
        model = PlansHistory
        fields = "__all__"