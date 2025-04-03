# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404

# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from google.auth.transport import requests
# from google.oauth2 import id_token

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# from .models import (
#     Item,
#     HeritageHouse,
#     DemolitionRequest,
#     SellRequest,
# )
# from .serializers import (
#     ItemSerializer,
#     HeritageHouseSerializer,
#     DemolitionRequestSerializer,
#     SellRequestSerializer,
#     UserSerializer,
# )

# # ------------------ Item & HeritageHouse APIs ------------------

# class ItemListView(APIView):
#     def get(self, request):
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)

# class HeritageHouseList(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         heritage_houses = HeritageHouse.objects.all()
#         serializer = HeritageHouseSerializer(heritage_houses, many=True)
#         return Response(serializer.data)

# # ------------------ Google Authentication ------------------

# class GoogleLoginView(APIView):
#     def post(self, request):
#         token = request.data.get('token')
#         try:
#             idinfo = id_token.verify_oauth2_token(token, requests.Request(), "YOUR_GOOGLE_CLIENT_ID")
#             email = idinfo.get('email')
#             name = idinfo.get('name')

#             user, created = User.objects.get_or_create(email=email, defaults={"username": name})
#             auth_token, _ = Token.objects.get_or_create(user=user)

#             return Response({'token': auth_token.key})
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # ------------------ Traditional Registration & Login ------------------


# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         data = request.data
#         username = data.get("username")
#         email = data.get("email")
#         password = data.get("password")

#         # Check if email or username already exists
#         if User.objects.filter(username=username).exists():
#             return Response({"message": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             return Response({"message": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

#         # Create user
#         user = User(
#             username=username,
#             email=email,
#         )
#         user.set_password(password)  # ✅ Hashes the password
#         user.save()

#         return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         identifier = request.data.get("identifier")  # Can be username or email
#         password = request.data.get("password")

#         if not identifier or not password:
#             return Response({"message": "Username/Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Try to find user by username or email
#         user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()

#         if not user:
#             return Response({"message": "Invalid username/email or password."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Authenticate user
#         user = authenticate(username=user.username, password=password)

#         if user is None:
#             return Response({"message": "Invalid username/email or password."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Generate or get existing token
#         token, created = Token.objects.get_or_create(user=user)

#         return Response({
#             "token": token.key,  # 🔑 This is the token you should use in the frontend
#             "is_superuser": user.is_superuser,  # ✅ Helps redirect superusers
#             "message": "Login successful"
#         }, status=status.HTTP_200_OK)


# # ------------------ Heritage House JSON Response ------------------

# def heritage_houses(request):
#     houses = HeritageHouse.objects.all()
#     data = [
#         {
#             "id": house.id,
#             "name": house.name,
#             "description": house.description,
#             "latitude": float(house.latitude),
#             "longitude": float(house.longitude),
#             "image": house.image.url if house.image else None,
#         }
#         for house in houses
#     ]
#     return JsonResponse(data, safe=False)

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def upload_profile_picture(request):
#     user = request.user

#     if "profile_picture" not in request.FILES:
#         return JsonResponse({"error": "No file uploaded"}, status=400)

#     image = request.FILES["profile_picture"]
#     filename = f"profile_pics/{user.id}_{image.name}"
#     file_path = default_storage.save(filename, ContentFile(image.read()))

#     user.userprofile.profile_picture = file_path
#     user.userprofile.save()

#     return JsonResponse({"profile_picture": request.build_absolute_uri(file_path)})

# @login_required
# def get_user_profile(request):
#     user = request.user
#     return JsonResponse({
#         "name": user.userprofile.name,
#         "email": user.email,
#         "profile_picture": user.userprofile.profile_picture.url if user.userprofile.profile_picture else None,
#     })

# class DemolitionRequestView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         serializer = DemolitionRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
            
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 "dashboard_updates",
#                 {"type": "send_update"},
#             )

#             return Response({'message': 'Demolition request submitted successfully!'}, status=201)
#         return Response(serializer.errors, status=400)

