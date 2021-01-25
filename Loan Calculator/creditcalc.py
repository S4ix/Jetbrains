import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type",
                    choices=["annuity", "diff"])
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()
arguments = [args.type, int(args.payment) if args.payment else None, int(args.principal)if args.principal else None,
             int(args.periods) if args.periods else None, float(args.interest) if args.interest else None]

valid = True
if arguments.count(None) < 2:
    if (not arguments[1] or arguments[1] >= 0) and (not arguments[2] or arguments[2] >= 0) \
            and (not arguments[3] or arguments[3] >= 0) and (not arguments[4] or arguments[4] >= 0):
        if args.type not in ["annuity", "diff"]:
            print("Incorrect parameters")
            valid = False
        elif args.type == "diff" and args.payment:
            print("Incorrect parameters")
            valid = False
        if not args.interest:
            print("Incorrect parameters")
            valid = False
    else:
        print("Incorrect parameters")
        valid = False
else:
    print("Incorrect parameters")
    valid = False

calc_type = args.type
loan_principal = int(args.principal or 0)
number_of_periods = int(args.periods or 0)
loan_interest = float(args.interest or 0.0)
annuity_payment = int(args.payment or 0)

if valid:
    if calc_type == "diff":
        nominal_interest_rate = loan_interest / (12 * 100)
        payment = loan_principal / number_of_periods
        payment_sum = 0
        for i in range(number_of_periods):
            rest = loan_principal - ((loan_principal * i) / number_of_periods)
            monthly_diff_payment = math.ceil(payment + nominal_interest_rate * rest)
            print(f'Month {i + 1}: payment is {monthly_diff_payment}')
            payment_sum += monthly_diff_payment
        print(f'\nOverpayment = {payment_sum - loan_principal}')

    elif calc_type == "annuity":
        if number_of_periods == 0:
            nominal_interest_rate = loan_interest / (12 * 100)
            number_of_months = math.ceil(math.log(annuity_payment / (annuity_payment - nominal_interest_rate * loan_principal), 1 + nominal_interest_rate))
            years = number_of_months // 12
            months = number_of_months % 12
            if years > 0:
                year_string = f'It will take {years} year{"s" if years > 1 else ""}'
            if months > 0:
                month_string = f' and {months} month{"s" if months > 1 else ""}'
            else:
                month_string = ''
            print(year_string + month_string + ' to repay this loan!')
            print(f'Overpayment = {number_of_months * annuity_payment - loan_principal}')
        if annuity_payment == 0:
            nominal_interest_rate = loan_interest / (12 * 100)
            annuity = loan_principal * (nominal_interest_rate * math.pow(1 + nominal_interest_rate, number_of_periods))/(math.pow(1 + nominal_interest_rate, number_of_periods) - 1)
            print(f'Your annuity payment = {math.ceil(annuity)}!')
            print(f'Overpayment = {math.ceil(annuity) * number_of_periods - loan_principal}')

        if loan_principal == 0:
            nominal_interest_rate = loan_interest / (12 * 100)
            denominator = (nominal_interest_rate * math.pow(1 + nominal_interest_rate, number_of_periods))/(math.pow(1 + nominal_interest_rate, number_of_periods) - 1)
            loan_principal = math.floor(annuity_payment / denominator)
            print(f'Your loan principal = {loan_principal}!')
            print(f'Overpayment = {annuity_payment * number_of_periods - loan_principal}')

