from django.urls    import path, include

from core.views     import MainCategoryView
from products.views import TopicView

urlpatterns = [
    path('navigation', MainCategoryView.as_view()),
    path('topic', TopicView.as_view()),
    path('users', include('users.urls')),
    path('products', include('products.urls')),
    path('payments', include('payments.urls')),
]