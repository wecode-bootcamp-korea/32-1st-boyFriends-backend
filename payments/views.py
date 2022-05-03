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
        option     = data.get("size", None)

        Cart.objects.create(
            user_id    = user_id,
            product_id = product_id,
            count      = count,
            option     = option
        )
        return JsonResponse({"message": "CART_CREATED"}, status=201)

    @login_decorator
    def get(self, request):
        THUMBNAIL = 2

        carts = Cart.objects.filter(user_id=request.user)

        for cart in carts:
            sizestocks = cart.product.sizestock_set.filter(product_id=cart.product.id)

            size_stocks = [
                {
                "size": sizestock.size.size if sizestock.size else "단품",
                "stock": sizestock.stock.stock
                } for sizestock in sizestocks
            ]

        results = [
            {
                "productId" : cart.product_id,
                "img"       : cart.product.image_set.filter(image_type_id=THUMBNAIL).first().image_url if cart.product.image_set.filter(image_type_id=THUMBNAIL) else None,
                "name"      : cart.product.name,
                "price"     : cart.product.price,
                "size_stock": size_stocks,
                "count"     : cart.count,
                "sale"      : cart.product.discount,
                "isChecked" : cart.check_box,
                "cartId"    : cart.id
            } for cart in carts
        ]
        return JsonResponse({"results": results}, status=200)

    @login_decorator
    def patch(self, request):
        data = json.loads(request.body)

        cart_id = data["cart_id"]
        user_id = request.user

        existing_cart = Cart.objects.get(id=cart_id, user_id=user_id)

        count     = data.get("count", existing_cart.count)
        check_box = data.get("isChecked", existing_cart.check_box)
        option    = data.get("option", existing_cart.option)

        existing_cart.count     = count
        existing_cart.check_box = check_box
        existing_cart.option    = option

        existing_cart.save()
        return JsonResponse({"message": "COUNT_MODIFIED"}, status=205)

    @login_decorator
    def delete(self, request):
        cart_ids = request.GET.getlist('cart_ids', None)
        user_id  = request.user

        if cart_ids is None:
            return JsonResponse({'message': 'CART_EMPTY'}, status=404)

        Cart.objects.filter(id__in=cart_ids, user_id=user_id).delete()
        return JsonResponse({'message': 'CART_DELETED'}, status=204)