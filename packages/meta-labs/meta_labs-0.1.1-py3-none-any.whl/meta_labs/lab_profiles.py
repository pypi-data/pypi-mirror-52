from edc_lab import LabProfile

from .panels import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    chemistry_alt_panel,
    chemistry_panel,
    fbc_panel,
    hba1c_panel,
    hba1c_poc_panel,
)


subject_lab_profile = LabProfile(
    name="subject_lab_profile", requisition_model="meta_subject.subjectrequisition"
)

subject_lab_profile.add_panel(fbc_panel)
subject_lab_profile.add_panel(blood_glucose_panel)
subject_lab_profile.add_panel(blood_glucose_poc_panel)
subject_lab_profile.add_panel(hba1c_panel)
subject_lab_profile.add_panel(hba1c_poc_panel)
subject_lab_profile.add_panel(chemistry_panel)
subject_lab_profile.add_panel(chemistry_alt_panel)
