from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from portfolio.portfolio.models import TimestampedModel

class UserProfile(TimestampedModel):
    # 必要なフィールドを定義
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

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


class CustomUser(AbstractUser, TimestampedModel):
    username = None  # usernameフィールドを無効化
    name = models.CharField(max_length=255, unique=True)  # nameを使用
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)  # 管理者フラグ
    bio = models.TextField(max_length=1500, blank=True, null=True)  # 自己紹介
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # プロフィール画像
    is_deleted =  models.BooleanField(default=False)  # 論理削除用フラグ

    USERNAME_FIELD = "email"  # 認証に使用するフィールド
    REQUIRED_FIELDS = ["name"]  # スーパーユーザー作成時の必須フィールド

    objects = CustomUserManager()  # カスタムマネージャーを使用

    def __str__(self):
        return self.email

    def delete(self, using=None, keep_parents=False):
        """論理削除を実現するためのオーバーライドメソッド"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """論理削除されたデータの復元"""
        self.is_deleted = False
        self.save()

    class Meta:
        ordering = ['-created_at']  # デフォルトの並び順
        
class Like(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_user'
    )
    class Meta:
        unique_together = ('user', 'liked_user')

class GeneralUserProfile(TimestampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', '男性'), ('female', '女性'), ('other', 'その他')])
    likes_count = models.PositiveIntegerField(default=0)  # ランキング用