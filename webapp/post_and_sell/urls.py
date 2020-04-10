from django.urls import path
from .views import PostAndSell, ManagePosting, PublicSalesOrder, PublicOrderHistory,Events, AdminProductView, AdminManagePostings, AdminPriceAndFee
urlpatterns = [
	path('post',PostAndSell.as_view(), name='post'),
	path('post-list',ManagePosting.as_view(), name='post_list'),
	path('my-sales-order', PublicSalesOrder.as_view(), name='public_sales_order'),
	path('my-order-history', PublicOrderHistory.as_view(), name='public_order_history'),
	path('multiple-events',Events.as_view(), name='multiple_events'),
	path('product-list',AdminProductView.as_view(), name='product_list'),
	path('price-and-price',AdminPriceAndFee.as_view(), name='price_and_fee'),
	path('admin-manage-postings',AdminManagePostings.as_view(), name='admin_manage_postings'),

]