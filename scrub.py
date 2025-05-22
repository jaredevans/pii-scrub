import re
import spacy

nlp = spacy.load("en_core_web_sm")

# Address patterns
ADDRESS_PATTERNS = [
    re.compile(
        r'^[ \t]*[\w\d\s\.,#\-]+?\n[ \t]*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?',
        re.MULTILINE
    ),
    re.compile(
        r'\b\d{1,5}\s+([A-Z][a-z]*\s){0,4}'
        r'(Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Parkway|Pkwy|Place|Pl|Lane|Ln)'
        r'(?:,? [A-Z][a-z]+)*,? [A-Z]{2,}\s\d{5}(-\d{4})?\b',
        re.MULTILINE
    ),
    re.compile(
        r'\d{1,5}\s[\w\s]+,\s*[A-Z][a-z]+,?\s+[A-Z]{2}\s+\d{5}(?:-\d{4})?',
        re.MULTILINE
    )
]

# Date patterns
DATE_PATTERNS = [
    re.compile(r'\b\d{2}/\d{2}/\d{4}\b'),                        # 12/31/2022
    re.compile(r'\b\d{4}-\d{2}-\d{2}\b'),                        # 2022-12-31
    re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2}, \d{4}\b', re.IGNORECASE),  # Jan 1, 2022
    re.compile(r'\b\d{1,2}[ -](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[ -]\d{4}\b', re.IGNORECASE), # 31 Dec 2022
    re.compile(r'\b\d{1,2}/\d{1,2}\b'),  # MM/DD or M/D (should be last!)
]

# SSN
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

# Phone
PHONE_PATTERN = re.compile(
    r'(?<!\d)(\(?\d{3}\)?[\s\-\.]?\d{3}[\-\.]?\d{4})(?!\d)',
    re.MULTILINE
)

# Email
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')

# Social media handles (words starting with @)
SOCIAL_MEDIA_PATTERN = re.compile(r'(^|\s)@[A-Za-z0-9_]+\b')


