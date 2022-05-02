import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product

from core.utils      import login_decorator

class ProductDetailView(View):
    @login_decorator
    def get(self, request, product_id):
        product     = Product.objects.get(id=product_id)
        size_stocks = product.sizestock_set.filter(product_id=product_id)
        reviews     = product.review_set.filter(product_id=product_id) if product.review_set.filter(product_id=product_id) else None

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



class JustProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)

        results = [
            {
                "id"            : product_id,
                "itemTitle"     : product.category.sub,
                "category"      : product.category.main_category.main,
                "userName"      : request.user.name if request.user else None,
                "img"           : product.image_set.first().image_urls if product.image_set.filter(image_type_id=1) else None,
                "price"         : product.price,
                "discount"      : product.discount,
                "discount_price": ((product.price) * (100 - (product.discount))) // 100 if product.discount else product.price
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

class ReviewView(View):
    @login_decorator
    def post(self, reqeust):
        data = json.loads(reqeust.body)

        user_id = reqeust.user
        rating = data["rating"]
        comment = data["comment"]
        product_id = data["product_id"]

        Review.objects.create(
            rating     = rating,
            comment    = comment,
            product_id = product_id,
            user_id    = user_id
        )
        return JsonResponse({"message": "REVIEW_CREATED"}, status=201)

    @login_decorator
    def patch(self, review_id):
        data    = json.loads(request.body)
        user_id = request.user
        rating  = data.get("rating", None)
        comment = data.get("comment", None)

        if Review.objects.filter(id=review_id).exists():
            review         = Review.objects.get(id=review_id, user_id=user_id)
            review.rating  = rating
            review.comment = comment
            review.save()
        return JsonResponse({"message": "REVIEW_MODIFIED"}, status=205)

    def get(self, request, product_id):
        product         = Product.objects.get(id=product_id)
        reviews         = product.review_set.filter(product_id=product_id) if product.review_set.filter(product_id=product_id) else None
        order_condition = request.GET.get("order", "recent")
        page            = int(request.GET.get("page", 1))
        offset          = int(request.GET.get("offset", 2))

        end   = page * offset
        start = end - offset

        results = [
            {
                "id"           : review.id,
                "reviewerName" : review.user.name,
                "productSize"  : product.sizestock_set.size.size if product.sizestock_set.size else None,
                "reviewContent": review.comment,
                "reputation"   : review.rating,
                "reivewImg"    : review.image_set.first().image_urls if review.image_set.filter(review_id=review.id) else None,
                "reviewCount"  : len(product.review_set.filter(product_id=product.id)) if product.review_set.filter(product_id=product.id) else None,
                "created_at"   : review.created_at
                # "ratingRatios" : [rating_ratio] for rating_ratio in rating_ratios
            } for review in reviews
        ]

        if order_condition == "recent":
            results = sorted(results, key=lambda review: review["created_at"], reverse=True)

        if order_condition == "high_rating":
            results = sorted(results, key=lambda review: review["reputation"] if product["reputation"] else 0, reverse=True)
        if order_condition == "low_rating":
            results = sorted(results, key=lambda review: review["reputation"] if product["reputation"] else 0)

        results = results[start:end]
        return JsonResponse({"results": results}, status=200)

    @login_decorator
    def delete(self, request):
        review_ids = request.GET.getlist("review_ids")
        user_id    = request.user

        Review.objects.filter(id__in=review_ids, user_id=user_id).delete()
        return JsonResponse({'message': 'REVIEW_DELETED'}, status=204)
