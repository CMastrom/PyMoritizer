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
	YELLOW = "\033[0;93m"
	RED = "\033[0;31m"

	"""
		Prints the output results in 
		a formatted manner.
	"""
	@staticmethod
	def outputFormattedResults(
		entries: dict,
		redundantEntries: dict = None
	) -> None:
		if redundantEntries is not None:
			Output.printRedundantResults(
				redundantEntries = redundantEntries
			)

		Output.printLineBreak()

		Output.printResults(
			results = entries
		)

	"""
		Prints a line break.
	"""
	@staticmethod
	def printLineBreak() -> None:
		print("\n--------------------\n")


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

	"""
		Prints a warning message.
	"""
	@staticmethod
	def printWarningMessage(
		msg: str
	) -> None:
		print(f"{Output.YELLOW}WARNING: {Output.RED}{msg}{Output.RESET}")

	"""
		Prints an error message.
	"""
	@staticmethod
	def printErrorMessage(
		msg: str
	) -> None:
		print(f"{Output.RED}ERROR: {Output.WHITE}{msg}{Output.RESET}")