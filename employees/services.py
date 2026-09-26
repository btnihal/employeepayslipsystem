from decimal import Decimal, ROUND_HALF_UP


def calculate_salary(employee, leave_count):

    basic_salary = employee.basic_salary

    
    daily_salary = basic_salary / Decimal('30')

    leave_deduction = daily_salary * Decimal(leave_count)

    # Basic salary after leave
    adjusted_basic = basic_salary - leave_deduction

    # Prevent negative salary
    if adjusted_basic < 0:
        adjusted_basic = Decimal('0')

    hra = (
        adjusted_basic *
        employee.hra_percent /
        Decimal('100')
    )

    da = (
        adjusted_basic *
        employee.da_percent /
        Decimal('100')
    )

    other_allowance = (
        adjusted_basic *
        employee.other_allowance_percent /
        Decimal('100')
    )

    gross_salary = (
        adjusted_basic +
        hra +
        da +
        other_allowance
    )

    pf = (
        adjusted_basic *
        employee.pf_percent /
        Decimal('100')
    )

    esi = (
        adjusted_basic *
        employee.esi_percent /
        Decimal('100')
    )

    net_salary = gross_salary - pf - esi

    # Round money values to 2 decimal places
    def money(value):
        return value.quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

    return {
        'basic_salary': money(adjusted_basic),
        'hra': money(hra),
        'da': money(da),
        'other_allowance': money(other_allowance),
        'gross_salary': money(gross_salary),
        'pf': money(pf),
        'esi': money(esi),
        'net_salary': money(net_salary),
    }