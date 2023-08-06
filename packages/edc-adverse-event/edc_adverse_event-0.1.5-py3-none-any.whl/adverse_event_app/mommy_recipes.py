from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE
from edc_reportable import GRADE4
from edc_utils import get_utcnow
from faker import Faker
from model_mommy.recipe import Recipe

from .models import AeInitial, AeTmg, AeFollowup, AeSusar

fake = Faker()


aeinitial = Recipe(
    AeInitial,
    action_identifier=None,
    tracking_identifier=None,
    ae_description="A description of this event",
    ae_grade=GRADE4,
    ae_study_relation_possibility=YES,
    ae_start_date=get_utcnow().date(),
    ae_awareness_date=get_utcnow().date(),
    sae=NO,
    susar=NO,
    susar_reported=NOT_APPLICABLE,
    ae_cause=NO,
    ae_cause_other=None,
)

aetmg = Recipe(AeTmg, action_identifier=None, tracking_identifier=None)

aesusar = Recipe(AeSusar, action_identifier=None, tracking_identifier=None)

aefollowup = Recipe(
    AeFollowup, relevant_history=NO, action_identifier=None, tracking_identifier=None
)
