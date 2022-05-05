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

from products.models  import Product, Category


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
            q &= Q(name__icontains=search)
            page_title = "검색결과"

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
            "new"        : "-new"
        }

        products = Product.objects\
            .annotate(discount_price=(F("price") * ((100 - F("discount") / 100))))\
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
                    "discount_price": ((product.price) * (100 - (product.discount))) // 100,
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