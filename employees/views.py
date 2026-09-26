from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip
from .forms import EmployeeForm, PayslipForm
from decimal import Decimal
from .services import calculate_salary
from django.db import IntegrityError
def emp_list(request):
    employees = Employee.objects.all()

    return render(
        request,
        'employees/emp_list.html',
        {'employees': employees}
    )


def emp_create(request):

    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('emp_list')

    else:
        form = EmployeeForm()

    return render(
        request,
        'employees/emp_form.html',
        {'form': form}
    )


def emp_detail(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    return render(
        request,
        'employees/emp_detail.html',
        {'employee': employee}
    )


def emp_update(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    if request.method == 'POST':
        form = EmployeeForm(
            request.POST,
            instance=employee
        )

        if form.is_valid():
            form.save()
            return redirect(
                'emp_detail',
                pk=employee.pk
            )

    else:
        form = EmployeeForm(
            instance=employee
        )

    return render(
        request,
        'employees/emp_form.html',
        {
            'form': form,
            'employee': employee
        }
    )


def emp_delete(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    if request.method == 'POST':
        employee.delete()
        return redirect('emp_list')

    return render(
        request,
        'employees/emp_confirm_delete.html',
        {'employee': employee}
    )

def generate_payslip(request):

    if request.method == 'POST':

        form = PayslipForm(request.POST)

        if form.is_valid():

            employee = form.cleaned_data['employee']

            month = form.cleaned_data['month']

            leave_count = form.cleaned_data[
                'leave_count'
            ]

            salary = calculate_salary(
                employee,
                leave_count
            )

            payslip = Payslip.objects.create(
                employee=employee,
                month=month,
                leave_count=leave_count,

                basic_salary=salary[
                    'basic_salary'
                ],

                hra=salary[
                    'hra'
                ],

                da=salary[
                    'da'
                ],

                other_allowance=salary[
                    'other_allowance'
                ],

                gross_salary=salary[
                    'gross_salary'
                ],

                pf=salary[
                    'pf'
                ],

                esi=salary[
                    'esi'
                ],

                net_salary=salary[
                    'net_salary'
                ],
            )

            return redirect(
                'payslip_detail',
                pk=payslip.pk
            )

    else:

        form = PayslipForm()

    return render(
        request,
        'employees/payslip_form.html',
        {'form': form}
    )
def payslip_detail(request, pk):

    payslip = get_object_or_404(
        Payslip,
        pk=pk
    )

    return render(
        request,
        'employees/payslip_detail.html',
        {'payslip': payslip}
    )

def dashboard(request):
    total_employees = Employee.objects.count()
    total_payslips = Payslip.objects.count()

    recent_employees = Employee.objects.order_by('-id')[:5]

    recent_payslips = Payslip.objects.select_related(
        'employee'
    ).order_by('-created_at')[:5]

    return render(
        request,
        'employees/dashboard.html',
        {
            'total_employees': total_employees,
            'total_payslips': total_payslips,
            'recent_employees': recent_employees,
            'recent_payslips': recent_payslips,
        }
    )
def payslip_history(request):
    payslips = Payslip.objects.select_related(
        'employee'
    ).order_by('-month', '-created_at')

    return render(
        request,
        'employees/payslip_history.html',
        {
            'payslips': payslips
        }
    )