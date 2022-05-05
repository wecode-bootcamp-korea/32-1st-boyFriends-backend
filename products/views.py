import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import (
                          Q,
                          F,
                          Case,
                          When,
                          Avg,
                          Count,
                      )

from core.utils       import identification_decorator, login_decorator

from products.models  import Product, Review, Category


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
      

class ProductsListView(View):
    def get(self, request):
        category_id      = request.GET.get("category_id", None)
        main_category_id = request.GET.get("main_category_id", None)
        order_condition  = request.GET.get("order", "high_rating")
        search           = request.GET.get("search", None)
        offset           = int(request.GET.get("offset", 0))
        limit            = int(request.GET.get("limit", 10))

        THUMBNAIL = 2

        q = Q()
        page_title = "모든상품"

        if search:
            q &= Q(name__icontains=search)\
                | Q(category__sub__icontains=search)\
                | Q(category__main_category__main__icontains=search)\
                | Q(product_status__status__icontains=search)\
                | Q(caution__description__icontains=search)\
                | Q(sizestock__size__size__exact=search)
            page_title = search + "에 대한 검색결과"

        if main_category_id:
            q &= Q(category_id__main_category_id=main_category_id)
            page_title = Category.objects.filter(main_category_id=main_category_id).first().main_category.main

        if category_id:
            q &= Q(category_id__id=category_id)
            page_title = Category.objects.get(id=category_id).sub

        order = {
            "min_price"  : "discount_price",
            "max_price"  : "-discount_price",
            "high_rating": "-total_rating",
            "reviews"    : "-reviews",
            "best"       : "-best",
            "new"        : "-new",
        }

        products = Product.objects\
            .annotate(discount_price=(F("price") * (100 - F("discount"))) / 100)\
            .annotate(reviews=Count("review"))\
            .annotate(total_rating=Avg("review__rating"))\
            .annotate(best=Case(When(product_status__status="Best", then=True), default=False))\
            .annotate(new=Case(When(product_status__status="New", then=True), default=False))\
            .filter(q)\
            .order_by(order[order_condition])\
            [offset:offset+limit]

        results = [
            {
                "pageTitle": page_title
            },
            [
                {
                    "id"            : product.id,
                    "name"          : product.name,
                    "price"         : product.price,
                    "discount"      : product.discount,
                    "discount_price": product.discount_price,
                    "stock"         : sum([size_stock.stock.stock for size_stock in product.sizestock_set.filter()]),
                    "img"           : product.image_set.get(image_type_id=THUMBNAIL).image_urls if product.image_set.filter(image_type_id=THUMBNAIL) else None,
                    "reviewCount"   : product.reviews if product.reviews else None,
                    "reputation"    : round(product.total_rating, 1) if product.total_rating else None,
                    "descript"      : product.caution.description if product.caution else None,
                    "status"        : product.product_status.status if product.product_status else None
                } for product in products
            ]
        ]
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