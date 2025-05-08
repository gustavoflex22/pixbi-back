from rest_framework.serializers import ListField, Serializer, CharField, JSONField

from src.modules.forms.serializers.base_serializer import BaseModelSerializer, MyField
from src.modules.forms.serializers.enum_serializers import (
    NewOSCFormTargetAudienceSerializer,
    NewOSCFormRecessMonthSerializer,
    NewOSCFormAgeGroupMMSerializer,
    NewOSCFormMealTypeMMSerializer,
    NewOSCFormFoodDistributionSerializer,
    NewOSCFormEducationalUsageTypeSerializer,
    NewOSCFormOtherPartnerTypeSerializer,
    NewOSCFormOtherPartnerFrequencyRecevedSerializer,
    NewOSCFormDonationExtractionTransportTypeSerializer,
)
from src.modules.forms.models.pre_save_models import (
    PreSaveNewOSCFormModel,
    PreSaveNewOSCFormResponsableModel,
)
from src.modules.forms.models.models import (
    NewOSCFormModel,
    NewOSCFormResponsableModel,
    NewOSCFormTargetAudience,
    NewOSCFormRecessMonth,
    NewOSCFormMealTypeMM,
    NewOSCFormEducationalUsage,
    NewOSCFormEducationalUsageType,
    NewOSCFormOtherPartner,
    NewOSCFormOtherPartnerFoodType,
    NewOSCFormOtherPartnerType,
    NewOSCFormOtherPartnerFrequencyReceved,
    NewOSCFormDonationExtraction,
    NewOSCFormDonationExtractionTransportType,
)


class NewOSCFormResponsableSerializer(BaseModelSerializer):

    class Meta:
        model = NewOSCFormResponsableModel
        fields = "__all__"


class PreSaveNewOSCFormResponsableSerializer(BaseModelSerializer):

    class Meta:
        model = PreSaveNewOSCFormResponsableModel
        fields = "__all__"


class NewOSCFormDonationExtractionSerializer(BaseModelSerializer):

    type_of_transport = NewOSCFormDonationExtractionTransportTypeSerializer(required=False)
    type_of_transport_create = MyField(write_only=True)

    class Meta:
        model = NewOSCFormDonationExtraction
        fields = "__all__"

    def create(self, validated_data):
        type_of_transport_data = validated_data.pop("type_of_transport_create")

        instance = NewOSCFormDonationExtraction.objects.create(**validated_data)
        self.set_one_to_many_instances(instance, "type_of_transport", type_of_transport_data, NewOSCFormDonationExtractionTransportType, default=False)
        return instance


class NewOSCFormOtherPartnerSerializer(BaseModelSerializer):

    partner_type = NewOSCFormOtherPartnerTypeSerializer(required=False, many=True)
    partner_type_create = ListField(write_only=True)
    
    food_type = NewOSCFormOtherPartnerTypeSerializer(required=False, many=True)
    food_type_create = ListField(write_only=True)
    
    frequency_receved = NewOSCFormOtherPartnerFrequencyRecevedSerializer(required=False)
    frequency_receved_create = MyField(write_only=True)

    class Meta:
        model = NewOSCFormOtherPartner
        fields = "__all__"

    def create(self, validated_data):
        partner_type_data = validated_data.pop("partner_type_create")
        food_type_data = validated_data.pop("food_type_create")
        frequency_receved_data = validated_data.pop("frequency_receved_create")

        instance = NewOSCFormOtherPartner.objects.create(**validated_data)
        self.set_list_many_to_many_instances(instance, "partner_type", partner_type_data, NewOSCFormOtherPartnerType, default=False)
        self.set_list_many_to_many_instances(instance, "food_type", food_type_data, NewOSCFormOtherPartnerFoodType, default=False)
        self.set_one_to_many_instances(instance, "frequency_receved", frequency_receved_data, NewOSCFormOtherPartnerFrequencyReceved, default=False)
        return instance

class NewOSCFormEducationalUsageSerializer(BaseModelSerializer):

    educational_usage_type = NewOSCFormEducationalUsageTypeSerializer(required=False, many=True)
    educational_usage_type_create = ListField(write_only=True)

    class Meta:
        model = NewOSCFormEducationalUsage
        fields = "__all__"

    def create(self, validated_data):
        educational_usage_type_data = validated_data.pop("educational_usage_type_create")

        instance = NewOSCFormEducationalUsage.objects.create(**validated_data)
        self.set_list_many_to_many_instances(instance, "educational_usage_type", educational_usage_type_data, NewOSCFormEducationalUsageType, default=False)
        return instance



