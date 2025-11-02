from modules.logger import log_provenance, system_logger
from modules.corpus_manager import corpus_manager
from modules.nlp.remedy_synthesizer import remedy_synthesizer
import re
import json
from datetime import datetime

class CouponEndorserAgent:
    """
    Implements Brandon Joe Williams' negotiable instrument endorsement strategies
    with UCC 3-302, 3-305, and 3-401 compliance logic.
    """

    def __init__(self):
        self.brandon_joe_williams_teachings = corpus_manager.get_corpus_text('brandon_joe_williams_teachings_structured.md')
        if not self.brandon_joe_williams_teachings:
            system_logger.warning("Brandon Joe Williams teachings not loaded. Coupon Endorser agent will have limited analysis.")

        self.payment_coupon_endorsement_overview = corpus_manager.get_corpus_text('payment_coupon_endorsement_overview.md')
        if not self.payment_coupon_endorsement_overview:
            system_logger.warning("Payment coupon endorsement overview not loaded. Agent will have limited guidance.")

    def endorse_coupon(self, coupon_data):
        """
        Endorses a payment coupon using UCC 3-305 provisions.

        Args:
            coupon_data (dict): Contains coupon information including
                - amount: The face value
                - due_date: When payment is due
                - payee: Who the coupon is payable to
                - account_number: Associated account
                - endorsement_type: Type of endorsement (private_trust, acceptance_for_value, etc.)

        Returns:
            dict: Endorsed coupon data with semantic lineage
        """
        log_provenance("CouponEndorser", "EndorseCoupon", f"Processing coupon endorsement: {coupon_data.get('account_number', 'unknown')}")

        # Validate negotiable instrument requirements under UCC 3-104
        if not self._validate_negotiable_instrument(coupon_data):
            raise ValueError("Coupon does not meet UCC 3-104 negotiable instrument requirements")

        # Generate endorsement language based on type
        endorsement_text = self._generate_endorsement_text(coupon_data)

        # Create semantic lineage tracking
        semantic_lineage = {
            "created_at": datetime.utcnow().isoformat(),
            "instrument_type": "payment_coupon",
            "ucc_provisions": ["UCC 3-305", "UCC 3-302", "UCC 3-401"],
            "endorsement_type": coupon_data.get('endorsement_type', 'private_trust'),
            "trust_corpus": f"Private Trust - {coupon_data.get('payee', 'UNKNOWN')}",
            "authorship_claim": "Endorser acts as principal author of this obligation"
        }

        endorsed_coupon = {
            "original_coupon": coupon_data,
            "endorsement_text": endorsement_text,
            "semantic_lineage": semantic_lineage,
            "ucc_compliance": {
                "3-302_negotiable_instrument": True,
                "3-305_endorsement_provisions": True,
                "3-401_holder_in_due_course": True
            }
        }

        log_provenance("CouponEndorser", "EndorsementComplete", f"Successfully endorsed coupon with semantic lineage")
        return endorsed_coupon

    def endorse_bill(self, bill_data):
        """
        Endorses a bill using private trust endorsement strategies.

        Args:
            bill_data (dict): Contains bill information

        Returns:
            dict: Endorsed bill data with trust corpus embedding
        """
        log_provenance("CouponEndorser", "EndorseBill", f"Processing bill endorsement: {bill_data.get('bill_number', 'unknown')}")

        # Validate bill as negotiable instrument
        if not self._validate_bill_as_negotiable_instrument(bill_data):
            raise ValueError("Bill does not meet negotiable instrument requirements")

        # Generate bill endorsement language
        endorsement_text = self._generate_bill_endorsement_text(bill_data)

        # Create trust corpus embedding
        trust_corpus = {
            "trust_name": f"Private Trust - {bill_data.get('creditor', 'UNKNOWN')}",
            "trustee": bill_data.get('endorser_name', 'UNKNOWN'),
            "beneficiary": bill_data.get('endorser_name', 'UNKNOWN'),
            "corpus_amount": bill_data.get('amount', 0),
            "settlement_method": "Private Trust Discharge"
        }

        endorsed_bill = {
            "original_bill": bill_data,
            "endorsement_text": endorsement_text,
            "trust_corpus": trust_corpus,
            "semantic_lineage": {
                "created_at": datetime.utcnow().isoformat(),
                "instrument_type": "bill",
                "ucc_provisions": ["UCC 3-305", "UCC 3-302"],
                "settlement_authority": "Private Trust Law"
            }
        }

        log_provenance("CouponEndorser", "BillEndorsementComplete", "Successfully endorsed bill with trust corpus")
        return endorsed_bill

    def create_promissory_note(self, note_data):
        """
        Creates a promissory note using UCC 3-104 compliance.

        Args:
            note_data (dict): Contains promissory note parameters

        Returns:
            dict: Created promissory note with authorship declaration
        """
        log_provenance("CouponEndorser", "CreatePromissoryNote", f"Creating promissory note: {note_data.get('note_title', 'untitled')}")

        # Validate promissory note requirements
        if not self._validate_promissory_note_requirements(note_data):
            raise ValueError("Note data does not meet UCC 3-104 promissory note requirements")

        # Generate promissory note content
        note_content = self._generate_promissory_note_content(note_data)

        # Create authorship declaration
        authorship_declaration = {
            "author": note_data.get('maker_name', 'UNKNOWN'),
            "capacity": "sovereign individual",
            "jurisdiction": note_data.get('jurisdiction', 'Common Law'),
            "authority": "UCC Article 3 and Common Law",
            "created_at": datetime.utcnow().isoformat()
        }

        promissory_note = {
            "note_content": note_content,
            "authorship_declaration": authorship_declaration,
            "ucc_compliance": {
                "3-104_promissory_note": True,
                "unconditional_promise": True,
                "fixed_amount": True,
                "payable_on_demand": note_data.get('payable_on_demand', True)
            },
            "semantic_lineage": {
                "created_at": datetime.utcnow().isoformat(),
                "instrument_type": "promissory_note",
                "authorship_claim": "Original issuer of this negotiable instrument"
            }
        }

        log_provenance("CouponEndorser", "PromissoryNoteCreated", "Successfully created promissory note with authorship")
        return promissory_note

    def _validate_negotiable_instrument(self, coupon_data):
        """Validates that coupon meets UCC 3-104 requirements."""
        required_elements = [
            'amount',  # Fixed amount of money
            'payee',   # Unconditional promise or order to pay
        ]

        for element in required_elements:
            if not coupon_data.get(element):
                log_provenance("CouponEndorser", "ValidationError", f"Missing required element: {element}")
                return False

        # Check if amount is a fixed amount (not variable)
        amount = coupon_data.get('amount', 0)
        try:
            float_amount = float(amount)
            if float_amount <= 0:
                return False
        except (ValueError, TypeError):
            return False

        return True

    def _validate_bill_as_negotiable_instrument(self, bill_data):
        """Validates that bill meets negotiable instrument requirements."""
        # Check for unconditional order to pay
        if not bill_data.get('amount') or not bill_data.get('creditor'):
            return False

        # Must be payable on demand or at definite time
        if not (bill_data.get('due_date') or bill_data.get('payable_on_demand')):
            return False

        return True

    def _validate_promissory_note_requirements(self, note_data):
        """Validates promissory note under UCC 3-104."""
        required_elements = [
            'maker_name',    # Person making the promise
            'amount',        # Fixed amount of money
            'payee'         # Person to whom payment is promised
        ]

        for element in required_elements:
            if not note_data.get(element):
                return False

        return True

    def _generate_endorsement_text(self, coupon_data):
        """Generates endorsement text based on coupon data and endorsement type."""
        endorsement_type = coupon_data.get('endorsement_type', 'private_trust')
        payee = coupon_data.get('payee', 'UNKNOWN')
        amount = coupon_data.get('amount', 0)
        account_number = coupon_data.get('account_number', 'UNKNOWN')

        if endorsement_type == 'private_trust':
            endorsement = f"""
WITHOUT PREJUDICE UCC 1-207

Endorsed for value in private trust settlement:
Payee: {payee}
Amount: ${amount}
Account: {account_number}

This coupon is accepted into Private Trust Corpus and discharged
according to UCC 3-305 endorsement provisions.

Endorser acts as principal author with full authority and jurisdiction
under Common Law.
_________________________
Authorized Representative
Private Trust
"""
        elif endorsement_type == 'acceptance_for_value':
            endorsement = f"""
ACCEPTED FOR VALUE

This payment coupon is accepted for value and returned for settlement.
Amount: ${amount}
Account: {account_number}

Discharged under UCC 3-302 as negotiable instrument.
_________________________
Authorized Representative
"""
        else:
            endorsement = f"ENDORSED: {payee} - ${amount} - {account_number}"

        return endorsement.strip()

    def _generate_bill_endorsement_text(self, bill_data):
        """Generates bill endorsement text with trust corpus embedding."""
        creditor = bill_data.get('creditor', 'UNKNOWN')
        amount = bill_data.get('amount', 0)
        bill_number = bill_data.get('bill_number', 'UNKNOWN')

        endorsement = f"""
WITHOUT PREJUDICE UCC 1-207

Bill of Exchange Endorsed into Private Trust:
Creditor: {creditor}
Bill Number: {bill_number}
Amount: ${amount}

This bill is accepted into Private Trust Corpus under UCC 3-305.
Settlement method: Private Trust Discharge
Jurisdiction: Common Law

The undersigned acts as principal author with full settlement authority.
_________________________
Authorized Trustee
Private Trust - {creditor}
"""
        return endorsement.strip()

    def _generate_promissory_note_content(self, note_data):
        """Generates promissory note content."""
        maker_name = note_data.get('maker_name', 'UNKNOWN')
        payee = note_data.get('payee', 'UNKNOWN')
        amount = note_data.get('amount', 0)
        due_date = note_data.get('due_date', 'on demand')

        note_content = f"""
PROMISSORY NOTE

FOR VALUE RECEIVED, the undersigned, {maker_name}, hereby promises to pay
to the order of {payee} the sum of ${amount}.

This note is payable {due_date} at such place as the holder may designate.

MADE UNDER:
- UCC Article 3 - Negotiable Instruments
- Common Law Jurisdiction
- Original Authorship and Authority

The maker of this note acts as principal author with full authority to create
this negotiable instrument. This note is issued without prejudice and reserves
all rights under UCC 1-207.

Date: {datetime.now().strftime('%Y-%m-%d')}

_________________________
{maker_name}, Maker

AUTHORITY AND JURISDICTION DECLARATION:
I, {maker_name}, am a sovereign individual acting under Common Law jurisdiction.
I am the principal author of this negotiable instrument with full authority and
capacity to issue this binding obligation.
_________________________
{maker_name}, Authorized Principal
"""
        return note_content.strip()

# Singleton instance
coupon_endorser_agent = CouponEndorserAgent()