# class SellRequestView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = SellRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 "dashboard_updates",
#                 {"type": "send_update"},
#             )

#             return Response({'message': 'Sell request submitted successfully!'}, status=201)
#         return Response(serializer.errors, status=400)

# def demolition_count(request):
#     count = DemolitionRequest.objects.count()
#     return JsonResponse({"count": count})

# def sell_count(request):
#     count = SellRequest.objects.count()
#     return JsonResponse({"count": count})

# @login_required
# def demolition_list(request):
#     data = list(DemolitionRequest.objects.values())
#     return JsonResponse(data, safe=False)

# @login_required
# def sell_list(request):
#     data = list(SellRequest.objects.values())
#     return JsonResponse(data, safe=False)

# @api_view(["GET"])
# @permission_classes([AllowAny])
# def get_sell_requests(request):
#     sell_requests = SellRequest.objects.all()
#     serializer = SellRequestSerializer(sell_requests, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# @permission_classes([AllowAny])  # 👈 Ensures public access
# def get_demolish_requests(request):
#     try:
#         demolish_requests = DemolitionRequest.objects.all()
#         serializer = DemolitionRequestSerializer(demolish_requests, many=True)
#         return Response(serializer.data)
#     except Exception as e:
#         print("Error fetching demolish requests:", str(e))
#         return Response({"error": "Something went wrong"}, status=500)

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_accounts(request):
#     users = User.objects.filter(is_superuser=False)
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# @api_view(["PATCH"])
# @permission_classes([IsAuthenticated])
# def toggle_account_status(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#         user.is_active = not user.is_active
#         user.save()
#         return Response({"message": "User status updated"}, status=status.HTTP_200_OK)
#     except User.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# @api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
# def delete_account(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)

#         if request.user.is_superuser:
#             user.delete()
#             return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
#     except User.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_analytics(request):
#     total_sell_requests = SellRequest.objects.count()
#     total_demolish_requests = DemolitionRequest.objects.count()
    
#     return Response({
#         "total_sell_requests": total_sell_requests,
#         "total_demolish_requests": total_demolish_requests
#     })

# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from .models import Antique
# from .serializers import AntiqueSerializer

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])  # Requires authentication
# def get_antiques(request):
#     antiques = Antique.objects.all()
    
#     if not antiques.exists():
#         return Response({"message": "No antiques found."}, status=204)  # Send a proper response
    
#     serializer = AntiqueSerializer(antiques, many=True)
#     return Response(serializer.data)



# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Cart, CartItem, Antique



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_to_cart(request):
#     user = request.user
#     antique_id = request.data.get('antique_id')
#     quantity = int(request.data.get('quantity', 1))

#     try:
#         antique = Antique.objects.get(id=antique_id)
#         cart, _ = Cart.objects.get_or_create(user=user)

#         cart_item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             antique=antique,
#             defaults={'quantity': quantity}
#         )

#         if not created:
#             cart_item.quantity += quantity
#             cart_item.save()  # ✅ Ensure item is updated

#         # ✅ Return updated count
#         total_items = sum(item.quantity for item in cart.items.all())
#         return Response({"message": "Item added to cart", "total_items": total_items}, status=status.HTTP_201_CREATED)

#     except Antique.DoesNotExist:
#         return Response({"error": "Antique not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_cart_count(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user).first()  # ✅ Avoids creating a new empty cart

#     if not cart:
#         return Response({"total_items": 0})  # 🚨 No cart means no items

#     total_items = sum(item.quantity for item in cart.items.all())

#     return Response({"total_items": total_items})

# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .models import Cart

# @login_required
# def cart_count(request):
#     try:
#         cart = Cart.objects.get(user=request.user)
#         total_items = sum(item.quantity for item in cart.items.all())
#         return JsonResponse({"total_items": total_items})
#     except Cart.DoesNotExist:
#         return JsonResponse({"total_items": 0})  # Return 0 if user has no cart




# # views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Cart
# from .serializers import CartSerializer

