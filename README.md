# pii-scrub
Scrub all sorts of PII information from a text string

requirements.txt to help with install of modules.

Get the spacey en_core_web_sm:

python -m spacy download en_core_web_sm

Covered many corner cases, but there may be more lurking in the dark.  If find any, let me know!

Sample pii-scrubbing:

##################################################

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

4. University Contact
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

5. Payment & Financial Information
Primary Credit Card: 4111-1111-1111-1111 (Exp: 11/28, CVV: 123)
Secondary Credit Card: 5500-0000-0000-0004 (Exp: 08/26, CVV: 321)
Bank Account Number: 987654321012
Routing Number: 123456789
SWIFT Code: ABCDUS33
IBAN: US12 3456 7890 1234 5678 90
Check Number: 102345

6. Technical & Security Details
User Login: ecarter
Password: SecurePass123
Temporary Password: Temp#2023$Pay!
IP Address: 192.168.1.100
Alternate IP: 10.0.0.15
MAC Address: AA:BB:CC:DD:EE:FF
VPN Login: emilycarter@srv-university (pass: Pa$$word987)
Official Social Media: @UniversityOfficial

7. Additional PII for Testing Robustness
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

8. Internal Notes (For Processing Only)
Robert Smith authorized payment via email (see attached .eml)
Dr. Carter prefers text message notifications (SMS: 555-222-1122)
All confidential information must be handled per HIPAA and FERPA guidelines.

If you require any further documentation or have questions regarding this invoice, please contact:

Dr. Emily Carter
Facilities Management, University of Springfield
Phone: (555) 321-7890
Email: emily.carter@university.edu



#################

Scrubbed text:
Subject: Payment & Contract Confirmation – Invoice INV-[NUM_0[NUM_0[NUM_18]]]-[NUM_0[NUM_[NUM_[NUM_29]]]]

To: Accounts Payable Team
From: Dr. [NAME_10] ([EMAIL_01])
Date: [DATE_01]

1. Invoice & Transaction Details
Invoice Number: INV-[NUM_0[NUM_23]]-[NUM_0[NUM_20]]
Invoice Date: [DATE_02]
Purchase Order #: PO-[NUM_0[NUM_46]]-[NUM_0[NUM_53]]
Total Amount: $[NUM_[NUM_3[NUM_45]]],[NUM_09].[NUM_10]
Payment Due: [DATE_03]

2. Vendor Information
Vendor Name: ABC Facilities Management
Contact Name: [NAME_09]
Contact Email: [EMAIL_02]
Contact Phone: [PHONE_01]
Vendor Address:
[NUM_[NUM_15]] Industrial Road, Suite [NUM_13]
Springfield, IL [NUM_14]
Vendor Tax ID (EIN): 12-[NUM_16]
Vendor Bank Account: [NUM_17]
Vendor Routing Number: [SSN_01]

3. University Contact
Representative: Dr. [NAME_08]
University [NAME_07]: [EMAIL_03]
Work Phone: [PHONE_02]
Mobile Phone: [PHONE_03]
Employee ID: UC[NUM_30]456
Date of Birth: [DATE_04]
Social Security Number: [SSN_02]
Office Address:
[NUM_19] Campus Avenue, Building 5, Room [NUM_21]
Springfield, IL [NUM_22]

4. Payment & Financial Information
Primary Credit Card: [NUM_24]-[NUM_25]-[NUM_[NUM_36]]-[NUM_27] (Exp: 11/28, CVV: 123)
Secondary Credit Card: [NUM_31]-[NUM_32]-[NUM_33]-[NUM_34] (Exp: 08/26, CVV: [NUM_37])
Bank Account Number: [NUM_38]
Routing Number: [SSN_03]
SWIFT Code: [SWIFT_01]
IBAN: US12 [NUM_39] [NUM_40] [NUM_41] [NUM_42] [NUM_43]
Check Number: [NUM_44]

5. Technical & Security Details
User Login: ecarter
[NAME_06]: SecurePass123
Temporary Password: [PASSWORD_01]
IP Address: [IP_01]
Alternate IP: [IP_02]
MAC Address: [MAC_01]
VPN Login: emilycarter[SOCIAL_01]-university (pass: Pa$$word987)
Official Social Media: [SOCIAL_02]

6. Additional PII for Testing Robustness
Passport Number: [SSN_04]
Driver’s License: S123-[NUM_47]-[NUM_48]-[NUM_49] (IL)
License Plate: SPR-[NUM_50]
Student ID: S20231234
Personal Email: [EMAIL_04]
Home Address: [NUM_51] [NAME_05], Springfield, IL [NUM_52]
Emergency Contact:
Name: [NAME_04]
Phone: [PHONE_04]
Relation: Spouse

7. Internal Notes (For Processing Only)
[NAME_03] authorized payment via email (see attached .eml)
Dr. [NAME_02] prefers text message notifications (SMS: [PHONE_05])
All confidential information must be handled per HIPAA and FERPA guidelines.

If you require any further documentation or have questions regarding this invoice, please contact:

Dr. [NAME_01]
Facilities Management, University of Springfield
Phone: [PHONE_06]
Email: [EMAIL_05]
