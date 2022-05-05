from django.http      import JsonResponse
from django.views     import View

from products.models  import Category

class TopicView(View):
    def get(self, request):
        THUMBNAIL = 2
        TOPIC     = 4

        results =[{
            "categoryId"   : category.id,
            "categoryName" : category.sub,
            "categoryImg"  : category.image_set.get(image_type_id=TOPIC).image_urls,
            "product"      : [{
                "productId"       : product.id,
                "productName"     : product.name,
                "productImg"      : product.image_set.get(image_type_id=THUMBNAIL).image_urls if product.image_set.filter(image_type_id=THUMBNAIL) else None,
                "productPrice"    : product.price,
                "productDiscount" : product.discount,
                "productStatus"   : product.product_status.status if product.product_status else None
            } for product in category.product_set.all()]
        } for category in Category.objects.all()]
        
        return JsonResponse({"results": results}, status=200)