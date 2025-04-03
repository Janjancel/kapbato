from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..models import Cart, CartItem, Antique
from ..serializers import CartSerializer


# ------------------ Add to Cart ------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add an item to the cart or update quantity if it already exists."""
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

        # ✅ Return updated cart count
        total_items = cart.items.aggregate(total_quantity=CartItem.Sum("quantity"))["total_quantity"] or 0
        return Response({"message": "Item added to cart", "total_items": total_items}, status=status.HTTP_201_CREATED)

    except Antique.DoesNotExist:
        return Response({"error": "Antique not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------ Get Cart Count ------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart_count(request):
    """Get total number of items in the user's cart."""
    cart = Cart.objects.filter(user=request.user).first()
    total_items = cart.items.aggregate(total_quantity=CartItem.Sum("quantity"))["total_quantity"] or 0
    return Response({"total_items": total_items}, status=status.HTTP_200_OK)


@login_required
def cart_count(request):
    """Django function-based view to get cart count."""
    cart = Cart.objects.filter(user=request.user).first()
    total_items = cart.items.aggregate(total_quantity=CartItem.Sum("quantity"))["total_quantity"] or 0
    return JsonResponse({"total_items": total_items}, status=200)


# ------------------ Retrieve Cart Details ------------------

class CartView(APIView):
    """Retrieve the authenticated user's cart details."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=200)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=404)


# ------------------ Update Cart Item Quantity ------------------

class CartItemUpdateView(APIView):
    """Update the quantity of an item in the cart."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)

            new_quantity = request.data.get("quantity")
            if not new_quantity or int(new_quantity) <= 0:
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


# ------------------ Remove Item from Cart ------------------

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, item_id):
    """Remove an item from the user's cart."""
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


# ------------------ Auto Create Cart for New Users ------------------

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """Automatically create a cart for new users."""
    if created:
        Cart.objects.create(user=instance)  # ✅ Ensure every user has a cart
