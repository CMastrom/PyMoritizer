"""
	Handles parsing user arguments
"""

from argparse import ArgumentParser
from sys import exit

class UserInput:
	# For simple type naming:
	NONE_OR_DIE = None

	def __init__(
		self: object
	):
		# For parsing:
		self._parser = ArgumentParser()

		# Guard against accidentally forgetting to initiate arguments:
		self._wasInitiated = False

		# Guard against parsing args multiple times:
		self._wasParsed = False

		# Holds the parsed args:
		self._parsedArgs = None

	"""
		Initiate valid arguments.
	"""
	def initializeUserArguments(
		self: object
	)-> object:
		self._wasInitiated = True

		# NOTE: there's in implied help '-h' flag

		self._parser.add_argument(
			"-s",
			"--sale-price",
			dest="SALEPRICE",
			help="Total price of the house.",
			type=float,
			required=True
		)

		self._parser.add_argument(
			"-d",
			"--down-payment",
			dest="DOWNPAYMENT",
			help="Intended down payment on the house.",
			#action="store_true",
			type=float,
			required=True
		)

		self._parser.add_argument(
			"-i",
			"--interest-rate",
			dest="INTERESTRATE",
			help="Interest rate associated with the mortgage loan. NOTE: do not input percentage but, rather, the float version thereof (e.g., not '5%%' but, rather, '0.05')",
			#action="store_true",
			type=float,
			required=True
		)

		self._parser.add_argument(
			"-t",
			"--time-duration",
			dest="TIMEDURATION",
			help="The duration of time the loan is set for. Use 'm' for months or 'y' for years (e.g., '-d 7m' or '-d 7y'). If no unit is specified, then this defaults to years.",
			#action="store_true",
			type=str,
			required=True
		)

		self._parser.add_argument(
			"-p",
			"--pmi",
			dest="PMI",
			help="The PMI percentage. NOTE: do not input percentage but, rather, the float version thereof (e.g., not '5%%' but, rather, '0.05').",
			#action="store_true",
			type=float
		)

		self._parser.add_argument(
			"-a",
			"--additional-monthly-principle-payment",
			dest="ADDITIONALMONTHLYPRINCIPLEPAYMENT",
			help="An additional principle payment per month.",
			#action="store_true",
			type=float
		)

		# NOTE: The NIFA arguments must all be supplied
		# or none.
		self._parser.add_argument(
			"-nI",
			"--nifa-interest-rate",
			dest="NIFAINTERESTRATE",
			help="The interest rate for the NIFA down payment assistance loan. For calculating the 1st mortgage NIFA loan, just use the other required parameters. NOTE: do not input percentage but, rather, the float version thereof (e.g., not '5%%' but, rather, '0.05'). NOTE: All NIFA arguments must to specified or none.",
			#action="store_true",
			type=float
		)

		self._parser.add_argument(
			"-nP",
			"--nifa-loan-percentage-amount",
			dest="NIFALOANPERCENTAGEAMOUNT",
			help="The percentage of the sale price that will be borrowed for NIFA down payment assistance. For calculating the 1st mortgage NIFA loan, just use the other required parameters. NOTE: do not input percentage but, rather, the float version thereof (e.g., not '5%%' but, rather, '0.05'). NOTE: All NIFA arguments must to specified or none.",
			#action="store_true",
			type=float
		)

		self._parser.add_argument(
			"-nT",
			"--nifa-loan-time-duration",
			dest="NIFALOANTIMEDURATION",
			help="The duration of time (term) for the NIFA down payment assistance loan. Use 'm' for months or 'y' for years (e.g., '-d 7m' or '-d 7y'). If no unit is specified, then this defaults to years. NOTE: All NIFA arguments must to specified or none.",
			#action="store_true",
			type=str
		)

		return self

	"""
		Helper method - check if args were initiated
	"""
	def _makeSureArgsWereInitiated(
		self: object
	) -> NONE_OR_DIE:
		if not self._wasInitiated:
			print("User arguments were never initialized! Terminating.")
			exit(1)

	"""
		Helper method - parse args (if applicable)
	"""
	def _parseArgs(
		self: object
	) -> None:
		if not self._wasParsed:
			self._parsedArgs = vars(self._parser.parse_args())

	""" 
		Handles preliminary work before returning arg result.
	"""
	def _handlePreliminaryWork(
		self: object
	) -> NONE_OR_DIE:
		# Make sure they were initiated:
		self._makeSureArgsWereInitiated() # Could die

		# Parse (if applicable):
		self._parseArgs()

	"""
		Handles retrieving user args
		by mapping unknown `get<arg-name>`
		calls to arg names.
		
		E.g., `getMyArg()` will return user arg
		value for `MYARG`.

		NOTE: will return none if arg doesn't exist
		or format  is incorrect.

		@throws Exception
		@return none | any
	"""
	def __getattr__(
		self: object,
		methodName: str
	):
		# Make sure the args were properly
		# setup to begin with:
		self._handlePreliminaryWork()

		# In order to return anything
		# when attribute is invoked,
		# a wrapper method is required:
		def wrapper():
			# Make sure it matches the format
			# `get<arg-name>`:
			if not methodName.startswith("get"):
				return None

			# Try to obtain that value from
			# argparse:
			try:
				return self._parsedArgs[methodName[3:].upper()]
			except KeyError:
				return None
			except Exception as e:
				raise e

		return wrapper
