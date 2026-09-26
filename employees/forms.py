from django import forms
from .models import Employee, Payslip


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = [
            'employee_id',
            'name',
            'designation',
            'joining_date',
            'basic_salary',
            'hra_percent',
            'da_percent',
            'other_allowance_percent',
            'esi_percent',
            'pf_percent',
        ]

        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

class PayslipForm(forms.ModelForm):

    class Meta:
        model = Payslip

        fields = [
            'employee',
            'month',
            'leave_count',
        ]

        widgets = {
            'month': forms.DateInput(
                format='%Y-%m',
                attrs={
                    'type': 'month'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['month'].input_formats = [
            '%Y-%m'
        ]

    def clean_month(self):
        month = self.cleaned_data['month']

        return month.replace(day=1)

    def clean_leave_count(self):

        leave_count = self.cleaned_data[
            'leave_count'
        ]

        if leave_count < 0:
            raise forms.ValidationError(
                'Leave count cannot be negative.'
            )

        if leave_count > 30:
            raise forms.ValidationError(
                'Leave count cannot exceed 30 days.'
            )

        return leave_count