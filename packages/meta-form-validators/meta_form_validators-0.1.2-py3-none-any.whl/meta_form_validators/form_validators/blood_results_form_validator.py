# from django.apps import apps as django_apps
from edc_reportable import GRADE3, GRADE4
from edc_reportable.form_validator_mixin import ReportablesFormValidatorMixin
from edc_lab.form_validators import CrfRequisitionFormValidatorMixin
from edc_form_validators.form_validator import FormValidator


class BloodResultsFormValidator(
    ReportablesFormValidatorMixin, CrfRequisitionFormValidatorMixin, FormValidator
):

    reportable_grades = [GRADE3, GRADE4]
    reference_list_name = "meta"
