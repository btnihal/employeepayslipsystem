from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from .models import Employee, Payslip
from .services import calculate_salary


class EmployeeModelTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id='EMP001',
            name='Test Employee',
            designation='Python Developer',
            joining_date='2026-09-01',
            basic_salary=Decimal('30000'),
            hra_percent=Decimal('20'),
            da_percent=Decimal('10'),
            other_allowance_percent=Decimal('5'),
            esi_percent=Decimal('0.75'),
            pf_percent=Decimal('12'),
        )

    def test_employee_created(self):
        self.assertEqual(
            self.employee.name,
            'Test Employee'
        )

        self.assertEqual(
            self.employee.employee_id,
            'EMP001'
        )


class SalaryCalculationTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id='EMP002',
            name='Salary Test',
            designation='Developer',
            joining_date='2026-09-01',
            basic_salary=Decimal('30000'),
            hra_percent=Decimal('20'),
            da_percent=Decimal('10'),
            other_allowance_percent=Decimal('5'),
            esi_percent=Decimal('0.75'),
            pf_percent=Decimal('12'),
        )

    def test_salary_calculation(self):

        salary = calculate_salary(
            self.employee,
            leave_count=2
        )

        self.assertEqual(
            salary['basic_salary'],
            Decimal('28000.00')
        )

        self.assertEqual(
            salary['gross_salary'],
            Decimal('37800.00')
        )

        self.assertEqual(
            salary['net_salary'],
            Decimal('34230.00')
        )


class PayslipConstraintTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id='EMP003',
            name='Duplicate Test',
            designation='Developer',
            joining_date='2026-09-01',
            basic_salary=Decimal('30000'),
            hra_percent=Decimal('20'),
            da_percent=Decimal('10'),
            other_allowance_percent=Decimal('5'),
            esi_percent=Decimal('0.75'),
            pf_percent=Decimal('12'),
        )

    def test_payslip_can_be_created(self):

        payslip = Payslip.objects.create(
            employee=self.employee,
            month='2026-09-01',
            leave_count=2,
            basic_salary=Decimal('28000'),
            hra=Decimal('5600'),
            da=Decimal('2800'),
            other_allowance=Decimal('1400'),
            gross_salary=Decimal('37800'),
            pf=Decimal('3360'),
            esi=Decimal('210'),
            net_salary=Decimal('34230'),
        )

        self.assertEqual(
            payslip.employee.employee_id,
            'EMP003'
        )

    def test_duplicate_payslip_is_not_allowed(self):

        # First payslip
        Payslip.objects.create(
            employee=self.employee,
            month='2026-09-01',
            leave_count=2,
            basic_salary=Decimal('28000'),
            hra=Decimal('5600'),
            da=Decimal('2800'),
            other_allowance=Decimal('1400'),
            gross_salary=Decimal('37800'),
            pf=Decimal('3360'),
            esi=Decimal('210'),
            net_salary=Decimal('34230'),
        )

        # Second payslip for the same employee and same month
        with self.assertRaises(IntegrityError):

            Payslip.objects.create(
                employee=self.employee,
                month='2026-09-01',
                leave_count=3,
                basic_salary=Decimal('27000'),
                hra=Decimal('5400'),
                da=Decimal('2700'),
                other_allowance=Decimal('1350'),
                gross_salary=Decimal('36450'),
                pf=Decimal('3240'),
                esi=Decimal('202.50'),
                net_salary=Decimal('33007.50'),
            )