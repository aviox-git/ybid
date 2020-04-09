from django.urls import path
from .views import PostView, ManagePosting, SalesOrder, OrderHistory,Events
urlpatterns = [
	path('post',PostView.as_view(), name='post'),
	path('post-list',ManagePosting.as_view(), name='post_list'),
	path('my-sales-order', SalesOrder.as_view(), name='public_sales_order'),
	path('my-order-history', OrderHistory.as_view(), name='public_order_history'),
	path('multiple-events',Events.as_view(), name='multiple_events'),

]