from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ..models import (
    DemolitionRequest,
    SellRequest,
    Antique
)
from ..serializers import (
    DemolitionRequestSerializer,
    SellRequestSerializer,
    UserSerializer,
    AntiqueSerializer
)

# ------------------ Demolition Requests ------------------

class DemolitionRequestView(APIView):
    """Submit a new demolition request."""

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = DemolitionRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Send WebSocket update to the dashboard
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {"type": "send_update"},
            )

            return Response({'message': 'Demolition request submitted successfully!'}, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_demolish_requests(request):
    """Retrieve all demolition requests."""
    try:
        demolish_requests = DemolitionRequest.objects.all()
        serializer = DemolitionRequestSerializer(demolish_requests, many=True)
        return Response(serializer.data)
    except Exception as e:
        print("Error fetching demolish requests:", str(e))
        return Response({"error": "Something went wrong"}, status=500)


@login_required
def demolition_count(request):
    """Get total demolition request count."""
    count = DemolitionRequest.objects.count()
    return JsonResponse({"count": count})


@login_required
def demolition_list(request):
    """Retrieve a list of all demolition requests."""
    data = list(DemolitionRequest.objects.values())
    return JsonResponse(data, safe=False)


# ------------------ Sell Requests ------------------

class SellRequestView(APIView):
    """Submit a new sell request."""

    def post(self, request, *args, **kwargs):
        serializer = SellRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Send WebSocket update to the dashboard
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "dashboard_updates",
                {"type": "send_update"},
            )

            return Response({'message': 'Sell request submitted successfully!'}, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_sell_requests(request):
    """Retrieve all sell requests."""
    sell_requests = SellRequest.objects.all()
    serializer = SellRequestSerializer(sell_requests, many=True)
    return Response(serializer.data)


@login_required
def sell_count(request):
    """Get total sell request count."""
    count = SellRequest.objects.count()
    return JsonResponse({"count": count})


@login_required
def sell_list(request):
    """Retrieve a list of all sell requests."""
    data = list(SellRequest.objects.values())
    return JsonResponse(data, safe=False)


# ------------------ User Account Management ------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accounts(request):
    """Retrieve all non-superuser accounts."""
    users = User.objects.filter(is_superuser=False)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def toggle_account_status(request, user_id):
    """Activate or deactivate a user account."""
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
    """Delete a user account (Admin only)."""
    try:
        user = User.objects.get(id=user_id)

        if request.user.is_superuser:
            user.delete()
            return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# ------------------ Analytics ------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_analytics(request):
    """Get total counts of sell and demolish requests."""
    total_sell_requests = SellRequest.objects.count()
    total_demolish_requests = DemolitionRequest.objects.count()
    
    return Response({
        "total_sell_requests": total_sell_requests,
        "total_demolish_requests": total_demolish_requests
    })


# ------------------ Antique Listings ------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_antiques(request):
    """Retrieve all antiques."""
    antiques = Antique.objects.all()
    
    if not antiques.exists():
        return Response({"message": "No antiques found."}, status=status.HTTP_204_NO_CONTENT)
    
    serializer = AntiqueSerializer(antiques, many=True)
    return Response(serializer.data)
