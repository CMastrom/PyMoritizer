#!/usr/bin/env python3

from UserInput import UserInput
from FinancesCalculator import FinancesCalculator
from Output import Output
from sys import version_info, exit

if __name__ == "__main__":
	# Ensure that this is running python 3:
	if version_info[0] < 3:
		Output.printErrorMessage(f"This script only works with Python version >= 3. Python version {version_info[0]}.{version_info[1]}.{version_info[2]} was detected.")
		exit(1)

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
	
	# The NIFA args must either (1) all be present or (2) none:
	NIFA_INTEREST_RATE = userInputHandler.getNifaInterestRate()
	NIFA_LOAN_PERCENTAGE_AMOUNT = userInputHandler.getNifaLoanPercentageAmount()
	nifaLoanTimeDuration = userInputHandler.getNifaLoanTimeDuration()

	if (
		(
			NIFA_INTEREST_RATE != None or 
			NIFA_LOAN_PERCENTAGE_AMOUNT != None or 
			nifaLoanTimeDuration != None
		) and
		(
			NIFA_INTEREST_RATE == None or
			NIFA_LOAN_PERCENTAGE_AMOUNT == None or
			nifaLoanTimeDuration == None 
		)
	):
		Output.printErrorMessage("Nifa interest rate, loan percentage amount, and loan time duration (term) must be all specified or none specified.")
		exit(1)

	# Display a disclaimer that this
	# program is not expert financial
	# advice: it is a rough estimation.
	Output.printWarningMessage("This program is not expert financial advice: it is an estimation based off of your input. Please refer to an expert financial advisor before finalizing any loans pertinent hereto.")

	# Perform a bit of extra parsing for timeDuration:
	if timeDuration[-1] != 'm':
		# Remove last char if
		# not numeric:
		timeDuration = int(timeDuration[:-1] if not timeDuration[-1].isnumeric() else timeDuration)

		# Treat it as a year and
		# convert to month:
		timeDuration *= 12

	# Do ditto ^ for NIFA time duration (if applicable):
	if (
		nifaLoanTimeDuration != None and
		nifaLoanTimeDuration != 'm'
	):
		nifaLoanTimeDuration = int(nifaLoanTimeDuration[:-1] if not nifaLoanTimeDuration[-1].isnumeric() else nifaLoanTimeDuration)
		nifaLoanTimeDuration *= 12

	financesHelper = FinancesCalculator()

	MONTHLY_MORTGAGE_PAYMENT = financesHelper.calculateMonthlyMortgagePayment(
		interestRate = INTEREST_RATE,
		totalLoanAmount = SALE_PRICE - DOWN_PAYMENT,
		termInMonths = timeDuration
	)

	# Account for additional principle payment (if applicable):
	if ADDITIONAL_MONTHLY_PRINCIPLE_PAYMENT is not None:
		MONTHLY_MORTGAGE_PAYMENT += ADDITIONAL_MONTHLY_PRINCIPLE_PAYMENT

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

	# Print formatted results:
	redundantEntries = {
		"Sale Price": f"${SALE_PRICE}",
		"Down Payment": f"${DOWN_PAYMENT}",
		"Loan Amount" : f"${str(SALE_PRICE - DOWN_PAYMENT)}",
		"Interest Rate (%)": f"{INTEREST_RATE * 100}%",
		"Time Duration (Term)": f"{timeDuration / 12} years ({timeDuration} months)"
	}

	if PMI is not None:
		redundantEntries["PMI (%)"] = f"{PMI * 100}%"

	entries = {
		"Years Until 80% LTV Is Reached": YEARS_UNTIL_AT_80_PERCENT_LOAN_TO_VALUE_RATIO,
		"Monthly Mortgage Payment": f"${MONTHLY_MORTGAGE_PAYMENT}",
		"Total Interest Paid": f"${TOTAL_INTEREST_PAID}"
	}

	if TOTAL_PMI_PAID is not None:
		entries["Total PMI Paid"] = f"${TOTAL_PMI_PAID}"

	Output.outputFormattedResults(
		entries = entries,
		redundantEntries = redundantEntries
	)

	# Calculate for NIFA (if applicable):
	if NIFA_INTEREST_RATE != None:
		(_, NIFA_TOTAL_INTEREST_PAID) = financesHelper.calculateYearsUntil80LtvAndTotalInterest(
			interestRate = NIFA_INTEREST_RATE,
			totalLoanAmount = SALE_PRICE * NIFA_LOAN_PERCENTAGE_AMOUNT,
			salePrice = SALE_PRICE,
			termInMonths = nifaLoanTimeDuration,
			additionalPrinciplePayment = 0.0
		)

		# Print formatted results:
		redundantEntries = {
			"NIFA Loan Amount (%)": f"{NIFA_LOAN_PERCENTAGE_AMOUNT * 100}%",
			"NIFA Loan Amount ($)": f"${NIFA_LOAN_PERCENTAGE_AMOUNT * SALE_PRICE}",
			"NIFA Loan Duration (Term)(Years)": f"{nifaLoanTimeDuration / 12} years ({nifaLoanTimeDuration} months)",
			"NIFA Loan Interest Rate (%)": f"{NIFA_INTEREST_RATE * 100}%"
		}

		entries = {
			"NIFA Total Interest Paid ($)": f"${NIFA_TOTAL_INTEREST_PAID}"
		}

		Output.printLineBreak()

		Output.outputFormattedResults(
			entries = entries,
			redundantEntries = redundantEntries
		)