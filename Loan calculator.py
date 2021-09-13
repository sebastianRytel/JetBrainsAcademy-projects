import argparse
import math
import sys

parser = argparse.ArgumentParser()

parser.add_argument('--type', choices=['annuity', 'diff'])
parser.add_argument('--principal')
parser.add_argument('--periods')
parser.add_argument('--interest')
parser.add_argument('--payment')

args = parser.parse_args()
list_args = sys.argv

list_arguments = [args.type, args.principal, args.periods, args.interest, args.payment]
list_arguments_str_cast = [str(list_arguments[i]) for i in range(len(list_arguments))]

for element in list_arguments_str_cast:
    if '-' in element:
        print("Incorrect parameters.")
        quit()   
if not args.type:
    print("Incorrect parameters.")
    quit() 
if args.type == 'diff':
    if args.payment:
        print("Incorrect parameters.")
        quit()
    if len(list_args) < 5:
        print("Incorrect parameters.")
        quit()   
 
    sum_month_diff_pay = 0
    i = (float(args.interest) / 100) / 12 * 1
    for m in range(1, int(args.periods)+1):
        month_diff_pay = int(args.principal) / int(args.periods) + i * (int(args.principal) - (int(args.principal) * (m - 1) / int(args.periods)))
        sum_month_diff_pay += math.ceil(month_diff_pay)
        print(f'Month {m}: payment is {math.ceil(month_diff_pay)}')
    print(f'\nOverpayment = {math.ceil(sum_month_diff_pay - (int(args.principal)))}')

elif args.type == 'annuity':
    if not args.interest:
        print("Incorrect parameters.")
        quit()
    if args.principal and args.periods and args.interest:
        i = (float(args.interest) / 100) / 12 * 1
        a = int(args.principal) * (i * math.pow((1 + i), int(args.periods))) / (math.pow((1 + i), int(args.periods)) - 1)    
        overpayment = math.ceil(a) * int(args.periods) - int(args.principal)
        print(f'Your annuity payment = {math.ceil(a)}!')
        print(f'Overpayment = {overpayment}')
    elif args.payment and args.periods and args.interest:
        i = (float(args.interest) / 100) / 12 * 1
        loan_principal = int(args.payment) / ((i * math.pow((1 + i), int(args.periods))) / (math.pow((1 + i), int(args.periods)) - 1))
        overpayment = int(args.payment) * int(args.periods) - loan_principal
        print(f'Your loan principal = {math.ceil(loan_principal)}!')
        print(f'Overpayment = {math.ceil(overpayment)}')
    else:
        i = (float(args.interest) / 100) / 12 * 1
        base = i + 1
        x = int(args.payment) / (int(args.payment) - (i * int(args.principal)))
        number_months = math.log(x, base)
        years = int(math.ceil(number_months) / 12)
        overpayment = (math.ceil(number_months) * int(args.payment)) - int(args.principal)
        print(f'It will take {years} years to repay this loan!')
        print(f'Overpayment = {overpayment}')
