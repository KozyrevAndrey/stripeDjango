from django.urls import path

from .views import (
    CreateCheckoutSession,
    ProductLandingPageView,
    ArticleDetailView,
    SuccessView,
    CancelView
)

urlpatterns = [
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('buy/<pk>/', CreateCheckoutSession.as_view(), name='buy'),
    path('', ProductLandingPageView.as_view(), name='landing'),
    path('item/<pk>/', ArticleDetailView.as_view(), name='detail')

]