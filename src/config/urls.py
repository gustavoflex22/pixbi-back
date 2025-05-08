from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from src.modules.forms.views import (
    PreSaveNewOSCFormView,
    NewOSCFormView,
    NewOSCFormTargetAudienceView,
    NewOSCFormRecessMonthView,
    NewOSCFormAgeGroupView,
    NewOSCFormMealTypeView,
    NewOSCFormFoodDistributionTypeView,
    NewOSCFormEducationalUsageTypeView,
    NewOSCFormOtherPartnerFoodTypeView,
    NewOSCFormOtherPartnerTypeView,
    NewOSCFormOtherPartnerFrequencyRecevedView,
    NewOSCFormDonationExtractionTransportTypeView,
)
from src.modules.users.views import UserView


router = routers.DefaultRouter()

router.register(r"pre-save", PreSaveNewOSCFormView, basename="pre-save")
router.register(r"new-osc-form", NewOSCFormView, basename="new-osc-form")
router.register(r"target-audience", NewOSCFormTargetAudienceView, basename="target-audience")
router.register(r"recess-mounth", NewOSCFormRecessMonthView, basename="recess-mounth")
router.register(r"age-group", NewOSCFormAgeGroupView, basename="age-group")
router.register(r"meal-type", NewOSCFormMealTypeView, basename="meal-type")
router.register(r"distribution-type", NewOSCFormFoodDistributionTypeView, basename="distribution-type")
router.register(r"educational-usage-type", NewOSCFormEducationalUsageTypeView, basename="educational-usage-type")
router.register(r"other-partner-food-type", NewOSCFormOtherPartnerFoodTypeView, basename="other-partner-food-type")
router.register(r"other-partner-type", NewOSCFormOtherPartnerTypeView, basename="other-partner-type")
router.register(r"other-partner-frequency-receved", NewOSCFormOtherPartnerFrequencyRecevedView, basename="other-partner-frequency-receved")
router.register(r"donation-extraction-transport-type", NewOSCFormDonationExtractionTransportTypeView, basename="donation-extraction-transport-type")
router.register(r"users", UserView, basename="users")


urlpatterns = [
    path('api/', include(router.urls)),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
