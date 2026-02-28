from django.urls import path
from .views import quiz_view, register_view, results_history_view, login_view, logout_view

urlpatterns = [
    path('', quiz_view, name='quiz'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('results/', results_history_view, name='results'),
]