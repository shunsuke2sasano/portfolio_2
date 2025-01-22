from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import AdminSettingsForm, AccountForm
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GeneralUserProfile, Like
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q

User = get_user_model()

# 管理者専用アクセスのチェック
def admin_check(user):
    return user.is_staff or user.is_superuser

def login_view(request):
    """
    管理者と一般ユーザー共通のログインビュー
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # フォームが有効な場合、ユーザーを認証
            user = form.get_user()
            login(request, user)
            # ログイン後のリダイレクト先をユーザーのタイプで変更
            if user.is_staff or user.is_superuser:
                return redirect('dashboard:admin_dashboard')
            else:
                return redirect('dashboard:user_dashboard')
        else:
            # 認証失敗時にエラーメッセージを表示
            messages.error(request, "ログインに失敗しました。ユーザー名またはパスワードが正しくありません。")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
@user_passes_test(admin_check)  # 管理者のみアクセス許可
def admin_settings(request):
    """
    管理者設定画面
    """
    if request.method == 'POST':
        form = AdminSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "設定が更新されました。")
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = AdminSettingsForm(instance=request.user)

    return render(request, 'accounts/admin_settings.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def account_list(request):
    accounts = User.objects.filter(is_deleted=False)
    paginator = Paginator(accounts, 5)  # 1ページあたり5件
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/account_list.html', {'page_obj': page_obj})

@login_required
@user_passes_test(admin_check)
def account_delete(request, pk, permanent=False):
    """
    アカウント削除ビュー (論理削除):
    - 論理削除 (is_deleted=True)
    """
    account = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        if not account.is_deleted:
            account.is_deleted = True
            account.save()
            messages.success(request, "アカウントを削除しました。")
        else:
            messages.error(request, "このアカウントはすでに削除されています。")
        return redirect('accounts:account_list')

    return render(request, 'accounts/confirm_delete.html', {'account': account})

@login_required
@user_passes_test(admin_check)
def toggle_status(request, pk):
    print(f"Received toggle request for user ID: {pk}")  # デバッグログ
    if request.method == "POST":
        try:
            account = get_object_or_404(CustomUser, pk=pk)
            account.is_active = not account.is_active
            account.save()
            return JsonResponse({
                "success": True,
                "is_active": account.is_active,
                "message": f"アカウントが{'有効化' if account.is_active else '無効化'}されました。",
            })
        except Exception as e:
            print(f"Error: {e}")  # エラー確認ログ
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "無効なリクエストです。"}, status=400)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            account_type = form.cleaned_data.get('account_type')
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('name')  # name フィールドを username に設定
            if account_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "アカウントが作成されました。")
            return redirect('accounts:account_list')
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = AccountForm()

    return render(request, 'accounts/account_create.html', {'form': form})


@login_required
@user_passes_test(admin_check)
def account_delete_list(request):
    deleted_accounts = User.objects.filter(is_deleted=True)  # 論理削除されたアカウント
    return render(request, 'accounts/account_delete_list.html', {'accounts': deleted_accounts})

@login_required
@user_passes_test(admin_check)
def account_delete_permanently(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        user.delete()  # 完全削除
        messages.success(request, "アカウントを完全に削除しました。")
        return redirect('accounts:account_delete_list')
    return redirect('accounts:account_delete_list') 

@login_required
@user_passes_test(admin_check)
def account_restore(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_deleted = False  # 復元
        user.save()
        messages.success(request, "アカウントを復元しました。")
        return redirect('accounts:account_delete_list')
    
@login_required
def general_account_list(request):
    profiles = GeneralUserProfile.objects.all()
    return render(request, 'accounts/general_account_list.html', {'profiles': profiles})

def like_toggle(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

        # POSTデータの取得
        user_id = request.POST.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User ID is required'}, status=400)

        # GeneralUserProfile の取得
        liked_user = get_object_or_404(GeneralUserProfile, user_id=user_id)

        # Like のトグル処理
        like, created = Like.objects.get_or_create(user=request.user, liked_user=liked_user.user)
        if created:
            liked_user.likes_count += 1
        else:
            like.delete()
            liked_user.likes_count -= 1

        liked_user.save()

        # 成功レスポンス
        return JsonResponse({'success': True, 'likes_count': liked_user.likes_count})
    except Exception as e:
        # エラーが発生した場合のログとレスポンス
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in like_toggle: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def monthly_like_ranking(request):
    current_month = now().month

    # 修正後のクエリ
    profiles = GeneralUserProfile.objects.filter(
        user__liked_user__created_at__month=current_month
    ).annotate(total_likes=Count('user__liked_user')).order_by('-total_likes')[:10]

    return render(request, 'accounts/monthly_like_ranking.html', {'profiles': profiles})

def general_account_detail(request, user_id):
    profile = get_object_or_404(GeneralUserProfile, user_id=user_id)
    return render(request, 'accounts/general_account_detail.html', {'profile': profile})