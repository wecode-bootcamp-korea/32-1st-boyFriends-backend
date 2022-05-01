from django.http     import JsonResponse
from django.views    import View

from products.models import Product

from core.utils      import login_decorator

class ProductDetailView(View):
    @login_decorator
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        size_stocks = product.sizestock_set.filter(product_id=product_id)
        reviews = product.review_set.filter(product_id=product_id) if product.review_set.filter(product_id=product_id) else None

        results = [
            {
                "id"       : product_id,
                "itemTitle": product.category.sub,
                "category" : product.category.main_category.main,
                "userName" : request.user.name if request.user else None,
                "img"      : product.image_set.first().image_urls if product.image_set.filter(image_type_id=1) else None,
                "price"    : product.price,
                "productOptioin": [
                    {
                        "id"      : size_stock.id,
                        "size"    : size_stock.size.size if size_stock.size else None,
                        "stock"   : size_stock.stock.stock,
                        "category": product.category.main_category.main
                    } for size_stock in size_stocks
                ],
                "단품"   : "null",
                "sale"  : product.discount,
                "review": [
                    {
                        "id"           : review.id,
                        "reviewerName" : review.user.name,
                        "reviewContent": review.comment,
                        "reputation"   : review.rating,
                        "reivewImg"    : review.image_set.first().image_urls if review.image_set.filter(review_id=review.id) else None
                    } for review in reviews
                ]
            }
        ]
        return JsonResponse({"results": results}, status=200)
