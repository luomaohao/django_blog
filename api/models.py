from django.db import models

# Create your models here.
class todo(models.Model):
    """
    创建的todolist 模型
    """
    title = models.CharField(max_length=256)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

