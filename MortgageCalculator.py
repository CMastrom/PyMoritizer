"""
	Helper class for making various 
	mortgage calculations.
"""

class MortgageCalculator:
	class CommonTermPeriods:
		ThirtyYears = 360
		FifteenYears = 180

	def __init__(
		self: object,
		downPayment: float,
		salePrice: float,
		interestRate: float,
		termInMonths: int
	) -> None:
		# self.downPayment = downPayment
		self.salePrice = salePrice
		self.totalLoanAmount = salePrice - downPayment
		self.interestRate = interestRate
		self.termInMonths = termInMonths

	"""
		Calculates the monthly mortgage payment.

		Formula: (Pv * R) / (1 - (1 + R)^-n)
	"""
	def calculateMonthlyMortgagePayment(
		self: object
	) -> float:
		periodicInterestRate = self.interestRate / 12

		return (self.totalLoanAmount * periodicInterestRate) / (1 - pow(1 + periodicInterestRate, -float(self.termInMonths)))

	"""
		Calculates how many years until the
		homebuyer is at the desired LTV (Loan-To-Value ratio).

		NOTE: This is calculating based off of a standard
		amoritized schedule. It iterates through each month
		and calculates how much principle is left thereafter. 
		Once it hits desired amount paid in principle, then it returns that
		year corresponding to the month.
	"""
	def calculateYearsUntilDesiredLtvAndTotalInterest(
		self: object,
		desiredLTVRatioLeft: float,
		additionalPrinciplePayment: float = None,
		monthlyMortgagePayment: float = None
	) -> tuple:
		# If desired LTV is 1, then
		# that is 100% debt, and so
		# the person would have paid
		# no interest yet:
		if desiredLTVRatioLeft == 1:
			return (0.0, 0.0)

		if desiredLTVRatioLeft > 1 or desiredLTVRatioLeft < 0:
			raise Exception("Desired LTV must be in the interval [0,1].")

		if monthlyMortgagePayment is None:
			monthlyMortgagePayment = self.calculateMonthlyMortgagePayment()

		if additionalPrinciplePayment is None:
			additionalPrinciplePayment = 0.0

		percentLTV = self.salePrice * desiredLTVRatioLeft
		principleLeft = self.totalLoanAmount
		currentMonthInterest = None
		totalInterestPaid = 0.0
		yearsUntilLTV = 0.0

		# Edge case where it has already been reached:
		if percentLTV >= principleLeft:
			return (0.0, 0.0)

		for month in range(self.termInMonths + 1):
			currentMonthInterest = (principleLeft * self.interestRate) / 12
			totalInterestPaid += currentMonthInterest
			principlePaid = monthlyMortgagePayment - currentMonthInterest
			principleLeft -= principlePaid + additionalPrinciplePayment

			if (
				principleLeft <= percentLTV
			):
				yearsUntilLTV = float(month + 1) / 12.0

				break

			if (
				principleLeft <= 0
			):
				if yearsUntilLTV == 0.0:
					yearsUntilLTV = float(self.termInMonths) / 12.0
					
				break

		return (yearsUntilLTV, totalInterestPaid)

	""" 
		Calculate how much PMI would be paid
		in total before getting to 0% PMI (i.e.,
		80% LTV).
	"""
	def calculateTotalPmiPaid(
		self: object,
		pmi: float,
		yearsUntil80PercentLtv: float = None
	) -> float:
		if yearsUntil80PercentLtv is None:
			(yearsUntil80PercentLtv, interestRate) = self.calculateYearsUntilDesiredLtvAndTotalInterest(
				desiredLTVRatioLeft = 0.80
			)

		pmiAnnualPremium = self.totalLoanAmount * pmi

		return pmiAnnualPremium * yearsUntil80PercentLtv