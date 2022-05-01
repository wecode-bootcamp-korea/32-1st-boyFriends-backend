from django.http     import JsonResponse
from django.views    import View

from products.models import Product
from payments.models import Cart

from core.utils      import login_decorator

class CartView(View):
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
                "isChecked": cart.check_box
            } for cart in carts
        ]
        return JsonResponse({"results": results}, status=200)
