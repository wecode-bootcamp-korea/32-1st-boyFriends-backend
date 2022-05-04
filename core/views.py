from django.http      import JsonResponse
from django.views     import View

from products.models  import Category

class TopicView(View):
    def get(self, request):
            categories = Category.objects.all()
            results = []
            for category in categories:
                products = category.product_set.all()

                results.append({
                "categoryId"     : category.id,
                "categoryName"   : category.sub,
                "categoryImg"    : category.image_set.get(category_id=category.id).image_urls,
                "product"        : [{
                                    "productId"       : product.id,
                                    "productName"     : product.name,
                                    "productImg"      : product.image_set.get(image_type_id = 2).image_urls if product.image_set.filter(image_type_id=2) else None,
                                    "productPrice"    : product.price,
                                    "productDiscount" : product.discount,
                                    "productStatus"   : product.product_status.status if product.product_status else None
                                    } for product in products]
                })
            return JsonResponse({"results": results}, status=200)