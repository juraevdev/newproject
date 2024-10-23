from django.urls import path
from accounts.views import RegisterAPIView, RegisterVerifyAPIView, ResendVerifyCodeAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('register/verify/', RegisterVerifyAPIView.as_view()),
    path('register/resend-code/', ResendVerifyCodeAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]