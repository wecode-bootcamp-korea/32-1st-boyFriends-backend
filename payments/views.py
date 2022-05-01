import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product
from payments.models import Cart

from core.utils      import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        user_id    = request.user
        product_id = data["product_id"]
        count      = data["count"]
        check_box  = data["isChecked"]

        cart, created  = Cart.objects.get_or_creat(
            user_id    = user_id,
            product_id = product_id,
            count      = count,
            check_box  = check_box
        )
        if not created:
            cart.save()
        return JsonResponse({"results": results}, status=201)

    @login_decorator
    def get(self, request):
        carts      = Cart.object.filter(user_id=request.user)
        sizestocks = cart.product.sizestock_set.filter(product_id=cart.product.id)

        results = [
            {
                "id"       : cart.product_id,
                "img"      : cart.product.image_set.filter(image_type_id=2).first().image_url if cart.product.image_set.filter(image_type_id=2) else None,
                "name"     : cart.product.name,
                "price"    : cart.product.price,
                "size"     : [(sizestock.size.size for sizestock in sizestocks) if sizestocks.size else "단품"],
                "sale"     : cart.product.discount,
                "stock"    : [sizestock.stock.stock for sizestock in sizestocks],
                "isChecked": cart.check_box,
                "cart_id"  : cart.id
            } for cart in carts
        ]
        return JsonResponse({"results": results}, status=200)

    @login_decorator
    def delete(self, request):
        cart_ids = request.GET.getlist('cart_ids', None)
        user_id  = request.user

        if cart_ids is None:
            return JsonResponse({'message': 'CART_EMPTY'}, status=404)

        Cart.objects.filter(id__in=cart_ids, user_id=user_id).delete()
        return JsonResponse({'message': 'CART_DELETED'}, status=204)