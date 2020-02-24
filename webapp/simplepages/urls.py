from django.urls import path
from .views import Homepage, FaqCategoryView, AddFaqCategory


urlpatterns = [
	path('', Homepage.as_view(), name="homepage"),


	# faqs
	path('faq-category', FaqCategoryView.as_view(), name="faq_category"),
	path('add-faq-category', AddFaqCategory.as_view(), name="add_faq_category"),
]