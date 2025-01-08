from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', '未対応'),
        ('in_progress', '対応中'),
        ('resolved', '対応済み'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    body = models.TextField()  # お問い合わせ内容を格納するフィールド
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name}: {self.body[:20]}..."  # contentをbodyに修正