class CacheFormResponseSerializer(Serializer):

    user_id = CharField(max_length=255, required=False)
    # step = CharField(max_length=1)
    new_data = JSONField(required=False)


class PreSaveNewOSCFormSerializer(BaseModelSerializer):

    responsable = PreSaveNewOSCFormResponsableSerializer()

    class Meta:
        model = PreSaveNewOSCFormModel
        fields = "__all__"

    def create(self, validated_data):
        responsable_data = validated_data.pop("responsable", None)

        instance = PreSaveNewOSCFormModel.objects.create(**validated_data)
        PreSaveNewOSCFormResponsableModel.objects.create(pre_save=instance, **responsable_data)

        return instance
    
    def update(self, instance, validated_data):
        responsable_data = validated_data.pop("responsable", None)
        responsable_instance = instance.responsable

        for key in validated_data.keys():
            setattr(instance, key, validated_data.get(key, None))
        
        for key in responsable_data.keys():
            setattr(responsable_instance, key, responsable_data.get(key, None))
        
        instance.save()
        responsable_instance.save()
        return instance


class NewOSCFormSerializer(BaseModelSerializer):

    responsable = NewOSCFormResponsableSerializer()
    
    target_audience = NewOSCFormTargetAudienceSerializer(required=False, many=True)
    target_audience_create = ListField(write_only=True)
    
    recess_months = NewOSCFormRecessMonthSerializer(required=False, many=True)
    recess_months_create = ListField(required=False, write_only=True)

    age_group_mm =  NewOSCFormAgeGroupMMSerializer(required=False, many=True)
    meal_types_mm = NewOSCFormMealTypeMMSerializer(required=False, many=True)
    food_distribution_mm = NewOSCFormFoodDistributionSerializer(required=False, many=True)
    educational_usage = NewOSCFormEducationalUsageSerializer(required=False)
    other_parters = NewOSCFormOtherPartnerSerializer(required=False)
    
    donation_extraction = NewOSCFormDonationExtractionSerializer(required=False)

    class Meta:
        model = NewOSCFormModel
        fields = "__all__"

    def create(self, validated_data: dict):
        
        responsable_data = validated_data.pop("responsable", None)
        target_audience_list_data = validated_data.pop("target_audience_create", None)
        recess_months_list_data = validated_data.pop("recess_months_create", None)

        age_group_list_data = validated_data.pop("age_group_mm", None)
        meal_types_mm_list_data = validated_data.pop("meal_types_mm", None)
        food_distribution_data = validated_data.pop("food_distribution_mm", None)
        educational_usage_data = validated_data.pop("educational_usage", None)
        other_parters_data = validated_data.pop("other_parters", None)
        
        donation_extraction_data = validated_data.pop("donation_extraction", None)

        validated_data["user"] = self.context['request'].user
        instance = NewOSCFormModel.objects.create(**validated_data)
        NewOSCFormResponsableModel.objects.create(form_answer=instance, **responsable_data)
        
        self.save_many_to_many_instances(age_group_list_data, NewOSCFormAgeGroupMMSerializer, form_answer = instance.id)
        self.save_many_to_many_instances(food_distribution_data, NewOSCFormFoodDistributionSerializer, form_answer = instance.id)
        self.save_many_to_many_instances(meal_types_mm_list_data, NewOSCFormMealTypeMMSerializer, form_answer = instance.id)

        self.set_list_many_to_many_instances(instance, "target_audience", target_audience_list_data, NewOSCFormTargetAudience, default=False)
        self.set_list_many_to_many_instances(instance, "recess_months", recess_months_list_data, NewOSCFormRecessMonth)

        if educational_usage_data:
            educational_usage_data["form_answer"] = instance.id
            educational_usage_serializer = NewOSCFormEducationalUsageSerializer(data=educational_usage_data)
            educational_usage_serializer.is_valid(raise_exception=True)
            educational_usage_serializer.save()

        if other_parters_data:
            other_parters_data["form_answer"] = instance.id
            other_parters_serializer = NewOSCFormOtherPartnerSerializer(data=other_parters_data)
            other_parters_serializer.is_valid(raise_exception=True)
            other_parters_serializer.save()

        if donation_extraction_data:
            donation_extraction_data["form_answer"] = instance.id
            donation_extraction_serializer = NewOSCFormDonationExtractionSerializer(data=donation_extraction_data)
            donation_extraction_serializer.is_valid(raise_exception=True)
            donation_extraction_serializer.save()

        if meal_types_mm_list_data:
            for meal_type_mm_data in meal_types_mm_list_data:
                NewOSCFormMealTypeMM.objects.create(form_answer=instance, **meal_type_mm_data)

        return instance
