from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # usernameフィールドを無効化
    name = models.CharField(max_length=255, unique=True)  # nameを使用
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)  # 管理者フラグ
    bio = models.TextField(max_length=1500, blank=True, null=True)  # 自己紹介
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # プロフィール画像

    USERNAME_FIELD = "email"  # 認証に使用するフィールド
    REQUIRED_FIELDS = ["name"]  # スーパーユーザー作成時の必須フィールド

    objects = CustomUserManager()  # カスタムマネージャーを使用

    def __str__(self):
        return self.email
