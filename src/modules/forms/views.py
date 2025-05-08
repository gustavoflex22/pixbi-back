from datetime import datetime
import pandas as pd
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import TruncMonth
from django.db.models import Count
import newrelic.agent
from django.core.cache import cache
from django.http import HttpResponse
from src.modules.forms.models.pre_save_models import PreSaveNewOSCFormModel
from src.modules.forms.models.models import (
    NewOSCFormModel,
    NewOSCFormTargetAudience,
    NewOSCFormRecessMonth,
    NewOSCFormAgeGroup,
    NewOSCFormMealType,
    NewOSCFormFoodDistributionType,
    NewOSCFormEducationalUsageType,
    NewOSCFormOtherPartnerFoodType,
    NewOSCFormOtherPartnerType,
    NewOSCFormOtherPartnerFrequencyReceved,
    NewOSCFormDonationExtractionTransportType,
)
from src.modules.forms.serializers.enum_serializers import (
    NewOSCFormTargetAudienceSerializer,
    NewOSCFormRecessMonthSerializer,
    NewOSCFormAgeGroupSerializer,
    NewOSCFormMealTypeSerializer,
    NewOSCFormFoodDistributionTypeSerializer,
    NewOSCFormEducationalUsageTypeSerializer,
    NewOSCFormOtherPartnerFoodTypeSerializer,
    NewOSCFormOtherPartnerTypeSerializer,
    NewOSCFormOtherPartnerFrequencyRecevedSerializer,
    NewOSCFormDonationExtractionTransportTypeSerializer,

)
from src.modules.forms.serializers.new_osc_form_serializers import (
    NewOSCFormSerializer,
    PreSaveNewOSCFormSerializer,
    CacheFormResponseSerializer
)


class PreSaveNewOSCFormView(ModelViewSet):
    queryset = PreSaveNewOSCFormModel.objects.all()
    serializer_class = PreSaveNewOSCFormSerializer

    DEFAULT_CACHE_EXPIRATION = 86400 # one day


    @action(methods=['POST'], detail=False, serializer_class=CacheFormResponseSerializer, permission_classes = (IsAuthenticated,))
    def cached_response(self, request):
        
        current_user = request.user
        request.data['user_id'] = current_user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        if validated_data.get("new_data"):
            cache.set(
                f"{validated_data.get('user_id')}", #_{validated_data.get('step')}
                validated_data.get("new_data"),
                self.DEFAULT_CACHE_EXPIRATION
            )
            return Response(status=HTTP_201_CREATED)
        
        cached = cache.get(f"{validated_data.get('user_id')}") #_{validated_data.get('step')}
        return Response(status=HTTP_200_OK, data=cached)


class NewOSCFormView(ModelViewSet):
    queryset = NewOSCFormModel.objects.all()
    serializer_class = NewOSCFormSerializer

    def create(self, request, *args, **kwargs):
        newrelic.agent.add_custom_attribute("payload", request.data)
        return super().create(request, *args, **kwargs)
    
    @action(methods=["GET"], detail=False)
    def count(self, request):
        return Response(data=NewOSCFormModel.objects.count())
    
    @action(methods=["GET"], detail=False)
    def count_by_month(self, request):
        count_by_name_months = [0 for _ in range(1,12)]
        query = NewOSCFormModel.objects.filter(created_at__year=datetime.now().year)
        count_by_months = query.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).values("month", "count").all()
        for val in count_by_months:
            count_by_name_months[val.get("month").month - 1] = val.get("count")
        return Response(data=count_by_name_months)

    @action(methods=["GET"], detail=False)
    def count_by_city(self, request):
        query = NewOSCFormModel.objects.filter(created_at__year=datetime.now().year)
        count_by_city = query.values('city').annotate(count=Count('city')).values("city", "count").order_by('-count').all()
        count_by_city = count_by_city[:8]
        return Response(data=count_by_city)
    
    @action(methods=["GET"], detail=False)
    def count_city(self, request):
        query = NewOSCFormModel.objects.filter(created_at__year=datetime.now().year)
        return Response(data=len(set(query.values_list("city", flat=True))))
    
    @action(methods=["GET"], detail=False)
    def export_all_answers(self, request):
        query = NewOSCFormModel.objects.all().values()
        df = pd.DataFrame(list(query))

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=persons.xlsx'

        df.to_excel(response, index=False, engine='openpyxl')

        return response
    

class NewOSCFormTargetAudienceView(ModelViewSet):

    queryset = NewOSCFormTargetAudience.objects.filter(default=True).all()
    serializer_class = NewOSCFormTargetAudienceSerializer

class NewOSCFormRecessMonthView(ModelViewSet):

    queryset = NewOSCFormRecessMonth.objects.all()
    serializer_class = NewOSCFormRecessMonthSerializer

class NewOSCFormAgeGroupView(ModelViewSet):

    queryset = NewOSCFormAgeGroup.objects.all()
    serializer_class = NewOSCFormAgeGroupSerializer

class NewOSCFormMealTypeView(ModelViewSet):

    queryset = NewOSCFormMealType.objects.all()
    serializer_class = NewOSCFormMealTypeSerializer

class NewOSCFormFoodDistributionTypeView(ModelViewSet):

    queryset = NewOSCFormFoodDistributionType.objects.filter(default=True).all()
    serializer_class = NewOSCFormFoodDistributionTypeSerializer

class NewOSCFormDonationExtractionTransportTypeView(ModelViewSet):

    queryset = NewOSCFormDonationExtractionTransportType.objects.filter(default=True).all()
    serializer_class = NewOSCFormDonationExtractionTransportTypeSerializer

class NewOSCFormEducationalUsageTypeView(ModelViewSet):

    queryset = NewOSCFormEducationalUsageType.objects.filter(default=True).all()
    serializer_class = NewOSCFormEducationalUsageTypeSerializer

class NewOSCFormOtherPartnerFoodTypeView(ModelViewSet):

    queryset = NewOSCFormOtherPartnerFoodType.objects.filter(default=True).all()
    serializer_class = NewOSCFormOtherPartnerFoodTypeSerializer

class NewOSCFormOtherPartnerTypeView(ModelViewSet):

    queryset = NewOSCFormOtherPartnerType.objects.filter(default=True).all()
    serializer_class = NewOSCFormOtherPartnerTypeSerializer

class NewOSCFormOtherPartnerFrequencyRecevedView(ModelViewSet):

    queryset = NewOSCFormOtherPartnerFrequencyReceved.objects.filter(default=True).all()
    serializer_class = NewOSCFormOtherPartnerFrequencyRecevedSerializer