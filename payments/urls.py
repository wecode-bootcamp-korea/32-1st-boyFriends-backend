from django.urls    import path

from payments.views import (
                        CartView,
                        CartCountView,
                        CartCheckBoxView
                    )

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/cart/count', CartCountView.as_view()),
    path('/cart/check', CartCheckBoxView.as_view())
]