from django.db import models
from localflavor.br.models import BRCNPJField, BRPostalCodeField

from src.modules.forms.enums import (
    PriorityCategoryEnum,
    DisponibilityCollectionEnum
)

class ABNewOSCFormModel(models.Model):
    razao_social = models.CharField(max_length=255)
    cnpj = BRCNPJField()
    organization_site = models.CharField(max_length=255, null=True, blank=True)
    social_midia = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    street_number = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    cep = BRPostalCodeField()
    priority_category = models.CharField(max_length=4, choices=PriorityCategoryEnum.choices)
    activities_detail = models.CharField(max_length=1000, null=False)
    quantity_workers = models.IntegerField(null=False)
    quantity_volunteers = models.IntegerField(null=False)
    quantity_people_served_monthly = models.IntegerField(null=False)
    people_benefited = models.IntegerField(null=False, default=0)
    has_registration_form = models.BooleanField(null=False, default=False)
    has_adequate_space = models.BooleanField()
    has_freezing_system = models.BooleanField()
    has_local_kitchen = models.BooleanField()
    has_refectory = models.BooleanField()
    serve_local_meals = models.BooleanField()
    has_nutritionist = models.BooleanField()
    disponibility_collection = models.CharField(max_length=6, choices=DisponibilityCollectionEnum.choices, default=DisponibilityCollectionEnum.ONEX)
    collection_restriction_detail = models.CharField(max_length=1000, null=True, blank=True)
    donation_destination = models.CharField(max_length=1000, null=True, blank=True)
    has_public_agreement = models.BooleanField()
    has_specific_agreement = models.BooleanField()
    has_updated_cnpj = models.BooleanField()
    has_updated_member_registration = models.BooleanField()
    has_updated_minute_inauguration_assembly = models.BooleanField()
    has_updated_health_permit = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True


class ABNewOSCFormResponsableModel(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    
    class Meta:
        abstract = True


class ABNewOSCFormTargetAudience(models.Model):
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    
    class Meta:
        abstract = True


class ABNewOSCFormRecessMonth(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        abstract = True


class ABNewOSCFormAgeGroup(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class ABNewOSCFormAgeGroupMM(models.Model):
    quantity_people_served_monthly = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class ABNewOSCFormMealType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class ABNewOSCFormMealTypeMM(models.Model):
    week_serves = models.IntegerField(null=True, blank=True)
    people_server_daily = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class ABNewOSCFormFoodDistributionType(models.Model):
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ABNewOSCFormFoodDistribution(models.Model):
    monthly_distribution = models.CharField(max_length=500)

    class Meta:
        abstract = True


class ABNewOSCFormEducationalUsage(models.Model):
    usage_details = models.CharField(max_length=1000)

    class Meta:
        abstract = True


class ABNewOSCFormEducationalUsageType(models.Model):
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ABNewOSCFormOtherPartner(models.Model):

    class Meta:
            abstract = True


class ABNewOSCFormOtherPartnerFoodType(models.Model):
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ABNewOSCFormOtherPartnerType(models.Model):
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ABNewOSCFormOtherPartnerFrequencyReceved(models.Model):
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ABNewOSCFormDonationExtraction(models.Model):
    vehicle_description = models.CharField(max_length=500)

    class Meta:
        abstract = True


class ABNewOSCFormDonationExtractionTransportType(models.Model):
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True