#!/usr/bin/env python3

from UserInput import UserInput
from FinancesCalculator import FinancesCalculator
from Output import Output

if __name__ == "__main__":
	# Initialize command line arguments:
	userInputHandler = UserInput()
	userInputHandler.initializeUserArguments()

	# Obtain the values that were supplied by
	# the user for the args:
	SALE_PRICE = userInputHandler.getSalePrice()
	DOWN_PAYMENT = userInputHandler.getDownPayment()
	INTEREST_RATE = userInputHandler.getInterestRate()
	timeDuration = userInputHandler.getTimeDuration()
	PMI = userInputHandler.getPmi() # Optional argument
	ADDITIONAL_MONTHLY_PRINCIPLE_PAYMENT = userInputHandler.getAdditionalMonthlyPrinciplePayment() # Optional argument

	# Perform a bit of extra parsing for timeDuration:
	if timeDuration[-1] != 'm':
		# Remove last char if
		# not numeric:
		timeDuration = int(timeDuration[:-1] if not timeDuration[-1].isnumeric() else timeDuration)

		# Treat it as a year and
		# convert to month:
		timeDuration *= 12

	financesHelper = FinancesCalculator()

	MONTHLY_MORTGAGE_PAYMENT = financesHelper.calculateMonthlyMortgagePayment(
		interestRate = INTEREST_RATE,
		totalLoanAmount = SALE_PRICE - DOWN_PAYMENT,
		termInMonths = timeDuration
	)

	(YEARS_UNTIL_AT_80_PERCENT_LOAN_TO_VALUE_RATIO, TOTAL_INTEREST_PAID) = financesHelper.calculateYearsUntil80LtvAndTotalInterest(
		interestRate = INTEREST_RATE,
		totalLoanAmount = SALE_PRICE - DOWN_PAYMENT,
		salePrice = SALE_PRICE,
		termInMonths = timeDuration,
		additionalPrinciplePayment = ADDITIONAL_MONTHLY_PRINCIPLE_PAYMENT
	)

	TOTAL_PMI_PAID = None
	if PMI is not None:
		TOTAL_PMI_PAID = financesHelper.calculateTotalPmiPaid(
			pmi = PMI,
			salePrice = SALE_PRICE,
			downPayment = DOWN_PAYMENT,
			yearsUntil80PercentLtv = YEARS_UNTIL_AT_80_PERCENT_LOAN_TO_VALUE_RATIO
		)

	Output.outputFormattedResults(
		salePrice = SALE_PRICE,
		downPayment = DOWN_PAYMENT,
		interestRate = INTEREST_RATE,
		timeDuration = timeDuration,
		monthlyMortgagePayment = MONTHLY_MORTGAGE_PAYMENT,
		yearsUntil80Ltv = YEARS_UNTIL_AT_80_PERCENT_LOAN_TO_VALUE_RATIO,
		totalInterestPaid = TOTAL_INTEREST_PAID,
		pmi = PMI,
		totalPmiPaid = TOTAL_PMI_PAID
	)

