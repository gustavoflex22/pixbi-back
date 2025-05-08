from rest_framework.serializers import (
    ModelSerializer
)

from src.modules.forms.serializers.base_serializer import BaseModelSerializer, MyField

from src.modules.forms.models.models import (
    NewOSCFormTargetAudience,
    NewOSCFormRecessMonth,
    NewOSCFormAgeGroup,
    NewOSCFormMealType,
    NewOSCFormMealTypeMM,
    NewOSCFormFoodDistribution,
    NewOSCFormFoodDistributionType,
    NewOSCFormEducationalUsageType,
    NewOSCFormOtherPartnerFoodType,
    NewOSCFormOtherPartnerType,
    NewOSCFormOtherPartnerFrequencyReceved,
    NewOSCFormAgeGroupMM,
    NewOSCFormDonationExtractionTransportType,
)


class NewOSCFormTargetAudienceSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormTargetAudience
        fields = "__all__"

class NewOSCFormRecessMonthSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormRecessMonth
        fields = "__all__"

class NewOSCFormAgeGroupMMSerializer(ModelSerializer):

    class Meta:
        model = NewOSCFormAgeGroupMM
        fields = "__all__"

class NewOSCFormAgeGroupSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormAgeGroup
        fields = "__all__"

    def create(self, validated_data):
        age_group_mm = validated_data.pop("age_group_mm")
        
        instance = NewOSCFormAgeGroup.objects.create(**validated_data)
        instance.age_group_mm.set(age_group_mm)
        

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["age_group_mm"] = NewOSCFormAgeGroupMMSerializer(instance.age_group_mm.all(), many=True).data
        return representation

class NewOSCFormMealTypeMMSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormMealTypeMM
        fields = "__all__"

class NewOSCFormMealTypeSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormMealType
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["meal_types_mm"] = NewOSCFormMealTypeMMSerializer(instance.meal_types_mm.all(), many=True).data
        return representation

class NewOSCFormFoodDistributionSerializer(BaseModelSerializer):

    distribution_type_create = MyField(write_only=True)

    class Meta:
        model = NewOSCFormFoodDistribution
        fields = "__all__"
    
    def create(self, validated_data):
        distribution_type_data = validated_data.pop("distribution_type_create")

        instance = NewOSCFormFoodDistribution.objects.create(**validated_data)
        self.set_one_to_many_instances(instance, "distribution_type", distribution_type_data, NewOSCFormFoodDistributionType, default=False)
        return instance

class NewOSCFormFoodDistributionTypeSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormFoodDistributionType
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["food_distribution_mm"] = NewOSCFormFoodDistributionSerializer(instance.food_distribution_mm.all(), many=True).data
        return representation

class NewOSCFormEducationalUsageTypeSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormEducationalUsageType
        fields = "__all__"

class NewOSCFormOtherPartnerFoodTypeSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormOtherPartnerFoodType
        fields = "__all__"

class NewOSCFormOtherPartnerTypeSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormOtherPartnerType
        fields = "__all__"

class NewOSCFormOtherPartnerFrequencyRecevedSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormOtherPartnerFrequencyReceved
        fields = "__all__"

class NewOSCFormDonationExtractionTransportTypeSerializer(ModelSerializer):
    
    class Meta:
        model = NewOSCFormDonationExtractionTransportType
        fields = "__all__"