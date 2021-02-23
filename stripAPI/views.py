from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import stripe


class CreateCheckout(APIView):

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            stripe.api_key = "sk_test_51IGHpsLM8pLXgc6phmOBmKgxC26dLZwlGaSju80NqBWwtwooi02sCb6cZbN8v85Lc2otO6LDougRlnOygxDuu1ys00tqFR5k8h"
            checkout_session = stripe.checkout.Session.create(
                success_url="https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="https://example.com/canceled.html",
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": request.data['priceId'],
                        # For metered billing, do not pass quantity
                        "quantity": 1
                    }
                ],
            )
            return Response(data={'sessionId': checkout_session['id']}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': str(e)})
