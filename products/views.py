import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Review

from core.utils      import login_decorator


class ReviewView(View):
    @login_decorator
    def post(self, reqeust):
        data = json.loads(reqeust.body)

        user_id    = reqeust.user
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
                "productSize"  : review.product.sizestock_set.get().size.size if review.product.sizestock_set.get().size else None,
                "reviewContent": review.comment,
                "reputation"   : review.rating,
                "reivewImg"    : [review_img.image_urls for review_img in review_imgs],
                "created_at"   : review.created_at,
                "updated_at"   : review.updated_at
            }
        ]
        return JsonResponse({"results": results}, status=200)

    @login_decorator
    def patch(self, request, review_id):
        data = json.loads(request.body)

        user_id = request.user

        existing_review = Review.objects.get(id=review_id, user_id=user_id)

        rating  = data.get("rating", existing_review.rating)
        comment = data.get("comment", existing_review.comment)

        existing_review.rating = rating
        existing_review.comment = comment
        existing_review.save()
        return JsonResponse({"message": "REVIEW_MODIFIED"}, status=205)

    @login_decorator
    def delete(self, request):
        review_ids = request.GET.getlist("review_ids")
        user_id    = request.user

        Review.objects.filter(id__in=review_ids, user_id=user_id).delete()
        return JsonResponse({'message': 'REVIEW_DELETED'}, status=204)