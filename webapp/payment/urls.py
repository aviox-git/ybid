from django.conf.urls import url, include
from django.urls import path
from .views import StripeAccount, PaymentSuccessfull,  PaymentFailed

urlpatterns = [
	path('payment_successful/', PaymentSuccessfull.as_view(), name="payment_successful"),
	path('payment_failed/', PaymentFailed.as_view(), name="payment_failed"),
	path('stripe-account', StripeAccount.as_view(), name="stripe_account"),


]