# class CartView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             cart = Cart.objects.get(user=request.user)
#             serializer = CartSerializer(cart)
#             return Response(serializer.data, status=200)
#         except Cart.DoesNotExist:
#             print(f"🚨 Cart not found for user: {request.user.username}")  # Debugging log
#             return Response({"error": "Cart not found."}, status=404)




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from .models import Cart, CartItem

# class CartItemUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, item_id):
#         try:
#             # Get the authenticated user's cart
#             cart = Cart.objects.get(user=request.user)
            
#             # Ensure the item belongs to the user's cart
#             cart_item = CartItem.objects.get(id=item_id, cart=cart)

#             new_quantity = request.data.get("quantity")
            
#             if new_quantity is None or int(new_quantity) <= 0:
#                 return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

#             cart_item.quantity = int(new_quantity)
#             cart_item.save()

#             return Response({"message": "Quantity updated successfully"}, status=status.HTTP_200_OK)
#         except Cart.DoesNotExist:
#             return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
#         except CartItem.DoesNotExist:
#             return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)
#         except ValueError:
#             return Response({"error": "Invalid quantity format"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Cart, CartItem

# @api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
# def delete_cart_item(request, item_id):
#     try:
#         cart = Cart.objects.get(user=request.user)
#         cart_item = CartItem.objects.get(id=item_id, cart=cart)
#         cart_item.delete()
#         return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#     except Cart.DoesNotExist:
#         return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
#     except CartItem.DoesNotExist:
#         return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User

# @receiver(post_save, sender=User)
# def create_user_cart(sender, instance, created, **kwargs):
#     if created:
#         Cart.objects.create(user=instance)  # ✅ Ensure every user has a cart


from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from google.auth.transport import requests
from google.oauth2 import id_token

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import (
    Item,
    HeritageHouse,
    DemolitionRequest,
    SellRequest,
)
from .serializers import (
    ItemSerializer,
    HeritageHouseSerializer,
    DemolitionRequestSerializer,
    SellRequestSerializer,
    UserSerializer,
)

# ------------------ Item & HeritageHouse APIs ------------------

class ItemListView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class HeritageHouseList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        heritage_houses = HeritageHouse.objects.all()
        serializer = HeritageHouseSerializer(heritage_houses, many=True)
        return Response(serializer.data)

# ------------------ Google Authentication ------------------

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "YOUR_GOOGLE_CLIENT_ID")
            email = idinfo.get('email')
            name = idinfo.get('name')

            user, created = User.objects.get_or_create(email=email, defaults={"username": name})
            auth_token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': auth_token.key})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ------------------ Traditional Registration & Login ------------------


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Check if email or username already exists
        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)  # ✅ Hashes the password
        user.save()

        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")  # Can be username or email
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"message": "Username/Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Try to find user by username or email
        user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()

        if not user:
            return Response({"message": "Invalid username/email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate user
        user = authenticate(username=user.username, password=password)

        if user is None:
            return Response({"message": "Invalid username/email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate or get existing token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,  # 🔑 This is the token you should use in the frontend
            "is_superuser": user.is_superuser,  # ✅ Helps redirect superusers
            "message": "Login successful"
        }, status=status.HTTP_200_OK)


# ------------------ Heritage House JSON Response ------------------

def heritage_houses(request):
    houses = HeritageHouse.objects.all()
    data = [
        {
            "id": house.id,
            "name": house.name,
            "description": house.description,
            "latitude": float(house.latitude),
            "longitude": float(house.longitude),
            "image": house.image.url if house.image else None,
        }
        for house in houses
    ]
    return JsonResponse(data, safe=False)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_profile_picture(request):
    user = request.user

    if "profile_picture" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    image = request.FILES["profile_picture"]
    filename = f"profile_pics/{user.id}_{image.name}"
    file_path = default_storage.save(filename, ContentFile(image.read()))

    user.userprofile.profile_picture = file_path
    user.userprofile.save()

    return JsonResponse({"profile_picture": request.build_absolute_uri(file_path)})

@login_required
def get_user_profile(request):
    user = request.user
    return JsonResponse({
        "name": user.userprofile.name,
        "email": user.email,
        "profile_picture": user.userprofile.profile_picture.url if user.userprofile.profile_picture else None,
    })

class DemolitionRequestView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = DemolitionRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {"type": "send_update"},
            )

            return Response({'message': 'Demolition request submitted successfully!'}, status=201)
        return Response(serializer.errors, status=400)

class SellRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SellRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {"type": "send_update"},
            )

            return Response({'message': 'Sell request submitted successfully!'}, status=201)
        return Response(serializer.errors, status=400)

