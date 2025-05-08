from django.db import models
from localflavor.br.models import BRCNPJField, BRPostalCodeField

from src.modules.forms.enums import PriorityCategoryEnum, DisponibilityCollectionEnum
from src.modules.forms.models.abstract_models import (
    ABNewOSCFormModel,
    ABNewOSCFormResponsableModel,
    ABNewOSCFormTargetAudience,
    ABNewOSCFormRecessMonth,
    ABNewOSCFormTargetAudience,
    ABNewOSCFormRecessMonth,
    ABNewOSCFormAgeGroup,
    ABNewOSCFormAgeGroupMM,
    ABNewOSCFormMealType,
    ABNewOSCFormMealTypeMM,
    ABNewOSCFormFoodDistributionType,
    ABNewOSCFormFoodDistribution,
    ABNewOSCFormEducationalUsage,
    ABNewOSCFormEducationalUsageType,
    ABNewOSCFormOtherPartner,
    ABNewOSCFormOtherPartnerFoodType,
    ABNewOSCFormOtherPartnerType,
    ABNewOSCFormOtherPartnerFrequencyReceved,
    ABNewOSCFormDonationExtraction,
    ABNewOSCFormDonationExtractionTransportType,
)


class PreSaveNewOSCFormModel(ABNewOSCFormModel):
    razao_social = models.CharField(max_length=255, null=True, blank=True)
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
    priority_category = models.CharField(max_length=4, choices=PriorityCategoryEnum.choices, null=True)
    activities_detail = models.CharField(max_length=1000, null=True)
    quantity_workers = models.IntegerField(null=True)
    quantity_volunteers = models.IntegerField(null=True)
    quantity_people_served_monthly = models.IntegerField(null=True)
    people_benefited = models.IntegerField(null=True, default=0)
    has_registration_form = models.BooleanField(null=True, default=False)
    has_adequate_space = models.BooleanField(null=True)
    has_freezing_system = models.BooleanField(null=True)
    has_local_kitchen = models.BooleanField(null=True)
    has_refectory = models.BooleanField(null=True)
    serve_local_meals = models.BooleanField(null=True)
    has_nutritionist = models.BooleanField(null=True)
    disponibility_collection = models.CharField(max_length=6, choices=DisponibilityCollectionEnum.choices, null=True)
    collection_restriction_detail = models.CharField(max_length=1000, null=True, blank=True)
    donation_destination = models.CharField(max_length=1000, null=True, blank=True)
    has_public_agreement = models.BooleanField(null=True)
    has_specific_agreement = models.BooleanField(null=True)
    has_updated_cnpj = models.BooleanField(null=True)
    has_updated_member_registration = models.BooleanField(null=True)
    has_updated_minute_inauguration_assembly = models.BooleanField(null=True)
    has_updated_health_permit = models.BooleanField(null=True)
    created_at = models.DateField(auto_now_add=True)


class PreSaveNewOSCFormResponsableModel(ABNewOSCFormResponsableModel):
    name = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    pre_save = models.OneToOneField(PreSaveNewOSCFormModel, models.CASCADE, null=True, blank=True, related_name="responsable")


class PreSaveNewOSCFormTargetAudience(ABNewOSCFormTargetAudience):
    name = models.CharField(max_length=255, null=True)
    default = models.BooleanField(default=False)
    form_answer = models.ManyToManyField(PreSaveNewOSCFormModel, related_name="target_audience")


class PreSaveNewOSCFormRecessMonth(ABNewOSCFormRecessMonth):
    name = models.CharField(max_length=255, null=True)
    form_answer = models.ManyToManyField(PreSaveNewOSCFormModel, related_name="recess_months")


class PreSaveNewOSCFormAgeGroup(ABNewOSCFormAgeGroup):
    name = models.CharField(max_length=255, null=True)
    form_answer = models.ManyToManyField(PreSaveNewOSCFormModel, through='PreSaveNewOSCFormAgeGroupMM', related_name="age_group")


