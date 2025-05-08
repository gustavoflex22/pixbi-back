from django.db import models
from django.utils.translation import gettext_lazy as _


class PriorityCategoryEnum(models.TextChoices):
    ILP = "ILP", _("Instituição de Longa Permanência")
    IOAS = "IOAS", _("Instituição de Organização e Apoio Social")
    UDM = "UDM", _("Unidade de Distribuição / Mediadora")

class DisponibilityCollectionEnum(models.TextChoices):
    ONEX = "ONEX", _("1 vez por semana")
    TWOX = "TWOX", _("2 vezes por semana")
    THREEX = "THREEX", _("3 vezes por semana")
    FOURX = "FOURX", _("4 vezes por semana")
    FIVEX = "FIVEX", _("5 vezes por semana")
    SIXX = "SIXX", _("6 vezes por semana")
    ALLX = "ALLX", _("Todos os dias")