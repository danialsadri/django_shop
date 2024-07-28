import hashlib
from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="images/", width_field="width", height_field="height")
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)
    file_hash = models.CharField(max_length=40, db_index=True, editable=False)
    file_size = models.PositiveIntegerField(blank=True, null=True, editable=False)
    focal_point_x = models.PositiveIntegerField(blank=True, null=True)
    focal_point_y = models.PositiveIntegerField(blank=True, null=True)
    focal_point_width = models.PositiveIntegerField(blank=True, null=True)
    focal_point_height = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.image.file.closed:
            self.file_size = self.image.size
            hasher = hashlib.sha1()
            for chunk in self.image.file.chunks():
                hasher.update(chunk)
            self.file_hash = hasher.hexdigest()
        super().save(*args, **kwargs)
