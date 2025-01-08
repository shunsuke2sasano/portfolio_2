from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('dashboard:user_dashboard')
    return render(request, 'dashboard/admin_dashboard.html')

@login_required
def user_dashboard(request):
    if request.user.is_admin:
        return redirect('dashboard:admin_dashboard')
    return render(request, 'dashboard/user_dashboard.html')
