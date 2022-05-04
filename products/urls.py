from django.urls    import path

from products.views import ReviewView

urlpatterns = [
    path('/review/<int:review_id>', ReviewView.as_view())
]