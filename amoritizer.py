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

	YEARS_UNTIL_AT_80_PERCENT_LOAN_TO_VALUE_RATIO = financesHelper.calculateYearsUntil80Ltv(
		interestRate = INTEREST_RATE,
		totalLoanAmount = SALE_PRICE - DOWN_PAYMENT,
		salePrice = SALE_PRICE,
		termInMonths = timeDuration
	)

	Output.outputFormattedResults(
		salePrice = SALE_PRICE,
		downPayment = DOWN_PAYMENT,
		interestRate = INTEREST_RATE,
		timeDuration = timeDuration,
		monthlyMortgagePayment = MONTHLY_MORTGAGE_PAYMENT,
		yearsUntil80Ltv = YEARS_UNTIL_AT_80_PERCENT_LOAN_TO_VALUE_RATIO,
		pmi = PMI
	)