def demolition_count(request):
    count = DemolitionRequest.objects.count()
    return JsonResponse({"count": count})

def sell_count(request):
    count = SellRequest.objects.count()
    return JsonResponse({"count": count})

@login_required
def demolition_list(request):
    data = list(DemolitionRequest.objects.values())
    return JsonResponse(data, safe=False)

@login_required
def sell_list(request):
    data = list(SellRequest.objects.values())
    return JsonResponse(data, safe=False)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_sell_requests(request):
    sell_requests = SellRequest.objects.all()
    serializer = SellRequestSerializer(sell_requests, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])  # 👈 Ensures public access
def get_demolish_requests(request):
    try:
        demolish_requests = DemolitionRequest.objects.all()
        serializer = DemolitionRequestSerializer(demolish_requests, many=True)
        return Response(serializer.data)
    except Exception as e:
        print("Error fetching demolish requests:", str(e))
        return Response({"error": "Something went wrong"}, status=500)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accounts(request):
    users = User.objects.filter(is_superuser=False)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def toggle_account_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return Response({"message": "User status updated"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        if request.user.is_superuser:
            user.delete()
            return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_analytics(request):
    total_sell_requests = SellRequest.objects.count()
    total_demolish_requests = DemolitionRequest.objects.count()
    
    return Response({
        "total_sell_requests": total_sell_requests,
        "total_demolish_requests": total_demolish_requests
    })

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Antique
from .serializers import AntiqueSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Requires authentication
def get_antiques(request):
    antiques = Antique.objects.all()
    
    if not antiques.exists():
        return Response({"message": "No antiques found."}, status=204)  # Send a proper response
    
    serializer = AntiqueSerializer(antiques, many=True)
    return Response(serializer.data)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Antique



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    antique_id = request.data.get('antique_id')
    quantity = int(request.data.get('quantity', 1))

    try:
        antique = Antique.objects.get(id=antique_id)
        cart, _ = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            antique=antique,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()  # ✅ Ensure item is updated

        # ✅ Return updated count
        total_items = sum(item.quantity for item in cart.items.all())
        return Response({"message": "Item added to cart", "total_items": total_items}, status=status.HTTP_201_CREATED)

    except Antique.DoesNotExist:
        return Response({"error": "Antique not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart_count(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()  # ✅ Avoids creating a new empty cart

    if not cart:
        return Response({"total_items": 0})  # 🚨 No cart means no items

    total_items = sum(item.quantity for item in cart.items.all())

    return Response({"total_items": total_items})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def cart_count(request):
    try:
        cart = Cart.objects.get(user=request.user)
        total_items = sum(item.quantity for item in cart.items.all())
        return JsonResponse({"total_items": total_items})
    except Cart.DoesNotExist:
        return JsonResponse({"total_items": 0})  # Return 0 if user has no cart




# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=200)
        except Cart.DoesNotExist:
            print(f"🚨 Cart not found for user: {request.user.username}")  # Debugging log
            return Response({"error": "Cart not found."}, status=404)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem

class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        try:
            # Get the authenticated user's cart
            cart = Cart.objects.get(user=request.user)
            
            # Ensure the item belongs to the user's cart
            cart_item = CartItem.objects.get(id=item_id, cart=cart)

            new_quantity = request.data.get("quantity")
            
            if new_quantity is None or int(new_quantity) <= 0:
                return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

            cart_item.quantity = int(new_quantity)
            cart_item.save()

            return Response({"message": "Quantity updated successfully"}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid quantity format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        cart_item.delete()
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)  # ✅ Ensure every user has a cart
