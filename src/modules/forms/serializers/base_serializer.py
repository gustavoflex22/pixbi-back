from rest_framework.serializers import (
    ModelSerializer,
    Field,
    ValidationError
)

class MyField(Field):
    def to_representation(self, value):
        if isinstance(value, int):
            return value
        elif isinstance(value, str) and value.isdigit():
            return value
        raise ValidationError('Error')

    def to_internal_value(self, data):
        if isinstance(data, int):
            return data
        elif isinstance(data, str):
            return data
        raise ValidationError('Error')

class BaseModelSerializer(ModelSerializer):

    def format_digit_to_int(self, data):
        return int(data) if isinstance(data, str) and data.isdigit() else data

    def get_or_create_many_to_many_instances(self, validated_data, model, many=False, **kwargs):
        if many:
            instance_list = []
            for data in validated_data:
                instance_list.append(self.get_or_create_instance(data, model, **kwargs))
            return instance_list
        return self.get_or_create_instance(validated_data, model, **kwargs)
    
    def get_or_create_instance(self, data, model, **kwargs):
        data = self.format_digit_to_int(data)
        if type(data) == str:
            return model.objects.get_or_create(name=data, **kwargs)[0]
        return model.objects.get(id=data)

    def save_many_to_many_instances(self, validated_data, serializer: ModelSerializer, **kwargs):
        if not validated_data:
            return None
        list_data = list(map(lambda x: {**{x_key: x_value if type(x_value) in [str, int] else x_value.id for x_key, x_value in x.items()}  , **kwargs}, validated_data))
        mm_instance: ModelSerializer = serializer(data=list_data, many=True)
        mm_instance.is_valid(raise_exception=True)

        return mm_instance.save()

    def set_list_many_to_many_instances(self, instance, instance_attr, many_validated_data, many_model, **kwargs):
        if not many_validated_data:
            return None
        target_audience_instance_list = self.get_or_create_many_to_many_instances(many_validated_data, many_model, many=True, **kwargs)
        getattr(instance,instance_attr).set(target_audience_instance_list)
    
    def set_one_to_many_instances(self, instance, instance_attr, many_validated_data, many_model, **kwargs):
        if not many_validated_data:
            return None
        target_audience_instance_list = self.get_or_create_many_to_many_instances(many_validated_data, many_model, **kwargs)
        setattr(instance, instance_attr, target_audience_instance_list)
        instance.save()