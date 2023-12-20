#!/usr/bin/env python3

from UserInput import UserInput
from MortgageCalculator import MortgageCalculator
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
	DESIRED_LTV = userInputHandler.getDesiredLtv()
	PMI = userInputHandler.getPmi() # Optional argument
	ADDITIONAL_MONTHLY_PRINCIPLE_PAYMENT = userInputHandler.getAdditionalMonthlyPrinciplePayment() # Optional argument

	# Make sure that they didn't input the percentage as * 100:
	if DESIRED_LTV > 1 or DESIRED_LTV < 0:
		Output.printErrorMessage("Desired LTV must be in the range [0,1], where 1 is 100%% and 0 is 0%%.")
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

	mortgageHelper = MortgageCalculator(
		downPayment = DOWN_PAYMENT,
		salePrice = SALE_PRICE,
		interestRate = INTEREST_RATE,
		termInMonths = timeDuration
	)

	monthly_mortgage_payment = mortgageHelper.calculateMonthlyMortgagePayment()

	# Account for additional principle payment (if applicable):
	if ADDITIONAL_MONTHLY_PRINCIPLE_PAYMENT is not None:
		monthly_mortgage_payment += ADDITIONAL_MONTHLY_PRINCIPLE_PAYMENT

	(YEARS_UNTIL_DESIRED_LTV, TOTAL_INTEREST_PAID) = mortgageHelper.calculateYearsUntilDesiredLtvAndTotalInterest(
		desiredLTVRatioLeft = DESIRED_LTV,
		additionalPrinciplePayment = ADDITIONAL_MONTHLY_PRINCIPLE_PAYMENT
	)

	total_pmi_paid = None
	if PMI is not None:
		total_pmi_paid = mortgageHelper.calculateTotalPmiPaid(
			pmi = PMI,
			yearsUntil80PercentLtv = YEARS_UNTIL_DESIRED_LTV if DESIRED_LTV == 0.80 else None # if they didn't calculate for 80% LTV, then pass nothing so that it internally performs that calculation
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
		f"Years Until {DESIRED_LTV * 100}% LTV Is Reached": YEARS_UNTIL_DESIRED_LTV,
		"Monthly Mortgage Payment": f"${monthly_mortgage_payment}",
		f"Total Interest Paid By {DESIRED_LTV * 100}% LTV": f"${TOTAL_INTEREST_PAID}"
	}

	if total_pmi_paid is not None:
		entries["Total PMI Paid"] = f"${total_pmi_paid}"

	Output.outputFormattedResults(
		entries = entries,
		redundantEntries = redundantEntries
	)