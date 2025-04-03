# from django.urls import path
# from .views import HeritageHouseList, GoogleLoginView, heritage_houses, register, login_view

# urlpatterns = [
#     path('heritage-houses/', HeritageHouseList.as_view(), name='heritage-houses-list'),
#     path('api/google-login/', GoogleLoginView.as_view(), name='google-login'),
#     path("api/heritage-houses/", heritage_houses, name="heritage-houses"),
#     path("register/", register, name="register"),
#     path("login/", login_view, name="login"),
# ]

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    HeritageHouseList,
    GoogleLoginView,
    heritage_houses,
    RegisterView,
    LoginView, 
    upload_profile_picture,
    get_user_profile,
    DemolitionRequestView,
    SellRequestView,
    demolition_count, 
    sell_count,
    demolition_list, sell_list, get_sell_requests, get_demolish_requests, get_accounts, toggle_account_status, delete_account, get_analytics, get_antiques, add_to_cart, get_cart_count,
    CartView, CartItemUpdateView, delete_cart_item, cart_count
)

urlpatterns = [
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Heritage House Endpoints
    path('api/heritage-houses/', HeritageHouseList.as_view(), name='heritage-houses-list'),
    path('api/heritage-houses/json/', heritage_houses, name='heritage-houses-json'),

    # Authentication Endpoints
    path('api/google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path("api/upload-profile-picture/", upload_profile_picture, name="upload-profile-picture"),
    path("api/user-profile/", get_user_profile, name="get-user-profile"),
    path('api/demolition/', DemolitionRequestView.as_view(), name='demolition-request'),
    path('api/sell/', SellRequestView.as_view(), name='sell-request'),
    path('api/demolition/count/', demolition_count),
    path('api/sell/count/', sell_count),
    path("api/demolition/", demolition_list, name="demolition_list"),
    path("api/sell/", sell_list, name="sell_list"),
    path('api/sell-requests/', get_sell_requests, name='sell-requests'),
    path("api/demolish-requests/", get_demolish_requests, name="demolish-requests"),
    path("api/accounts/", get_accounts, name="accounts"),
    path("accounts/<int:user_id>/", toggle_account_status, name="toggle_account_status"),
    path("accounts/<int:user_id>/delete/", delete_account, name="delete_account"),
    path("api/analytics/", get_analytics, name="get_analytics"),
    path("antiques/", get_antiques, name="get_antiques"),
    path("api/cart/add/", add_to_cart, name="add_to_cart"), 
    path("cart/count/", get_cart_count, name="cart-count"),
    path('api/cart/', CartView.as_view(), name='cart'),
    path("cart/<int:item_id>/", CartItemUpdateView.as_view(), name="cart-item-update"),
    path("api/cart/item/<int:item_id>/", delete_cart_item, name="delete_cart_item"),
    path("cart/count/", cart_count, name="cart-count"), 


]
