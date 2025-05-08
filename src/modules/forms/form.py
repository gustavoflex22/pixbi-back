from django.forms import (
    ModelForm,
    TextInput,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple   
)

from src.modules.forms.models.models import (
    NewOSCFormModel,
    NewOSCFormTargetAudience,
    NewOSCFormRecessMonth,
    NewOSCFormAgeGroup,
    NewOSCFormMealType,
    NewOSCFormFoodDistribution,
    NewOSCFormFoodDistributionType,
    NewOSCFormEducationalUsage,
    NewOSCFormEducationalUsageType
    )


class CustomMMCF(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name

class NewOSCModelForm(ModelForm):
    
    class Meta:
        model = NewOSCFormModel
        fields = "__all__"
        widgets = {
            "nome": TextInput(attrs={ 'class': 'form-control', "readonly": True, 'id': "nome_field"}),
            "cnpj": TextInput(attrs={ 'class': 'form-control', 'id': "cnpj_field" }),
            "cep": TextInput(attrs={ 'class': 'form-control', 'id': "cep_field" }),
        }

    target_audience = CustomMMCF(
        queryset=NewOSCFormTargetAudience.objects.all(),
        widget=CheckboxSelectMultiple
    )
    
    recess_months = CustomMMCF(
        queryset=NewOSCFormRecessMonth.objects.all(),
        widget=CheckboxSelectMultiple
    )
    
    age_group = CustomMMCF(
        queryset=NewOSCFormAgeGroup.objects.all(),
        widget=CheckboxSelectMultiple
    )
    
    meal_types = CustomMMCF(
        queryset=NewOSCFormMealType.objects.all(),
        widget=CheckboxSelectMultiple
    )

class NewOSCFormFoodDistributionForm(ModelForm):

    class Meta:
        model = NewOSCFormFoodDistribution
        fields = "__all__"
        exclude = ('form_answer', )
    
    distribution_type = CustomMMCF(
        queryset=NewOSCFormFoodDistributionType.objects.all(),
        widget=CheckboxSelectMultiple
    )

class NewOSCFormEducationalUsageForm(ModelForm):

    class Meta:
        model = NewOSCFormEducationalUsage
        fields = "__all__"
        exclude = ('form_answer', )
    
    educational_usage_type = CustomMMCF(
        queryset=NewOSCFormEducationalUsageType.objects.all(),
        widget=CheckboxSelectMultiple
    )