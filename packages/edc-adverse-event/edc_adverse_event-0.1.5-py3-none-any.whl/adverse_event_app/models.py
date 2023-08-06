from django.db import models
from django.db.models.deletion import PROTECT
from edc_adverse_event.model_mixins import (
    AeInitialModelMixin,
    AeFollowupModelMixin,
    AeSusarModelMixin,
    AesiModelMixin,
    AeTmgModelMixin,
    DeathReportModelMixin,
    DeathReportTmgModelMixin,
)
from edc_identifier.managers import SubjectIdentifierManager
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_visit_schedule.model_mixins import OnScheduleModelMixin, CurrentSiteManager
from edc_action_item.models.action_model_mixin import ActionModelMixin
from edc_identifier.model_mixins.tracking_model_mixin import TrackingModelMixin
from edc_visit_schedule.model_mixins.off_schedule_model_mixin import OffScheduleModelMixin
from edc_adverse_event.constants import STUDY_TERMINATION_CONCLUSION_ACTION


class OnSchedule(OnScheduleModelMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by subject_consent.
    """

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def put_on_schedule(self):
        pass

    class Meta(OnScheduleModelMixin.Meta):
        pass


class StudyTerminationConclusion(
        ActionModelMixin, TrackingModelMixin, OffScheduleModelMixin, BaseUuidModel):

    action_name = STUDY_TERMINATION_CONCLUSION_ACTION

    tracking_identifier_prefix = "ST"

    subject_identifier = models.CharField(max_length=50, unique=True)

    class Meta(OffScheduleModelMixin.Meta):
        pass


class AeInitial(
    AeInitialModelMixin, BaseUuidModel
):

    class Meta(AeInitialModelMixin.Meta):
        pass


class AeFollowup(AeFollowupModelMixin, BaseUuidModel):

    ae_initial = models.ForeignKey(AeInitial, on_delete=PROTECT)

    class Meta(AeFollowupModelMixin.Meta):
        pass


class Aesi(AesiModelMixin, BaseUuidModel):

    ae_initial = models.ForeignKey(AeInitial, on_delete=PROTECT)

    class Meta(AesiModelMixin.Meta):
        pass


class AeSusar(AeSusarModelMixin, BaseUuidModel):

    ae_initial = models.ForeignKey(AeInitial, on_delete=PROTECT)

    class Meta(AeSusarModelMixin.Meta):
        pass


class AeTmg(AeTmgModelMixin, BaseUuidModel):

    ae_initial = models.ForeignKey(AeInitial, on_delete=PROTECT)

    class Meta(AeTmgModelMixin.Meta):
        pass


class DeathReport(DeathReportModelMixin, BaseUuidModel):

    class Meta(DeathReportModelMixin.Meta):
        pass


class DeathReportTmg(DeathReportTmgModelMixin, BaseUuidModel):

    class Meta(DeathReportTmgModelMixin.Meta):
        pass
