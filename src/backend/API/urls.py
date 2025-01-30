from django.urls import path
from . import views
from .views import CheckTransactionStatus

app_name = 'API'

urlpatterns = [
    path('score', views.game_update, name='game_update'),
    path('scorehistory', views.GameHistoryView.as_view(), name='score_history_api'),
    path('check_transaction_status/<int:game_id>/', views.CheckTransactionStatus.as_view(), name='check_transaction_status'),
]