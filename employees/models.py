from django.db import models

# Create your models here.
class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name= models.CharField(max_length=100)
    designation= models.CharField(max_length=100)
    joining_date= models.DateField()
    basic_salary= models.DecimalField(max_digits=10,decimal_places=2)
    hra_percent=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    da_percent=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    other_allowance_percent=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    esi_percent=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    pf_percent=models.DecimalField(max_digits=5,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.employee_id} - {self.name}"
class Payslip(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='payslips'
    )

    month = models.DateField()

    leave_count = models.PositiveIntegerField(default=0)

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    hra = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    da = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    other_allowance = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    gross_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    pf = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    esi = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'month'],
                name='unique_employee_month_payslip'
            )
        ]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.month}"
