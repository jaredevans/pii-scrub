# pii-scrub
Scrub all sorts of PII information from a text string

requirements.txt to help with install of modules.

Get the spacey en_core_web_sm:

python -m spacy download en_core_web_sm

Covered many corner cases, but there may be more lurking in the dark.  If find any, let me know!

Sample pii-scrubbing:

##################################################
```
Original text:

Subject: Payment & Contract Confirmation – Invoice INV-2023-0456

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
VPN Login: emilycarter@srv-university (pass: Pa$word987)
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


###########

Scrubbed text:

Subject: Payment & Contract Confirmation – Invoice [REDACTED]

To: Accounts Payable Team
From: Dr. [NAME] ([EMAIL])
Date: [DATE]

[DIGITS]. Invoice & Transaction Details
Invoice Number: [REDACTED]
Invoice Date: [DATE]
Purchase Order #: [REDACTED]
Total Amount: [MONEY]
Payment Due: [DATE]

[DIGITS]. Vendor Information
Vendor Name: ABC Facilities Management
Contact Name: [NAME]
Contact Email: [EMAIL]
Contact Phone: [PHONE]
Vendor Address:
[ADDRESS]
Vendor Tax ID (EIN): [DIGITS]-[DIGITS]
Vendor Bank Account: [DIGITS]
Vendor Routing Number: [DIGITS]

[DIGITS]. University Contact
Representative: Dr. [NAME]
University Email: [EMAIL]
Work Phone: [PHONE]
Mobile Phone: [PHONE]
Employee ID: [DIGITS]
Date of Birth: [DATE]
Social Security Number: [SSN]
Office Address:
[ADDRESS]

[DIGITS]. Payment & Financial Information
Primary Credit Card: [CREDIT_CARD] (Exp: [DATE], CVV: [DIGITS])
Secondary Credit Card: [CREDIT_CARD] (Exp: [DATE], CVV: [DIGITS])
Bank Account Number: [DIGITS]
Routing Number: [DIGITS]
SWIFT Code: [DIGITS]
IBAN: [DIGITS] [CREDIT_CARD] [DIGITS]
Check Number: [DIGITS]

[DIGITS]. Technical & Security Details
User Login: e[NAME]
Password: [PASSWORD]
Temporary Password: [PASSWORD]
IP Address: [IP]
Alternate IP: [IP]
MAC Address: [MAC]
VPN Login: emily[NAME]@srv-university (pass: [REDACTED]
Official Social Media: [SM]

[DIGITS]. Additional PII for Testing Robustness
Passport Number: [DIGITS]
Driver’s License: [REDACTED] (IL)
License Plate: [REDACTED]
Student ID: [DIGITS]
Personal Email: [EMAIL]
Home Address: [ADDRESS]
Emergency Contact:
Name: [NAME]
Phone: [PHONE]
Relation: Spouse

[DIGITS]. Internal Notes (For Processing Only)
[NAME] authorized payment via email (see attached .eml)
Dr. [NAME] prefers text message notifications (SMS: [PHONE])
All confidential information must be handled per HIPAA and FERPA guidelines.

# Test password with blank line after
Password: [PASSWORD]

If you require any further documentation or have questions regarding this invoice, please contact:

Dr. [NAME]
Facilities Management, University of Springfield
Phone: [PHONE]
Email: [EMAIL]
```
