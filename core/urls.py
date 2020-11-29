from django.urls import path
from . import views
from .views import ActivateLanguageView


urlpatterns = [
    path('language/activate/<language_code>/', ActivateLanguageView.as_view(), name='activate_language'),
    path('',views.index,name = 'index'),
    path('how_work/',views.how_work,name = 'how-work'),
    path('offer/',views.offers,name = 'offers'),
    path('faq/',views.faq,name = 'faq'),
    path('orders/',views.orders,name = 'orders'),
    path('order/', views.order, name='order'),
    path('support/',views.support,name = 'support'),
    path('cart/', views.cart, name='cart'),
    path('get/',views.api,name='api'),
    path('add_to_cart/',views.add_cart,name='add_cart'),
    path('clear_cart/',views.clear_cart,name='clear_cart'),
    path('delete_itm/<int:id>/',views.clear_item,name='delete_itm'),
    path('edit_itm/<int:id>/',views.edit_item,name='edit_itm'),
    path('orders/com/',views.com,name='com'),
    path('orders/com_all/',views.com_all,name='com_all'),
    path('orders/clear/',views.clear_com,name='clear_com'),
    path('orders/clear/<int:id>',views.clear_item_com,name='clear_item_com'),
    path('edit_itm_com/<int:id>/',views.edit_item_com,name='edit_itm_com'),
    path('update/<str:username>',views.update,name='update'),
    path('subscribe/',views.subscribe,name='subscribe'),
    path('payment/',views.payments,name='payment')
]