from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Quote(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    content = models.TextField()

    def __str__(self):
        if len(self.content) < 100:
            return f'{self.content} ({self.author.name})'
        return f'{self.content[:100]}... ({self.author.name})'

    class Meta:
        ordering = ['content']
