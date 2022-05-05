from django.urls    import path

from products.views import ProductsListView, ProductDetailView, ReviewView

urlpatterns = [
    path('', ProductsListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/review/<int:review_id>', ReviewView.as_view())
]