class PreSaveNewOSCFormAgeGroupMM(ABNewOSCFormAgeGroupMM):
    age_group = models.ForeignKey(PreSaveNewOSCFormAgeGroup, on_delete=models.CASCADE, related_name="age_group_mm")
    form_answer = models.ForeignKey(PreSaveNewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="age_group_mm")


class PreSaveNewOSCFormMealType(ABNewOSCFormMealType):
    name = models.CharField(max_length=255, null=True)
    form_answer = models.ManyToManyField(PreSaveNewOSCFormModel, through='PreSaveNewOSCFormMealTypeMM', related_name="meal_types")


class PreSaveNewOSCFormMealTypeMM(ABNewOSCFormMealTypeMM):
    meal_type = models.ForeignKey(PreSaveNewOSCFormMealType, on_delete=models.CASCADE, related_name="meal_types_mm")
    form_answer = models.ForeignKey(PreSaveNewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="meal_types_mm")


class PreSaveNewOSCFormFoodDistributionType(ABNewOSCFormFoodDistributionType):
    name = models.CharField(max_length=255, null=True)
    form_answer = models.ManyToManyField(PreSaveNewOSCFormModel, through='PreSaveNewOSCFormFoodDistribution', related_name="distribution_type")


class PreSaveNewOSCFormFoodDistribution(ABNewOSCFormFoodDistribution):
    monthly_distribution = models.CharField(max_length=500, null=True)
    distribution_type = models.ForeignKey(PreSaveNewOSCFormFoodDistributionType, on_delete=models.CASCADE, null=True, related_name="food_distribution_mm")
    form_answer = models.ForeignKey(PreSaveNewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="food_distribution_mm")


class PreSaveNewOSCFormEducationalUsage(ABNewOSCFormEducationalUsage):
    usage_details = models.CharField(max_length=1000, null=True)
    form_answer = models.OneToOneField(PreSaveNewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="educational_usage")


class PreSaveNewOSCFormEducationalUsageType(ABNewOSCFormEducationalUsageType):
    name = models.CharField(max_length=255, null=True)
    educational_usage = models.ManyToManyField(PreSaveNewOSCFormEducationalUsage, related_name="educational_usage_type")


class PreSaveNewOSCFormOtherPartner(ABNewOSCFormOtherPartner):
    form_answer = models.OneToOneField(PreSaveNewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="other_parters")
    frequency_receved = models.ForeignKey('PreSaveNewOSCFormOtherPartnerFrequencyReceved', on_delete=models.CASCADE, null=True, blank=True, related_name="other_parters")


class PreSaveNewOSCFormOtherPartnerFoodType(ABNewOSCFormOtherPartnerFoodType):
    name = models.CharField(max_length=255, null=True)
    food_distribution = models.ManyToManyField(PreSaveNewOSCFormOtherPartner, related_name="food_type")


class PreSaveNewOSCFormOtherPartnerType(ABNewOSCFormOtherPartnerType):
    name = models.CharField(max_length=255, null=True)
    food_distribution = models.ManyToManyField(PreSaveNewOSCFormOtherPartner, related_name="partner_type")


class PreSaveNewOSCFormOtherPartnerFrequencyReceved(ABNewOSCFormOtherPartnerFrequencyReceved):
    name = models.CharField(max_length=255, null=True)


class PreSaveNewOSCFormDonationExtraction(ABNewOSCFormDonationExtraction):
    vehicle_description = models.CharField(max_length=500, null=True)
    form_answer = models.OneToOneField(PreSaveNewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="donation_extraction")
    type_of_transport = models.ForeignKey('PreSaveNewOSCFormDonationExtractionTransportType', on_delete=models.CASCADE, null=True, blank=True, related_name="transport_type")


class PreSaveNewOSCFormDonationExtractionTransportType(ABNewOSCFormDonationExtractionTransportType):
    name = models.CharField(max_length=255, null=True)
