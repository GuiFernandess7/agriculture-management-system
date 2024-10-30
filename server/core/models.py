from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.db import models

class Field(models.Model):
    name = models.CharField(max_length=100)
    location = geo_models.PointField(null=True, blank=True)
    lon = models.FloatField()
    lat = models.FloatField()
    area = models.FloatField()
    soil_type = models.CharField(max_length=100)

    def apply_coordinates(self):
        """
        Converte as coordenadas de longitude e latitude em um objeto Point
        e atribui ao campo location.
        """
        if self.lon is not None and self.lat is not None:
            self.location = Point(self.lon, self.lat)
        else:
            self.location = None  # Ou trate conforme necessário

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que as coordenadas sejam aplicadas
        antes de salvar o modelo.
        """
        self.apply_coordinates()
        super(Field, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CropSeason(models.Model):
    crop_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.ForeignKey('Field', on_delete=models.CASCADE)
    estimated_yield = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def duration(self):
        """Calcula a duração da estação em dias."""
        return (self.end_date - self.start_date).days

    def __str__(self):
        return f"{self.crop_name} from {self.start_date} to {self.end_date}"

class Harvest(models.Model):
    crop_season = models.ForeignKey(CropSeason, on_delete=models.CASCADE, related_name='harvests')
    harvest_date = models.DateField()
    quantity = models.FloatField()
    quality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Harvest of {self.crop_season.crop_type} on {self.harvest_date}"