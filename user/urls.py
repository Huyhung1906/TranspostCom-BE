from django.urls import path, include
from .views import *
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('update/<int:pk>/', UpdateUserView.as_view(), name='user-update'),
    path('delete/<int:pk>/', DeleteUserView.as_view(), name='user-delete'),
    path('list/', ListUsersView.as_view(), name='list-users'),
    path('getuserbyid/<int:id>/', get_user_by_id_view, name='usersbyid'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]