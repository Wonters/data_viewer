from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to="files/")
    image = models.ImageField(upload_to="images/")
    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="items"
    )

    def __str__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    tags = models.ManyToManyField(Tag, related_name="datasets", null=True)

    def __str__(self):
        return self.name
