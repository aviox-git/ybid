from django.urls import path
from .views import Registration, ForgetPass,ResetPassword,CheckEmail, LoginView, LogoutView, EmailVerification, AdminLogin,AdminLogout, WebAppUsers,EditWebAppUsers,SuperAdmin,DeleteAdmin,EditAdmin,AddStaff,AddWebAppUsers,AddRole,RoleList,DeleteRole,StaffList,EditRole,EditStaff, AdminSummary
urlpatterns = [
	# registration url 
	path('',Registration.as_view(), name='registration'),
	path('email_verification/<user_id>', EmailVerification.as_view(), name="email_verification"),
	path('check_email',CheckEmail.as_view(), name='check_email'),


	# login url
	path('admin-login',AdminLogin.as_view(), name='admin-login'),
	path('admin-logout',AdminLogout.as_view(), name='admin-logout'),
	path('login',LoginView.as_view(), name='login'),
	path('forget_password',ForgetPass.as_view(), name='forget_password'),
	path('reset_password/<str:code>',ResetPassword.as_view(), name='reset_password'),
	path('logout',LogoutView.as_view(), name='logout'),


	path('webapp-users',WebAppUsers.as_view(), name='webapp-users'),
	path('edit-webapp-users/<int:user_id>/',EditWebAppUsers.as_view(), name='edit_webapp_users'),
	path('add_web_user', AddWebAppUsers.as_view(), name="add_web_user"),

	# admin url 
	path('admin_home', AdminSummary.as_view(), name="admin_home"),
	path('super_admin', SuperAdmin.as_view(), name="super_admin"),
	path('delete_admin/<user_id>', DeleteAdmin.as_view(), name="delete_admin"),
	path('edit_admin/<user_id>', EditAdmin.as_view(), name="edit_admin"),
	path('add_staff', AddStaff.as_view(), name="add_staff"),
	path('staff_list', StaffList.as_view(), name="staff_list"),
	path('edit_staff/<user_id>', EditStaff.as_view(), name="edit_staff"),
	path('add_role', AddRole.as_view(), name="add_role"),
	path('role_list',RoleList.as_view(), name="role_list"),
	path('edit_role/<group_id>',EditRole.as_view(), name="edit_role"),
	path('delete_role/<group_id>',DeleteRole.as_view(), name="delete_role"),

	
]