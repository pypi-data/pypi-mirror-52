from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_visit_tracking.modelform_mixins import SubjectModelFormMixin
from meta_form_validators.form_validators import BloodResultsFormValidator

from ...models import BloodResultsFbc


class BloodResultsFbcFormValidator(BloodResultsFormValidator):
    def clean(self):

        self.required_if_true(
            self.cleaned_data.get("hemoglobin") is not None,
            field_required="fbc_requisition",
        )
        self.validate_reportable_fields(reference_list_name=self.reference_list_name)


class BloodResultsFbcForm(ActionItemFormMixin, SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultsFormValidator

    class Meta:
        model = BloodResultsFbc
        fields = "__all__"
