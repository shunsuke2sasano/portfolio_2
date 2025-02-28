from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
import re
from django.contrib.auth.models import User

class EmailUpdateForm(forms.Form):
    email = forms.EmailField(
        label="新しいメールアドレス",
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '新しいメールアドレスを入力してください'}),
        required=True
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) > 255:
            raise forms.ValidationError("メールアドレスは255文字以下である必要があります。")
        return email


class PasswordUpdateForm(forms.Form):
    password = forms.CharField(
        label="新しいパスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '新しいパスワードを入力してください'}),
        required=True
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # パスワードのバリデーション: 8~32文字、半角英数字と _ - のみ許可
        if not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise forms.ValidationError("パスワードは8〜32文字の半角英数字と「_」「-」のみ使用できます。")
        return password


User = get_user_model()  # カスタムユーザーモデルを取得

class UserProfileEditForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="プロフィール画像",  # ラベルを設定
        help_text="画像サイズは2MB以内でアップロードしてください。"
    )
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="名前",  # ラベルを設定
        error_messages={'required': '名前を入力してください。'}
    )
    furigana = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="ふりがな",  # ラベルを設定
        error_messages={'invalid': 'ふりがなはひらがなのみで入力してください。'},
    )
    gender = forms.ChoiceField(
        choices=[('male', '男性'), ('female', '女性')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label="性別"  # ラベルを設定
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        label="年齢",  # ラベルを設定
        error_messages={
            'invalid': '年齢は数値で入力してください。',
            'max_value': '年齢は999以下にしてください。',
        }
    )
    bio = forms.CharField(
        max_length=1500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="自己紹介"  # ラベルを設定
    )

    class Meta:
        model = User
        fields = ['name', 'profile_image', 'furigana', 'gender', 'age', 'bio']

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("画像サイズは2MB以内にしてください。")
        return image

    def clean(self):
        cleaned_data = super().clean()
        # 必要に応じて追加のカスタム検証ロジックを記述
        return cleaned_data

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']