from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

def validate_hiragana(value):
    if not re.fullmatch(r'^[\u3040-\u309Fー]+$', value):
        raise ValidationError('ふりがなはひらがなのみで入力してください。')

class AdminSettingsForm(forms.ModelForm):
    password = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="8~32文字の半角英数字と'_'、'-'のみ使用可能",
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise ValidationError("パスワードは8~32文字の半角英数字と'_'、'-'のみ使用可能です。")
        return password

class AccountForm(forms.ModelForm):
    account_type = forms.ChoiceField(
        choices=[('general', '一般'), ('admin', '管理者')],
        widget=forms.RadioSelect,
        required=True,
    )
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required':'名前を入力してください'}
    )
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'メールアドレスは必須です。',
            'invalid': '有効なメールアドレスを入力してください。',
        }
    )
    password = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="8~32文字の半角英数字と'_'、'-'のみ使用可能",
        error_messages={'required': 'パスワードは必須です。'}
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    furigana = forms.CharField(
        max_length=255,
        required=False,
        validators=[validate_hiragana],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'ふりがなはひらがなのみで入力してください。'},)
    
    gender = forms.ChoiceField(
        choices=[('male', '男性'), ('female', '女性')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_value=999,
        error_messages={
            'invalid': '年齢は数値で入力してください。',
            'max_value': '年齢は999以下にしてください。'
        }
    )
    bio = forms.CharField(
        max_length=1500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['name','email', 'password', 'furigana', 'gender', 'age', 'bio', 'profile_image']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.match(r'^[a-zA-Z0-9_-]{8,32}$', password):
            raise ValidationError("パスワードは8~32文字の半角英数字と'_'、'-'のみ使用可能です。")
        return password

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("画像サイズは2MB以内にしてください。")
        return image

def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')

        # 管理者の場合、特定フィールドのチェックを追加
        if account_type == 'admin':
            if not cleaned_data.get('password'):
                self.add_error('password', '管理者アカウントの場合、パスワードは必須です。')
        return cleaned_data