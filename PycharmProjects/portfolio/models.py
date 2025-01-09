from django.db import models
from django.utils.timezone import now

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)      # 更新日時
    deleted_at = models.DateTimeField(null=True, blank=True)  # 削除日時（論理削除用）

    def delete(self, using=None, keep_parents=False):
        """論理削除を実現するためのオーバーライド"""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """論理削除されたデータを復元"""
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True  # 抽象モデルとして設定
