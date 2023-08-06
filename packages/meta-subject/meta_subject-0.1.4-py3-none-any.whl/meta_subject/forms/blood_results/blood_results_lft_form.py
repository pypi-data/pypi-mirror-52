from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_visit_tracking.modelform_mixins import SubjectModelFormMixin
from meta_form_validators.form_validators import BloodResultsFormValidator

from ...models import BloodResultsLft


class BloodResultsLftForm(ActionItemFormMixin, SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsFormValidator

    class Meta:
        model = BloodResultsLft
        fields = "__all__"
