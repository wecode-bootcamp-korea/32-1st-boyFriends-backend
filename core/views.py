from django.http     import JsonResponse
from django.views    import View

from products.models import MainCategory

class NavView(View):
    def get(self, request):
        main_categories = MainCategory.objects.all()

        results = [
            {
                "menuName"   : main_category.main,
                "menuLink"   : main_category.id,
                "sub" : [
                    {
                        "subMenu": main_category.category_set.all()[i].sub,
                        "subMenuLink": main_category.category_set.all()[i].id
                    } for i in range(len(main_category.category_set.all()))
                ]
            } for main_category in main_categories
        ]
        return JsonResponse({"results": results}, status=200)
