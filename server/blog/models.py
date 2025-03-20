from django.db import models
from django.utils.translation import gettext as _

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
    class STORAGES(models.TextChoices):
        disk = ("disk", _("disk"))
        s3 = ("s3", _("s3"))
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    storage = models.CharField(choices=STORAGES.choices, default=STORAGES.disk, max_length=10)
    tags = models.ManyToManyField(Tag, related_name="datasets", null=True)
    metadata = models.JSONField(null=True)

    def __str__(self):
        return self.name
    @property
    def images(self):
        return len(self.metadata.get('images',[]))
    @property
    def pdfs(self):
        return len(self.metadata.get('pdfs', []))
    @property
    def paragraphs(self):
        return len(self.metadata.get('paragraphs', []))
    @property
    def formulas(self):
        return len(self.metadata.get('formulas', []))