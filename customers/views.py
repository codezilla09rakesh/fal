from .models import (
    Plans,
    Transactions,
    PlansHistory,
    PlanOffers,
    Subscriptions,
    Bookmarks,
    Offers
)

from .serializers import (
    PlanSerializer,
    TransactionSerializer,
    SubscriptionsSerializer,
    UpdateSubscriptionsSerializer,
    BookmarkSerializer,
    OfferSerializer
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication


class PlansView(ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plans.objects.all()
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['admin']

    def create(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "Plan is created"}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id=None, *args, **kwargs):
        """
        :param request:
        :param id:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            plan = Plans.objects.get(id=id)
            serializer = PlanSerializer(plan, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"message": "plan has updated"}, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        plan_list = Plans.objects.all()
        serializer = PlanSerializer(plan_list, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        :param request:
        :param id:
        :param args:
        :param kwargs:
        :return:
        """
        if id:
            try:
                plan = Plans.objects.get(id=id)
                serializer = PlanSerializer(plan)
                data = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": "plan_id is none"})


class SubscriptionsView(ModelViewSet):
    serializer_class = SubscriptionsSerializer
    queryset = Subscriptions.objects.all()
    authentication_classes = [OAuth2Authentication]

    def list(self, request, *args, **kwargs):
        """
        return =>list of user_id, plan_id, transaction_id, status, valid_till
        """
        user = request.user
        subscriptions = Subscriptions.objects.filter(user=user.id)
        serializer = SubscriptionsSerializer(subscriptions, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        return => user_id, plan_id ,transaction_id, status, valid_till
        """
        user = request.user
        if id:
            try:
                subscription = Subscriptions.objects.get(id=id, user=user.id)
                serializer = SubscriptionsSerializer(subscription)
                data = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "Subscription is not found"})

    def update(self, request, id=None, *args, **kwargs):
        """
        params: request => plan, transaction, status, valid_till
        return : message => successfully updated
        """
        user = request.user
        if id:
            data = request.data
            try:
                subscription = Subscriptions.objects.get(id=id, user=user.id)
                serializer = UpdateSubscriptionsSerializer(subscription, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data={"message": "Successfully Updated "})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(data={"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "Subscription is not found"})


class TransactionsView(ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transactions.objects.all()
    authentication_classes = [OAuth2Authentication]

    def list(self, request, *args, **kwargs):
        """
        reutrn => user, stripe_id, plan, transaction_id
        """
        transactions = Transactions.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None, *args, **kwargs):
        """
        params: request => id
        returns => user, stripe_id, plan, transaction_id
        """
        user = request.user
        if id:
            try:
                transaction = Transactions.objects.get(id=id, user=user.id)
                serializer = TransactionSerializer(transaction, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class BookmarkView(ModelViewSet):
    serializer_class = BookmarkSerializer
    queryset = Bookmarks.objects.all()
    authentication_classes = [OAuth2Authentication]

    def create(self, request, *args, **kwargs):
        """
        params: request => user_id, stock_id, category
        return => successfully bookmark
        """
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "Successfully Bookmark"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        return => stock_id
        """
        user = request.user
        stock = Bookmarks.objects.filter(user=user.id)
        if not stock:
            return Response(data={"message": "No any stock bookmark"})
        serializer = BookmarkSerializer(stock, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def destroy(self, request, id=None, *args, **kwargs):
        """
        params: request => id
        return : stock are remove from bookmark
        """
        user = request.user
        print('id', id)
        if id:
            Bookmarks.objects.get(id=id, user=user.id).delete()
            return Response(data={"message": "stock are remove from bookmark"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "you do not pass any id"})


class OffersView(ModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offers.objects.all()
    # authentication_classes = [OAuth2Authentication]

    def list(self, request, *args, **kwargs):
        offer = Offers.objects.all()
        serializer = OfferSerializer(offer, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None, *args, **kwargs):
        try:
            offer = Offers.objects.get(id=id)
            serializer = OfferSerializer(offer)
            data = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
