from django.db import models


# Create your models here.
class Farmer(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    village_name = models.CharField(max_length=50, blank=True, null=True)
    district_name = models.CharField(max_length=50, blank=True, null=True)
    state_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    def get_phone_number(self):
        return self.phone_number

    def __str__(self):
        return f"{self.name}"


class HindiFarmerDetails(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    farmer = models.ForeignKey(Farmer, default=None, related_name="hi", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    village_name = models.CharField(max_length=50, blank=True, null=True)
    district_name = models.CharField(max_length=50, blank=True, null=True)
    state_name = models.CharField(max_length=50, blank=True, null=True)

    def get_phone_number(self):
        return self.farmer.phone_number

    def __str__(self):
        return f"{self.farmer.name}_hindi_{self.name}"


class MarathiFarmerDetails(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    farmer = models.ForeignKey(Farmer, default=None, related_name="ma", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    village_name = models.CharField(max_length=50, blank=True, null=True)
    district_name = models.CharField(max_length=50, blank=True, null=True)
    state_name = models.CharField(max_length=50, blank=True, null=True)

    def get_phone_number(self):
        return self.farmer.phone_number

    def __str__(self):
        return f"{self.farmer.name}_Marathi_{self.name}"


class TeleguFarmerDetails(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    farmer = models.ForeignKey(Farmer, default=None, related_name="te", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    village_name = models.CharField(max_length=50, blank=True, null=True)
    district_name = models.CharField(max_length=50, blank=True, null=True)
    state_name = models.CharField(max_length=50, blank=True, null=True)

    def get_phone_number(self):
        return self.farmer.phone_number

    def __str__(self):
        return f"{self.farmer.name}_telegu_{self.name}"


class PunjabiFarmerDetail(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    farmer = models.ForeignKey(Farmer, default=None, related_name="pu", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    village_name = models.CharField(max_length=50, blank=True, null=True)
    district_name = models.CharField(max_length=50, blank=True, null=True)
    state_name = models.CharField(max_length=50, blank=True, null=True)

    def get_phone_number(self):
        return self.farmer.phone_number

    def __str__(self):
        return f"{self.farmer.name}_punjabi_{self.name}"
