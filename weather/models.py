from django.db import models

# Weather Data Models
#TODO Validate data on database level by setting min and max values

class UploadedDocument(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


#Every row belongs to the parent document. Upon deletion of UploadedDocument, all the rows are deleted as well.
class WeatherDataRow(models.Model):
    parent_file=models.ForeignKey(UploadedDocument, on_delete=models.CASCADE)
    date= models.DateField()
    min_temp=models.FloatField(default=0)
    max_temp=models.FloatField(default=0)
    mean_temp=models.FloatField(default=0)
    heat_degree_days=models.FloatField(default=0)
    total_rain=models.FloatField(default=0)
    total_snow=models.FloatField(default=0)
    speed_max_gusts=models.FloatField(default=0, blank=True)

    def __str__(self) -> str:
        return str(self.parent_file)