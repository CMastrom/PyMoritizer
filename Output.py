"""
	Handles displaying output in a 
	user friendly way.

	NOTE: May have no to little effect if the
	terminal color doesn't support it.
"""

class Output:
	RESET = "\033[0m"
	WHITE = "\033[0;37m"
	GREEN = "\033[0;32m"
	CYAN = "\033[0;36m"
	BOLD_GREEN = "\033[1;32m"

	"""
		Prints the output results in 
		a formatted manner.
	"""
	@staticmethod
	def outputFormattedResults(
		salePrice: float,
		downPayment: float,
		interestRate: float,
		timeDuration: int,
		monthlyMortgagePayment: float,
		yearsUntil80Ltv: float,
		pmi: float = None
	) -> None:
		redundantEntries = {
			"Sale Price": salePrice,
			"Down Payment": downPayment,
			"Loan Amount" : salePrice - downPayment,
			"Interest Rate": interestRate,
			"Time Duration (Term)": timeDuration
		}

		if pmi is not None:
			redundantEntries["PMI (%)"] = pmi

		Output.printRedundantResults(
			redundantEntries = redundantEntries
		)

		print("\n--------------------\n")

		Output.printResults(
			results = {
				"Years Until 80% LTV Is Reached": yearsUntil80Ltv,
				"Monthly Mortgage Payment": monthlyMortgagePayment
			}
		)


	"""
		Prints result.
	"""
	@staticmethod
	def printResult(
		resultName: str,
		resultEntry #: any
	) -> None:
		print(f"{Output.BOLD_GREEN}{resultName}: {Output.CYAN}{resultEntry}{Output.RESET}")

	"""
		Prints results.
	"""
	@staticmethod
	def printResults(
		results: dict
	) -> None:
		for (resultName, resultEntry) in results.items():
			Output.printResult(
				resultName = resultName,
				resultEntry = resultEntry
			)

	"""
		Prints redundant entry.
	"""
	@staticmethod
	def printRedundantResult(
		redundantEntryName: str,
		redundantEntry #: any
	) -> None:
		print(f"{Output.GREEN}{redundantEntryName}: {Output.WHITE}{redundantEntry}{Output.RESET}")

	"""
		Prints redundant entries.
	"""
	@staticmethod
	def printRedundantResults(
		redundantEntries: dict
	) -> None:
		for (redundantEntryName, redundantEntry) in redundantEntries.items():
			Output.printRedundantResult(
				redundantEntryName = redundantEntryName,
				redundantEntry = redundantEntry
			)