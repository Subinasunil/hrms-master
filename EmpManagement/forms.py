# from django import forms
# from .models import EmployeeSkill

# class EmployeeSkillForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeSkill
#         fields = ['emp_id', 'language_skill', 'marketing_skill', 'programming_language_skill', 'value']
#         widgets = {
#             'value': forms.Select(attrs={'class': 'form-control'})
#         }

#     def __init__(self, *args, **kwargs):
#         super(EmployeeSkillForm, self).__init__(*args, **kwargs)
#         # Customize the queryset for the value field based on selected skill type
#         self.fields['value'].queryset = self.instance.get_selected_skill_queryset()
