from django.urls import path
from .views import Homepage, FAQWeb, FAQCategoryView,ContactCategoriesView, AdminContactList, ContactCategoriesEditView, AddFAQCategoryView,ContactCategoryAdd, EditFAQCategoryView, FAQView, AddFAQView, EditFAQView,  BlogCategoriesView, BlogCategoriesAddView, BlogCategoriesEditView, BlogWebView, BlogView, AddBlogView, EditBlogView, Pages, AddPage,PageStatus, DeletePage, EditPage,SelectedPagesStatus,SingleBlog,GetPages, Contact


urlpatterns = [
	path('', Homepage.as_view(), name="homepage"),
	path('contact_us', Contact.as_view(), name="contact_us"),



	path('add-contact-category', ContactCategoryAdd.as_view(), name="add_contact_category"),
	path('contact-category', ContactCategoriesView.as_view(), name="contact_category"),
	path('contact-category-edit/<int:cat_id>', ContactCategoriesEditView.as_view(), name="contact_category_edit"),
	path('public-contact-list', AdminContactList.as_view(), name="public_contact_list"),

	# Pages
	path('pages',Pages.as_view(), name='pages'),
    path('add-page',AddPage.as_view(), name='ticket-add-pages'),
    path('page-status',PageStatus.as_view()),
    path('delete-page',DeletePage.as_view()),
    path('edit-page/<page_id>',EditPage.as_view(), name="edit_page"),
    path('selected-pages-status',SelectedPagesStatus.as_view()),  


	#faq categories
	path('faqs', FAQWeb.as_view(), name="faq_web"),
	path('faq-category', FAQCategoryView.as_view(), name = 'faq_category'),
    path('faq-category-add', AddFAQCategoryView.as_view(),name='faq_category_add' ),
    path('faq-category-edit/<int:cat_id>', EditFAQCategoryView.as_view(),name='faq_category_edit' ),
    
    # FAQs
    path('faq', FAQView.as_view(),name='faqs'),
    path('faq-add', AddFAQView.as_view(),name='faq_add' ),
    path('faq-edit/<int:faq_id>', EditFAQView.as_view(),name='faq_edit' ),


    #Blog Categories
	path('blog',BlogWebView.as_view(), name='blog'),
	path('blog-category',BlogCategoriesView.as_view(), name='blog_category'),
	path('blog-category-add',BlogCategoriesAddView.as_view(), name='blog_category_add'),
	path('blog-category-edit/<int:cat_id>', BlogCategoriesEditView.as_view(), name='blog_category_edit'),

	#Blogs
	path('blogs', BlogView.as_view(),name='blogs'),
	path('blogs-add', AddBlogView.as_view(),name='blog_add' ),
	path('blogs-edit/<int:blog_id>', EditBlogView.as_view(),name='blog_edit' ),
	path('blog-details/<int:blog_id>',SingleBlog.as_view(), name='single_blog'),
	path('<page>',GetPages.as_view(),name='page')


]