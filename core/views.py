from django.http     import JsonResponse
from django.views    import View

from products.models import MainCategory
from core.utils      import identification_decorator


class NavView(View):
    @identification_decorator
    def get(self, request):
        main_categories = MainCategory.objects.all()

        results = [
            [
                {
                    "userName": request.user.name if request.user else None
                }
            ],
            [
                {
                    "menuName": main_category.main,
                    "menuLink": main_category.id,
                    "sub": [
                        {
                            "subMenu"    : sub_category.sub,
                            "subMenuLink": sub_category.id
                        } for sub_category in main_category.category_set.all()
                    ]
                } for main_category in main_categories
            ]
        ]
        return JsonResponse({"results": results}, status=200)