# Monetary value
MONEY_PATTERN = re.compile(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\$\d+')

# IP address (IPv4 only)
IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# MAC address
MAC_PATTERN = re.compile(r'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b')

# Credit card pattern
CREDIT_CARD_PATTERN = re.compile(
    r'(?<!\d)(?:'
    r'(?:\d{4}[-\s]?){3}\d{4}'      # 16 digits, possible dashes/spaces
    r'|'
    r'\d{4}[-\s]?\d{6}[-\s]?\d{5}'  # AMEX 15 digits, possible dashes/spaces
    r'|'
    r'\d{16}'                       # 16 digits, no separators
    r'|'
    r'\d{15}'                       # 15 digits, no separators
    r')(?!\d)'
)

# Long digit sequences (8+)
DIGIT_SEQUENCE_PATTERN = re.compile(r'\b\d{8,}\b')

# Password patterns
PASSWORD_INLINE_PATTERN = re.compile(
    r'(?i)(Password|Passcode|Pwd|Temporary Password|Temp Password|Temp Pwd|Temp Pass)\s*[:=]\s*([^\n]+)'
)
PASSWORD_NEXTLINE_PATTERN = re.compile(
    r'(?i)(Password|Passcode|Pwd|Temporary Password|Temp Password|Temp Pwd|Temp Pass)\s*[:=]?\s*\n([^\n]+)'
)

# Alphanumeric words containing both letters and digits
ALNUM_MIXED_PATTERN = re.compile(r'\b(?=\w*[A-Za-z])(?=\w*\d)\w+\b')

# All digit sequences (used at the end)
ALL_DIGITS_PATTERN = re.compile(r'\b\d+\b')

def password_inline_replacer(match):
    return f"{match.group(1)}: [PASSWORD]"

def password_nextline_replacer(match):
    return f"{match.group(1)}:\n[PASSWORD]"

def is_inside_token(text, start, end):
    """Check if a span is already inside a [TOKEN] like [EMAIL], [ADDRESS], etc."""
    before = text[max(0, start-1):start]
    after = text[end:end+1]
    return before == "[" and after == "]"

def scrub_text(text):
    # 0. Password (inline, e.g. Password: value)
    text = PASSWORD_INLINE_PATTERN.sub(password_inline_replacer, text)
    # 0.5 Password (next line, e.g. Password:\nvalue)
    text = PASSWORD_NEXTLINE_PATTERN.sub(password_nextline_replacer, text)
    # 1. Street Address (multiline first)
    for addr_re in ADDRESS_PATTERNS:
        text = addr_re.sub('[ADDRESS]', text)
    # 2. Date (all formats)
    for date_re in DATE_PATTERNS:
        text = date_re.sub('[DATE]', text)
    # 3. SSN
    text = SSN_PATTERN.sub('[SSN]', text)
    # 4. Phone
    text = PHONE_PATTERN.sub('[PHONE]', text)
    # 5. Email
    text = EMAIL_PATTERN.sub('[EMAIL]', text)
    # 5.5 Social media handles
    text = SOCIAL_MEDIA_PATTERN.sub(lambda m: f"{m.group(1)}[SM]", text)

    # 6. Monetary value
    def money_replacer(match):
        start, end = match.span()
        if is_inside_token(text, start, end):
            return match.group(0)
        return '[MONEY]'
    text = MONEY_PATTERN.sub(money_replacer, text)
    # 7. IP address
    def ip_replacer(match):
        start, end = match.span()
        if is_inside_token(text, start, end):
            return match.group(0)
        return '[IP]'
    text = IP_PATTERN.sub(ip_replacer, text)
    # 8. MAC address
    def mac_replacer(match):
        start, end = match.span()
        if is_inside_token(text, start, end):
            return match.group(0)
        return '[MAC]'
    text = MAC_PATTERN.sub(mac_replacer, text)
    # 9. Credit card
    def cc_replacer(match):
        start, end = match.span()
        if is_inside_token(text, start, end):
            return match.group(0)
        return '[CREDIT_CARD]'
    text = CREDIT_CARD_PATTERN.sub(cc_replacer, text)
    # 11. Name (spaCy), but skip matches inside [TOKEN]
    doc = nlp(text)
    names = sorted(set(ent.text for ent in doc.ents if ent.label_ == "PERSON"), key=len, reverse=True)
    for name in names:
        if name.strip().lower() == "password":
            continue  # Don't replace the word "password"
        if name.strip().lower() == "email":
            continue  # Don't replace the word "email"
        pattern = re.compile(re.escape(name), re.IGNORECASE)
        matches = list(pattern.finditer(text))
        new_text = []
        last_idx = 0
        for m in matches:
            start, end = m.span()
            if not is_inside_token(text, start, end):
                new_text.append(text[last_idx:start])
                new_text.append('[NAME]')
                last_idx = end
        new_text.append(text[last_idx:])
        text = ''.join(new_text)
    # 12. Scrub all alphanumeric words with both letters and digits
    text = ALNUM_MIXED_PATTERN.sub('[DIGITS]', text)
    # 13. Scrub ALL remaining digit sequences
    text = ALL_DIGITS_PATTERN.sub('[DIGITS]', text)
    return text

if __name__ == "__main__":
    input_text = """Subject: Payment & Contract Confirmation – Invoice INV-2023-0456

To: Accounts Payable Team
From: Dr. Emily Carter (emily.carter@university.edu)
Date: 2023-10-02

1. Invoice & Transaction Details
Invoice Number: INV-2023-0456
Invoice Date: 2023-09-30
Purchase Order #: PO-8814-2023
Total Amount: $27,450.00
Payment Due: 2023-10-15

2. Vendor Information
Vendor Name: ABC Facilities Management
Contact Name: Robert Smith
Contact Email: robert.smith@abcfacilities.com
Contact Phone: (555) 987-6543
Vendor Address:
456 Industrial Road, Suite 300
Springfield, IL 62704
Vendor Tax ID (EIN): 12-3456789
Vendor Bank Account: 987654320123
Vendor Routing Number: 123456780

3. University Contact
Representative: Dr. Emily Carter
University Email: emily.carter@university.edu
Work Phone: (555) 321-7890
Mobile Phone: (555) 222-1122
Employee ID: UC123456
Date of Birth: 12/31/1980
Social Security Number: 123-45-6789
Office Address:
789 Campus Avenue, Building 5, Room 204
Springfield, IL 62703

4. Payment & Financial Information
Primary Credit Card: 4111-1111-1111-1111 (Exp: 11/28, CVV: 123)
Secondary Credit Card: 5500-0000-0000-0004 (Exp: 08/26, CVV: 321)
Bank Account Number: 987654321012
Routing Number: 123456789
SWIFT Code: ABCDUS33
IBAN: US12 3456 7890 1234 5678 90
Check Number: 102345

5. Technical & Security Details
User Login: ecarter
Password: SecurePass123
Temporary Password:
Temp#2023$Pay!
IP Address: 192.168.1.100
Alternate IP: 10.0.0.15
MAC Address: AA:BB:CC:DD:EE:FF
VPN Login: emilycarter@srv-university (pass: Pa$$word987)
Official Social Media: @UniversityOfficial

6. Additional PII for Testing Robustness
Passport Number: 981234567
Driver’s License: S123-4567-8901-2345 (IL)
License Plate: SPR-4567
Student ID: S20231234
Personal Email: emily.carter@gmail.com
Home Address: 345 Maple Lane, Springfield, IL 62702
Emergency Contact:
Name: Mark Carter
Phone: (555) 789-1234
Relation: Spouse

7. Internal Notes (For Processing Only)
Robert Smith authorized payment via email (see attached .eml)
Dr. Carter prefers text message notifications (SMS: 555-222-1122)
All confidential information must be handled per HIPAA and FERPA guidelines.

# Test password with blank line after
Password:

SuperSecretShouldNotBeScrubbed

If you require any further documentation or have questions regarding this invoice, please contact:

Dr. Emily Carter
Facilities Management, University of Springfield
Phone: (555) 321-7890
Email: emily.carter@university.edu
"""
    print("Original text:\n")
    print(input_text)
    print("\n###########\n")
    scrubbed = scrub_text(input_text)
    print("Scrubbed text:\n")
    print(scrubbed)
