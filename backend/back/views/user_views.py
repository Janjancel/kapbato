# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def upload_profile_picture(request):
#     """Handles user profile picture upload."""
#     user = request.user

#     if "profile_picture" not in request.FILES:
#         return JsonResponse({"error": "No file uploaded"}, status=400)

#     image = request.FILES["profile_picture"]
#     filename = f"profile_pics/{user.id}_{image.name}"

#     # Save file to default storage
#     file_path = default_storage.save(filename, ContentFile(image.read()))

#     # Update user profile with new profile picture
#     user.userprofile.profile_picture = file_path
#     user.userprofile.save()

#     return JsonResponse({
#         "message": "Profile picture uploaded successfully!",
#         "profile_picture": request.build_absolute_uri(default_storage.url(file_path))
#     }, status=200)


# @login_required
# def get_user_profile(request):
#     """Returns the authenticated user's profile information."""
#     user = request.user

#     return JsonResponse({
#         "name": user.userprofile.name,
#         "email": user.email,
#         "profile_picture": request.build_absolute_uri(user.userprofile.profile_picture.url)
#         if user.userprofile.profile_picture else None,
#     }, status=200)

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ..serializers import UserSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_profile_picture(request):
    """Handles user profile picture upload."""
    user = request.user

    if "profile_picture" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    image = request.FILES["profile_picture"]
    filename = f"profile_pics/{user.id}_{image.name}"

    # Save file to default storage
    file_path = default_storage.save(filename, ContentFile(image.read()))

    # Update user profile with new profile picture
    user.userprofile.profile_picture = file_path
    user.userprofile.save()

    return JsonResponse({
        "message": "Profile picture uploaded successfully!",
        "profile_picture": request.build_absolute_uri(default_storage.url(file_path))
    }, status=200)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from back.serializers.profile_serializers import UserProfileSerializer
from ..models import UserProfile

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Fetch the currently logged-in user's profile details."""
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(user_profile, context={"request": request})
    return Response(serializer.data)

