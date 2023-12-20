# PyMoritizer

A python tool for calculating various mortgage related information—e.g., interest page before desired LTV is reached, years until desired LTV is reached, monthly mortgage payment, PMI paid before reaching standard 80% LTV, etc.

## Usage

```bash
$ python3 amoritizer.py -h
usage: amoritizer.py [-h] -s SALEPRICE -d DOWNPAYMENT -i INTERESTRATE -t
                     TIMEDURATION -l DESIREDLTV [-p PMI]
                     [-a ADDITIONALMONTHLYPRINCIPLEPAYMENT]

optional arguments:
  -h, --help            show this help message and exit
  -s SALEPRICE, --sale-price SALEPRICE
                        Total price of the house.
  -d DOWNPAYMENT, --down-payment DOWNPAYMENT
                        Intended down payment on the house.
  -i INTERESTRATE, --interest-rate INTERESTRATE
                        Interest rate associated with the mortgage loan. NOTE:
                        do not input percentage but, rather, the float version
                        thereof (e.g., not '5%' but, rather, '0.05')
  -t TIMEDURATION, --time-duration TIMEDURATION
                        The duration of time the loan is set for. Use 'm' for
                        months or 'y' for years (e.g., '-d 7m' or '-d 7y'). If
                        no unit is specified, then this defaults to years.
  -l DESIREDLTV, --desired-ltv DESIREDLTV
                        The desired remaining LTV (Loan-To-Value ratio). This
                        is used to calculate various things, such as the
                        interest paid.
  -p PMI, --pmi PMI     The PMI percentage. NOTE: do not input percentage but,
                        rather, the float version thereof (e.g., not '5%' but,
                        rather, '0.05').
  -a ADDITIONALMONTHLYPRINCIPLEPAYMENT, --additional-monthly-principle-payment ADDITIONALMONTHLYPRINCIPLEPAYMENT
                        An additional principle payment per month.
```

## Example

```bash
$ pymortizer -s 260000 -d 50000 -i 0.0726 -t 30y -l 0.0 -a 100
WARNING: This program is not expert financial advice: it is an estimation based off of your input. Please refer to an expert financial advisor before finalizing any loans pertinent hereto.
Sale Price: $260000.0
Down Payment: $50000.0
Loan Amount: $210000.0
Interest Rate (%): 7.26%
Time Duration (Term): 30.0 years (360 months)

--------------------

Years Until 0.0% LTV Is Reached: 24.416666666666668
Monthly Mortgage Payment: $1533.9948380073315
Total Interest Paid By 0.0% LTV: $238007.941048919
```