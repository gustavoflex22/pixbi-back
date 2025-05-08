from django.db import models
from django.contrib.auth import get_user_model

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


class NewOSCFormModel(ABNewOSCFormModel):
    pre_save = models.OneToOneField("forms.PreSaveNewOSCFormModel", models.CASCADE, null=True, blank=True, related_name="form_answer")
    user = models.ForeignKey(get_user_model(), models.CASCADE, null=True, blank=True, related_name="form_answer")


class NewOSCFormResponsableModel(ABNewOSCFormResponsableModel):
    form_answer = models.OneToOneField(NewOSCFormModel, models.CASCADE, null=True, blank=True, related_name="responsable")


class NewOSCFormTargetAudience(ABNewOSCFormTargetAudience):
    form_answer = models.ManyToManyField(NewOSCFormModel, related_name="target_audience")


class NewOSCFormRecessMonth(ABNewOSCFormRecessMonth):
    form_answer = models.ManyToManyField(NewOSCFormModel, related_name="recess_months")


class NewOSCFormAgeGroup(ABNewOSCFormAgeGroup):
    form_answer = models.ManyToManyField(NewOSCFormModel, through='NewOSCFormAgeGroupMM', related_name="age_group")


class NewOSCFormAgeGroupMM(ABNewOSCFormAgeGroupMM):
    age_group = models.ForeignKey(NewOSCFormAgeGroup, on_delete=models.CASCADE, related_name="age_group_mm")
    form_answer = models.ForeignKey(NewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="age_group_mm")


class NewOSCFormMealType(ABNewOSCFormMealType):
    form_answer = models.ManyToManyField(NewOSCFormModel, through='NewOSCFormMealTypeMM', related_name="meal_types")


class NewOSCFormMealTypeMM(ABNewOSCFormMealTypeMM):
    meal_type = models.ForeignKey(NewOSCFormMealType, on_delete=models.CASCADE, related_name="meal_types_mm")
    form_answer = models.ForeignKey(NewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="meal_types_mm")


class NewOSCFormFoodDistributionType(ABNewOSCFormFoodDistributionType):
    form_answer = models.ManyToManyField(NewOSCFormModel, through='NewOSCFormFoodDistribution', related_name="distribution_type")


class NewOSCFormFoodDistribution(ABNewOSCFormFoodDistribution):
    distribution_type = models.ForeignKey(NewOSCFormFoodDistributionType, on_delete=models.CASCADE, null=True, related_name="food_distribution_mm")
    form_answer = models.ForeignKey(NewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="food_distribution_mm")


class NewOSCFormEducationalUsage(ABNewOSCFormEducationalUsage):
    form_answer = models.OneToOneField(NewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="educational_usage")


class NewOSCFormEducationalUsageType(ABNewOSCFormEducationalUsageType):
    educational_usage = models.ManyToManyField(NewOSCFormEducationalUsage, related_name="educational_usage_type")


class NewOSCFormOtherPartner(ABNewOSCFormOtherPartner):
    form_answer = models.OneToOneField(NewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="other_parters")
    frequency_receved = models.ForeignKey('NewOSCFormOtherPartnerFrequencyReceved', on_delete=models.CASCADE, null=True, blank=True, related_name="other_parters")


class NewOSCFormOtherPartnerFoodType(ABNewOSCFormOtherPartnerFoodType):
    food_distribution = models.ManyToManyField(NewOSCFormOtherPartner, related_name="food_type")


class NewOSCFormOtherPartnerType(ABNewOSCFormOtherPartnerType):
    food_distribution = models.ManyToManyField(NewOSCFormOtherPartner, related_name="partner_type")


class NewOSCFormOtherPartnerFrequencyReceved(ABNewOSCFormOtherPartnerFrequencyReceved): ...


class NewOSCFormDonationExtraction(ABNewOSCFormDonationExtraction):
    form_answer = models.OneToOneField(NewOSCFormModel, on_delete=models.CASCADE, null=True, blank=True, related_name="donation_extraction")
    type_of_transport = models.ForeignKey('NewOSCFormDonationExtractionTransportType', on_delete=models.CASCADE, null=True, blank=True, related_name="transport_type")

class NewOSCFormDonationExtractionTransportType(ABNewOSCFormDonationExtractionTransportType): ...