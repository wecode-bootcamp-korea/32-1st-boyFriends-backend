from django.http      import JsonResponse
from django.views     import View
from django.db.models import (
                          Q,
                          F,
                          Case,
                          When,
                          Avg,
                          Count
                      )

from products.models  import Product, SizeStock, Category


class ProductsListView(View):
    def get(self, request):
        category_id      = request.GET.get("category_id", None)
        main_category_id = request.GET.get("main_category_id", None)
        order_condition  = request.GET.get("order", "high_rating")
        search           = request.GET.get("search", None)
        offset           = int(request.GET.get("offset", 0))
        limit            = int(request.GET.get("limit", 10))

        THUMBNAIL = 2

        size_stock = SizeStock.objects

        q = Q()

        if search:
            q &= Q(name__icontains=search)

        if main_category_id:
            q &= Q(category_id__main_category_id=main_category_id)

        if category_id:
            q &= Q(category_id__id=category_id)

        order = {
            "min_price": "discount_price",
            "max_price": "-discount_price",
            "high_rating": "-review__rating",
            "reviews": "-reviews",
            "best": "-best",
            "new": "-new"
        }

        products = Product.objects.annotate(discount_price=Case(When(discount=True, then=F("price") * (100 - F("discount") / 100)), default=F("price")))\
            .annotate(reviews=Count("review"))\
            .annotate(best=Case(When(product_status__status="Best", then=True), default=False))\
            .annotate(new=Case(When(product_status__status="New", then=True), default=False)) \
            .filter(q).order_by(order[order_condition])[offset:limit]

        results = [
            {
                "id"            : product.id,
                "name"          : product.name,
                "price"         : product.price,
                "discount"      : product.discount,
                "discount_price": ((product.price) * (100 - (product.discount))) // 100 if product.discount else product.price,
                "stock"         : size_stock.get(id=product.id).stock.stock,
                "is_soldout"    : "is_soldout" if size_stock.get(id=product.id).stock.stock == 0 else "on_stock",
                "img"           : product.image_set.get(image_type_id=THUMBNAIL).image_urls if product.image_set.filter(image_type_id=THUMBNAIL) else None,
                "reviewCount"   : product.review_set.aggregate(Count('id'))["id__count"] if product.review_set.exists() else None,
                "reputation"    : product.review_set.aggregate(Avg("rating"))["rating__avg"] if product.review_set.exists() else None,
                "descript"      : product.caution.description if product.caution else None,
                "status"        : product.product_status.status if product.product_status else None
            } for product in products
        ]

        return JsonResponse({"results": results}, status=200)