from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from portfolio.users.forms import EditProfileForm, UserSettingsForm

@login_required
def admin_dashboard(request):
    # 必要なデータを取得
    monthly_profiles = []
    yearly_profiles = []
    return render(request, 'dashboard/admin_dashboard.html', {
        'monthly_profiles': monthly_profiles,
        'yearly_profiles': yearly_profiles,
    })

@login_required
def user_dashboard(request):
    if request.user.is_admin:
        return redirect('dashboard:admin_dashboard')
    return render(request, 'dashboard/user_dashboard.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard:users_dashboard')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'dashboard/edit_profile.html', {'form': form})

@login_required
def users_settings(request):
    if request.method == 'POST':
        email_form = UserSettingsForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
            return redirect('dashboard:users_dashboard')
    else:
        email_form = UserSettingsForm(instance=request.user)

    return render(request, 'dashboard/users_settings.html', {'email_form': email_form})