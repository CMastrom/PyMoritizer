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
	def calculateYearsUntil80Ltv(
		self: object,
		interestRate: float,
		totalLoanAmount: float,
		salePrice: float,
		termInMonths: int,
		monthlyMortgagePayment: float = None
	) -> float:
		if monthlyMortgagePayment is None:
			monthlyMortgagePayment = self.calculateMonthlyMortgagePayment(
				interestRate = interestRate,
				totalLoanAmount = totalLoanAmount,
				termInMonths = termInMonths
			)

		eightyPercentLtv = salePrice * 0.80
		principleLeft = totalLoanAmount
		currentMonthInterest = None # Just initialize

		for month in range(termInMonths):
			currentMonthInterest = (principleLeft * interestRate) / 12
			principlePaid = monthlyMortgagePayment - currentMonthInterest

			principleLeft -= principlePaid

			if principleLeft <= eightyPercentLtv:
				return float(month + 1) / 12.0

		# Default's to 0 years:
		return 0.0