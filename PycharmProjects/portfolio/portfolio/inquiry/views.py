from django.shortcuts import render, get_object_or_404, redirect
from .models import Inquiry, Category
from .forms import InquiryForm, CategoryForm
from django.contrib import messages

# お問い合わせ一覧
def inquiry_list(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'inquiry/inquiry_list.html', {'inquiries': inquiries})

# お問い合わせ詳細
def inquiry_detail(request, id):
    inquiry = get_object_or_404(Inquiry, id=id)
    if request.method == 'POST':
        form = InquiryForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, "ステータスが更新されました。")
            return redirect('inquiry:inquiry_detail', id=id)
    else:
        form = InquiryForm(instance=inquiry)
    return render(request, 'inquiry/inquiry_detail.html', {'inquiry': inquiry, 'form': form})

# カテゴリ一覧
def category_list(request):
    categories = Category.objects.filter(is_deleted=False)
    return render(request, 'inquiry/category_list.html', {'categories': categories})

# カテゴリ追加
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "カテゴリーが追加されました。")
            return redirect('inquiry:category_list')
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = CategoryForm()
    return render(request, 'inquiry/category_add.html', {'form': form})

# カテゴリ編集
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "カテゴリーが更新されました。")
            return redirect('inquiry:category_list')
        else:
            messages.error(request, "入力にエラーがあります。")
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inquiry/category_edit.html', {'form': form})

# カテゴリ削除
def category_delete(request, id):
    category = get_object_or_404(Category, id=id, is_deleted=False)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "カテゴリーが削除されました。")
        return redirect('inquiry:category_list')
    
    return render(request, 'inquiry/category_list.html', {'category': category})

