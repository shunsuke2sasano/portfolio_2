from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),              # ログイン画面
    path('admin/settings/', views.admin_settings, name='admin_settings'),  # 管理者設定画面
    path('account_list/', views.account_list, name='account_list'),  # アカウント一覧
    path('account_create/', views.account_create, name='account_create'),  # アカウント作成
    path('account_delete_list/', views.account_delete_list, name='account_delete_list'),  # 削除済みアカウント一覧
    path('account_delete/<int:pk>/', views.account_delete, name='account_delete'),  # ソフトデリート
    path('account_restore/<int:pk>/', views.account_restore, name='account_restore'),  # アカウント復旧
    path('delete/permanent/<int:pk>/', views.account_delete_permanently, name='account_permanent_delete'),  # 完全削除
    path('toggle_status/<int:pk>/', views.toggle_status, name='toggle_status'),  # ステータス切り替え
    path('general_accounts/', views.general_account_list, name='general_account_list'), #一般
    path('general_accounts/<int:user_id>/', views.general_account_detail, name='general_account_detail'), #アカウント詳細
    path('like_toggle/', views.like_toggle, name='like_toggle'), #
    path('monthly_ranking/', views.monthly_like_ranking, name='monthly_like_ranking'), #月のいいねランキング

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

