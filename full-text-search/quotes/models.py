from django.db import models


class Author(models.Model):
    name_en = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_en


class Quote(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    content = models.TextField()
    lang = models.CharField(max_length=2, choices=[('en', 'en'), ('ru', 'ru')])

    def __str__(self):
        if len(self.content) < 100:
            return f'{self.content} ({self.author})'
        return f'{self.content[:100]}... ({self.author})'

    class Meta:
        ordering = ['content']
