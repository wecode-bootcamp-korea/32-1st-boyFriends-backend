import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product

from core.utils      import (
                         login_decorator,
                         identification_decorator
                     )

class ProductDetailView(View):
    @identification_decorator
    def get(self, request, product_id):
        DETAIL = 1

        product     = Product.objects.get(id=product_id)
        size_stocks = product.sizestock_set.filter(product_id=product_id)
        reviews     = product.review_set.filter(product_id=product_id) if product.review_set.filter(product_id=product_id) else None
        detail_imgs = product.image_set.filter(image_type_id=DETAIL)

        results = [
            {
                "id"       : product_id,
                "itemTitle": product.category.sub,
                "category" : product.category.main_category.main,
                "userName" : request.user.name if request.user else None,
                "img"      : [detail_img.image_urls for detail_img in detail_imgs],
                "price"    : product.price,
                "productOptioin": [
                    {
                        "id"      : size_stock.id,
                        "size"    : size_stock.size.size if size_stock.size else None,
                        "stock"   : size_stock.stock.stock,
                        "category": product.category.main_category.main
                    } for size_stock in size_stocks
                ],
                "sale"  : product.discount,
                "status": product.product_status,
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


class JustProductDetailView(View):
    @identification_decorator
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        DETAIL  = 1

        results = [
            {
                "id"           : product_id,
                "itemTitle"    : product.category.sub,
                "category"     : product.category.main_category.main,
                "userName"     : request.user.name if request.user else None,
                "img"          : product.image_set.first().image_urls if product.image_set.filter(image_type_id=DETAIL) else None,
                "price"        : product.price,
                "discount"     : product.discount,
                "discountPrice": ((product.price) * (100 - (product.discount))) // 100 if product.discount else product.price
            }
        ]
        return JsonResponse({"results": results}, status=200)


class ProductOptionView(View):
    def get(self, request, product_id):
        product     = Product.objects.get(id=product_id)
        size_stocks = product.sizestock_set.filter(product_id=product_id)

        results = [
            {
                "id"       : size_stock.id,
                "size"     : size_stock.size.size if size_stock.size else None,
                "stock"    : size_stock.stock.stock,
                "category" : product.category.main_category.main,
                "itemTitle": product.category.sub
            } for size_stock in size_stocks
        ]
        return JsonResponse({"results": results}, status=200)