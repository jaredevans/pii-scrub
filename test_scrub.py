import re
import pytest

# Import scrub_text from your scrub.py
from scrub import scrub_text

@pytest.mark.parametrize("text,expected", [
    # Address
    ("Send mail to 123 Main St, Springfield, IL 62704.", "Send mail to [ADDRESS]."),
    ("Home Address: 1234 Elm Drive, Springfield, IL 62701", "Home Address: [ADDRESS]"),
    # Date
    ("Birthday: 12/31/1980", "Birthday: [DATE]"),
    ("The event is on Jan 2, 2022.", "The event is on [DATE]."),
    ("Invoice date: 2022-09-30", "Invoice date: [DATE]"),
    # SSN
    ("SSN: 123-45-6789", "SSN: [SSN]"),
    # Phone
    ("Call me at (555) 987-6543", "Call me at [PHONE]"),
    ("Mobile: 555-123-4567", "Mobile: [PHONE]"),
    # Email
    ("Email me at john.doe@gmail.com", "Email me at [EMAIL]"),
    # Social Media Handle (with and without space)
    ("Follow us @CoolCompany", "Follow us [SM]"),
    ("Find us at  @CoolCompany", "Find us at  [SM]"),
    # Money
    ("Amount: $27,450.00", "Amount: [MONEY]"),
    # IP Address
    ("Server IP: 192.168.1.100", "Server IP: [IP]"),
    # MAC Address
    ("MAC: AA:BB:CC:DD:EE:FF", "MAC: [MAC]"),
    # Credit Card
    ("CC: 4111-1111-1111-1111", "CC: [CREDIT_CARD]"),
    ("Card: 5500-0000-0000-0004", "Card: [CREDIT_CARD]"),
    # Password Inline
    ("Password: Hunter2", "Password: [PASSWORD]"),
    # Password Next Line
    ("Password:\nLetMeIn", "Password: [PASSWORD]"),
    # Password w/ blank line after (should NOT scrub blank)
    ("Password:\n\nSuperSecret", "Password: [PASSWORD]"),
    # Names
    ("Contact: Robert Smith", "Contact: [NAME]"),
    ("Contact: Dr. Emily Carter", "Contact: Dr. [NAME]"),
    # Alphanumeric words with letters and digits (no symbols)
    ("Username: UC123456", "Username: [DIGITS]"),
    ("Student ID: S20231234", "Student ID: [DIGITS]"),
    ("Field: abc123", "Field: [DIGITS]"),
    # Alphanumeric + symbol ([REDACTED])
    ("VPN Login: pa$word987", "VPN Login: [REDACTED]"),
    ("Token: Abc123!", "Token: [REDACTED]"),
    ("Someword: Hello1!", "Someword: [REDACTED]"),
    ("Mix123word", "[DIGITS]"),  # Just digits+letters, no symbol
    ("!!abc", "!!abc"),            # Only symbol
    ("word!", "word!"),            # Only symbol
    ("word123", "[DIGITS]"),        # Only digits+letters, should get [DIGITS]
    # All remaining digit sequences
    ("Routing Number: 123456789", "Routing Number: [DIGITS]"),
])
def test_scrub_cases(text, expected):
    """Test various PII cases are scrubbed."""
    assert scrub_text(text).strip() == expected.strip()

def test_large_example():
    """Test the big example input (basic check, spot-checking tokens)."""
    example = """
    Subject: Payment & Contract Confirmation – Invoice INV-2023-0456

    To: Accounts Payable Team
    From: Dr. Emily Carter (emily.carter@university.edu)
    Date: 2023-10-02

    Vendor Name: ABC Facilities Management
    Contact Name: Robert Smith
    Contact Email: robert.smith@abcfacilities.com
    Contact Phone: (555) 987-6543
    Vendor Address:
    456 Industrial Road, Suite 300
    Springfield, IL 62704
    Vendor Tax ID (EIN): 12-3456789
    Vendor Bank Account: 987654320123
    """
    scrubbed = scrub_text(example)
    # Spot checks
    assert '[NAME]' in scrubbed
    assert '[EMAIL]' in scrubbed
    assert '[ADDRESS]' in scrubbed
    assert '[PHONE]' in scrubbed
    assert '[SSN]' not in scrubbed  # SSN is not in this sample
    assert '[DIGITS]' in scrubbed or '[MONEY]' in scrubbed or '[DATE]' in scrubbed

def test_password_blank_line():
    """Passwords with blank lines after should be scrubbed."""
    txt = "Password:\n\nSuperSecret"
    scrubbed = scrub_text(txt)
    # Should only scrub the line immediately after "Password:", blank lines should be skipped
    assert "Password:" in scrubbed
    assert "[PASSWORD]" in scrubbed

def test_no_false_positives():
    """Should not scrub the word 'password' as a name or common English phrases."""
    txt = "Reset your password by clicking here."
    out = scrub_text(txt)
    assert "password" in out.lower()

def test_does_not_scrub_inside_token():
    """Should not replace things inside [TOKEN] brackets."""
    txt = "Contact: [EMAIL]"
    out = scrub_text(txt)
    assert out == txt

# Add more edge cases as you need!

if __name__ == "__main__":
    pytest.main([__file__])

