from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    # path('', cache_page(60)(BaseNews.as_view()), name='home'),
    path('', BaseNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('test/', test, name='test'),
    path('signup/', signup, name='signup'),
    path('signin/', user_login, name='signin'),
    path('signout/', signout, name='signout'),
    path('contact/', contact, name='contact'),
]