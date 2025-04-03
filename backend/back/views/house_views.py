from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Item, HeritageHouse
from ..serializers import ItemSerializer, HeritageHouseSerializer

class ItemListView(APIView):
    """API View to fetch all items."""
    
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=200)


class HeritageHouseList(APIView):
    """API View to fetch all heritage houses."""
    
    permission_classes = [AllowAny]

    def get(self, request):
        heritage_houses = HeritageHouse.objects.all()
        serializer = HeritageHouseSerializer(heritage_houses, many=True)
        return Response(serializer.data, status=200)


def heritage_houses(request):
    """Django function-based view to fetch all heritage houses (JSON response)."""
    
    houses = HeritageHouse.objects.values(
        "id", "name", "description", "latitude", "longitude", "image"
    )

    data = [
        {
            "id": house["id"],
            "name": house["name"],
            "description": house["description"],
            "latitude": float(house["latitude"]),
            "longitude": float(house["longitude"]),
            "image": request.build_absolute_uri(house["image"]) if house["image"] else None,
        }
        for house in houses
    ]

    return JsonResponse(data, safe=False, status=200)
