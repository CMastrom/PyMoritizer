"""
	Helper class for making various 
	financial calculations.
"""

class FinancesCalculator:
	"""
		Calculates the monthly mortgage payment.

		Formula: (Pv * R) / (1 - (1 + R)^-n)
	"""
	def calculateMonthlyMortgagePayment(
		self: object,
		interestRate: float,
		totalLoanAmount: float,
		termInMonths: int
	) -> float:
		periodicInterestRate = interestRate / 12
		return (totalLoanAmount * periodicInterestRate) / (1 - pow(1 + periodicInterestRate, -float(termInMonths)))

	"""
		Calculates how many years until the
		homebuyer is at 80% LTV (Loan-To-Value ratio).

		NOTE: This is calculating based off of a standard
		amoritized schedule. It iterates through each month
		and calculates how much principle is left thereafter. 
		Once it hits 20% paid in principle, then it returns that
		year corresponding to the month.
	"""
	def calculateYearsUntil80LtvAndTotalInterest(
		self: object,
		interestRate: float,
		totalLoanAmount: float,
		salePrice: float,
		termInMonths: int,
		additionalPrinciplePayment: float = None,
		monthlyMortgagePayment: float = None
	) -> tuple:
		if monthlyMortgagePayment is None:
			monthlyMortgagePayment = self.calculateMonthlyMortgagePayment(
				interestRate = interestRate,
				totalLoanAmount = totalLoanAmount,
				termInMonths = termInMonths
			)

		if additionalPrinciplePayment is None:
			additionalPrinciplePayment = 0.0

		eightyPercentLtv = salePrice * 0.80
		principleLeft = totalLoanAmount
		currentMonthInterest = None # Just initialize
		totalInterestPaid = 0.0
		yearsUntil80Ltv = 0.0

		for month in range(termInMonths):
			currentMonthInterest = (principleLeft * interestRate) / 12
			totalInterestPaid += currentMonthInterest
			principlePaid = monthlyMortgagePayment - currentMonthInterest

			principleLeft -= principlePaid + additionalPrinciplePayment

			if (
				principleLeft <= eightyPercentLtv and 
				yearsUntil80Ltv == 0.0
			):
				yearsUntil80Ltv = float(month + 1) / 12.0

			if (
				principleLeft <= 0
			):
				if yearsUntil80Ltv == 0.0:
					yearsUntil80Ltv = float(termInMonths)
					
				break

		# Default's to 0 years:
		return (yearsUntil80Ltv, totalInterestPaid)

	""" 
		Calculate how much PMI would be paid
		in total before getting to 0% PMI (i.e.,
		80% LTV).
	"""
	def calculateTotalPmiPaid(
		self: object,
		pmi: float,
		salePrice: float,
		downPayment: float,
		yearsUntil80PercentLtv: float
	) -> float:
		pmiAnnualPremium = float(salePrice - downPayment) * pmi
		return pmiAnnualPremium * yearsUntil80PercentLtv