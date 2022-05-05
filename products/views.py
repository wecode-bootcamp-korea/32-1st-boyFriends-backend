import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product, Review, Category

from core.utils      import identification_decorator, login_decorator


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
      
      
class ProductDetailView(View):
    @identification_decorator
    def get(self, request, product_id):
        DETAIL = 1

        product     = Product.objects.get(id=product_id)
        size_stocks = product.sizestock_set.filter()
        reviews     = product.review_set.filter()
        detail_imgs = product.image_set.filter(image_type_id=DETAIL)

        results = [
            {
                "id"       : product_id,
                "itemTitle": product.name,
                "category" : product.category.main_category.main,
                "userName" : request.user.name if request.user else None,
                "img"      : [detail_img.image_urls for detail_img in detail_imgs],
                "price"    : product.price,
                "productOptioin": [
                    {
                        "id"      : size_stock.id,
                        "size"    : size_stock.size.size,
                        "stock"   : size_stock.stock.stock,
                        "category": product.category.main_category.main
                    } for size_stock in size_stocks
                ],
                "sale"  : product.discount,
                "status": product.product_status.status if product.product_status else None,
                "review": [
                    {
                        "id"           : review.id,
                        "reviewerName" : review.user.name,
                        "reviewContent": review.comment,
                        "reputation"   : review.rating,
                        "reivewImg"    : review.image_set.first().image_urls if review.image_set.filter() else None
                    } for review in reviews
                ]
            }
        ]
        return JsonResponse({"results": results}, status=200)


class JustProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        DETAIL  = 1

        results = [
            {
                "id"           : product_id,
                "itemTitle"    : product.category.sub,
                "category"     : product.category.main_category.main,
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
        size_stocks = product.sizestock_set.filter()

        results = [
            {
                "id"       : size_stock.id,
                "size"     : size_stock.size.size,
                "stock"    : size_stock.stock.stock,
                "category" : product.category.main_category.main,
                "itemTitle": product.category.sub
            } for size_stock in size_stocks
        ]
        return JsonResponse({"results": results}, status=200)
      
      
class ReviewView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        user_id    = request.user.id
        rating     = data["rating"]
        comment    = data["comment"]
        product_id = data["product_id"]

        Review.objects.create(
            rating     = rating,
            comment    = comment,
            product_id = product_id,
            user_id    = user_id
        )
        return JsonResponse({"message": "REVIEW_CREATED"}, status=201)

    def get(self, request, review_id):
        review      = Review.objects.get(id=review_id)
        review_imgs = review.image_set.filter(review_id=review.id) if review.image_set.exists() else None

        results = [
            {
                "id"           : review.id,
                "reviewerName" : review.user.name,
                "productId"    : review.product.id,
                "reviewContent": review.comment,
                "reputation"   : review.rating,
                "reivewImgs"   : [review_img.image_urls for review_img in review_imgs],
                "created_at"   : review.created_at,
                "updated_at"   : review.updated_at
            }
        ]
        return JsonResponse({"results": results}, status=200)

    @login_decorator
    def patch(self, request, review_id):
        data = json.loads(request.body)

        user_id = request.user.id

        existing_review = Review.objects.get(id=review_id, user_id=user_id)

        rating  = data.get("rating", existing_review.rating)
        comment = data.get("comment", existing_review.comment)

        existing_review.rating  = rating
        existing_review.comment = comment
        existing_review.save()
        return JsonResponse({"message": "REVIEW_MODIFIED"}, status=205)

    @login_decorator
    def delete(self, request):
        review_ids = request.GET.getlist("review_ids")
        user_id    = request.user.id

        Review.objects.filter(id__in=review_ids, user_id=user_id).delete()
        return JsonResponse({'message': 'REVIEW_DELETED'}, status=204)