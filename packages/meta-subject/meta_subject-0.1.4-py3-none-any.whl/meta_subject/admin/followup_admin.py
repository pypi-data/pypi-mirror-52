from django.contrib import admin
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

# from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_subject_admin
from ..forms import FollowupForm
from ..models import Followup
from .modeladmin import CrfModelAdminMixin


@admin.register(Followup, site=meta_subject_admin)
class FollowupAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):

    form = FollowupForm
