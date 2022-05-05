from django.urls    import path

from payments.views import CartView

urlpatterns = [
    path('/cart', CartView.as_view())
]