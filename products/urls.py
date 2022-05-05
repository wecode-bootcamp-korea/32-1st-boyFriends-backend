from django.urls    import path

from products.views import ProductDetailView, ReviewView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/review/<int:review_id>', ReviewView.as_view())
]