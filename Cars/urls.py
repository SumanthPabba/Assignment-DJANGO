from django.urls import path
from . import views
from Users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='base'),
    path('base/', views.base, name='base'),
    path('index/', views.index, name='index'),
    path('available/', views.available, name='available'),
    path('addcar/', views.addcar, name='addcar'),
    path('updatecar/<int:id>', views.updateCar, name="updatecar"),
    path('deletecar/<int:id>/', views.delete, name='deletecar'),
    path('media/<slug:pid>/', views.get_image, name="get_image"),
    path('search/', views.search.as_view(), name="search"),
    path('book/<int:id>/', views.book, name='book'),
    path('order_list/', views.orders_list, name="order-list"),

    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
    path('password_reset/', user_views.password_reset_request, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', user_views.profile, name='profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)