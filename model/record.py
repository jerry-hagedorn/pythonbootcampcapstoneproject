import datetime
import enum

VALID_RECORD_TYPES: list = ["ACCEPTANCE LETTER",
    "ADVANCE",
    "AFFIDAVIT",
    "AGREEMENT",
    "AMENDMENT OF FEDERAL TAX LIEN",
    "AMENDMENT OR UCC AMENDMENT",
    "APPOINTMENT",
    "ASSIGNMENT",
    "ASSN DEED OF TRUST/ASSN OF MORTGAGE",
    "BENEFICIARY DEED",
    "BILL OF SALE",
    "BIRTH CERTIFICATE",
    "BOND",
    "CEMETERY DEED",
    "CERTIFICATE",
    "CATTEL MORTGAGE",
    "CONTINUATION OF FNST",
    "CONTRACT FOR DEED",
    "CT ADMIN DEED",
    "DANGEROUS BUILDING NOTICE",
    "DANGEROUS BUILDING RELEASE",
    "DEATH CERTIFICATE",
    "DECREE",
    "DEED",
    "DEED OF TRUST",
    "DEPARTMENT OF JUSTICE LIEN",
    "DURABLE POWER OF ATTORNEY",
    "EASEMENT",
    "EASEMENT & RIGHT OF WAY",
    "EXPUNGE AFFIDAVIT",
    "FEDERAL PENSION LIEN",
    "FEDERAL TAX LIEN",
    "FINAL SETTLEMENT",
    "FINANCING STATEMENT",
    "FORECLOSURE COM DESIG",
    "FORECLOSURE/TRUSTEE'S DEED UNDER FORECLOSURE",
    "INCORPORATION",
    "INTENT TO HOME SCHOOL",
    "INTERNATIONAL MARRIAGE LICENSE",
    "JUDGMENT",
    "LEASE",
    "LEVY/NOTICE",
    "LIEN",
    "LIS PENDEN/NOTICE",
    "MARITAL WAIVER",
    "MEMORANDUM",
    "MERGER",
    "MILITARY DISCHARGE",
    "MISCELLANEOUS",
    "MODIFICATION",
    "MORTGAGE",
    "NOTICE",
    "NOTICE MECHANIC LIEN",
    "OPTION",
    "ORDER",
    "ORDINANCE",
    "PA 2.x DOC TYPE, DO NOT DELETE",
    "PARTIAL EXPUNGE AFFIDAVIT",
    "PARTIAL REL FIN",
    "PARTIAL REL STATE TAX LIEN",
    "PARTIAL REL TAX LIEN",
    "PARTIAL RELEASE",
    "PARTIAL REVOCATION FEDERAL TAX LIEN RELEASE",
    "PARTIAL WITHDRAWAL TAX LIEN",
    "PATENT",
    "PERSONAL REP DEED",
    "PLAT",
    "POWER OF ATTORNEY",
    "PROBATE",
    "PUBLICATION",
    "QUIT CLAIM DEED",
    "RATIFICATION",
    "RELEASE DT/SATIS OF MTG/RECONVEYANCE",
    "RELEASE FEDERAL TAX LIEN",
    "RELEASE FNST",
    "RELEASE JUDGEMENT LIEN",
    "RELEASE LIEN",
    "RELEASE LIS PENDEN",
    "RELEASE MECHANIC LIEN NOTICE",
    "RELEASE OF AGREEMENT",
    "RELEASE OF ASGN & RENTS",
    "RELEASE OF DEPARTMENT OF JUSTICE LIEN",
    "RELEASE OF NOT/LEVY/MOD/CERT",
    "RELEASE STATE TAX LIEN",
    "REMOVAL & APPOINTMENT",
    "REPORT OF COMM",
    "REQUEST",
    "RESTRICTIONS",
    "REV & APPT POWER OF ATTORNEY",
    "REVOCATION",
    "REVOCATION OF POWER OF ATTORNEY",
    "REVOCATION OF TAX LIEN RELEASE",
    "RIGHT OF WAY",
    "SHERIFFS DEED",
    "STATE TAX LIEN",
    "SUBORDINATION",
    "SURVEY",
    "TERMINATION",
    "TRADEMARK",
    "TRANSFER",
    "TRUSTEES DEED",
    "UTILITY",
    "VACANCY/VACATION",
    "VOID",
    "WAIVER",
    "WARRANTY DEED",
    "WILL",
    "WILL & FINAL SETTLEMENT",
    "WITHDRAWAL OF TAX LIEN"
    ]

class Record:

    _county_record_key: str
    _instrument_num: str
    _book: str
    _page: str
    _date_recorded: datetime.date
    _record_type: str
    _grantors: list
    _grantees: list
    _description: str


    def __init__(self, county_record_key: str,  instrument_num: str, date_recorded: datetime.date, record_type: str, book: str ="", page: str ="", grantors: list =None, grantees: list =None, description: str = ""):

        self._county_record_key = county_record_key
        self._instrument_num = instrument_num
        self._date_recorded = date_recorded
        self._record_type = record_type
        self._book = book
        self._page = page
        self._description = description
        if grantors is None:
            self._grantors = []
        else:
            self._grantors = grantors
        if grantees is None:
            self._grantees = []
        else:
            self._grantees = grantees

    def __str__(self):
        return str(vars(self))

    @property
    def get_county_record_key(self):
        return self._county_record_key

    @property
    def get_instrument_num(self):
        return self._instrument_num


    @property
    def get_date_recorded(self):
        return self._date_recorded

    @property
    def get_record_type(self):
        return self._record_type

    @property
    def get_book(self):
        return self._book


    @property
    def get_page(self):
        return self._page


    @property
    def get_grantors(self):
        return self._grantors

    def set_grantors(self, grantors: list):
        self._grantors = grantors

    @property
    def get_grantees(self):
        return self._grantees

    def set_grantees(self, grantees: list):
        self._grantees = grantees

    @property
    def get_description(self):
        return self._description



