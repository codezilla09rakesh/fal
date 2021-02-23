from rest_framework import serializers
from .models import Plans, Transactions, Subscriptions, Bookmarks, Offers


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = "__all__"


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = "__all__"


class UpdateSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ['plan', 'transaction', 'status', 'valid_till']


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"
