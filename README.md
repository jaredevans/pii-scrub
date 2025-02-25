# pii-scrub
Scrub all sorts of PII information from a text string

requirements.txt to help with install of modules.

Get the spacey en_core_web_sm:

python -m spacy download en_core_web_sm

Covered many corner cases, but there may be more lurking in the dark.  If find any, let me know!

Sample pii-scrubbing:

##################################################

Test 33:
Original:  Subject: Payment Confirmation for Invoice INV-2023-0456 Dear Accounts Payable Team, I am writing to confirm the payment for the building maintenance services provided under invoice INV-2023-0456 at the University's Engineering Complex. Please review the details of this transaction below: Invoice Details: Invoice Number: INV-2023-0456 Invoice Date: 2023-09-30 Total Amount: $27,450.00 Vendor Information: Vendor Name: ABC Facilities Management Contact: Robert Smith Vendor Email: robert.smith@abcfacilities.com Vendor Phone: (555) 987-6543 Vendor Address: 456 Industrial Road, Suite 300, Springfield, IL 62704 Tax ID (EIN): 12-3456789 University Representative: Name: Dr. Emily Carter Email: emily.carter@university.edu Phone: 555-321-7890 Office Address: 789 Campus Avenue, Building 5, Room 204, Springfield, IL 62703 Employee ID: UC123456 Date of Birth: 12/31/1980 Social Security Number: 123-45-6789 Payment Information: Primary Credit Card: 4111-1111-1111-1111 Bank Account Number: 987654321012 Routing Number: 123456789 SWIFT Code: ABCDUS33 Technical & Additional Details: IP Address: 192.168.1.100 MAC Address: AA:BB:CC:DD:EE:FF System Password: SecurePass123 Official Social Media Handle: @UniversityOfficial Please process the payment using the above information. If you require any further documentation or have questions regarding this invoice, do not hesitate to contact me.  Thank you for your prompt attention to this matter.  Sincerely, Dr. Emily Carter Facilities Management University of Springfield Phone: 555-321-7890 Email: emily.carter@university.edu
------------------------------
Scrubbed:  Subject: Payment Confirmation for Invoice INV-[BANK_15]-[BANK_16] Dear Accounts Payable Team, I am writing to confirm the payment for the building maintenance services provided under invoice INV-[BANK_17]-[BANK_18] at the University's Engineering Complex. Please review the details of this transaction below: Invoice Details: Invoice Number: INV-[BANK_19]-[BANK_20] Invoice Date: [DOB_07] Total Amount: $27,450.00 Vendor Information: Vendor Name: ABC Facilities Management Contact: [NAME_12] Vendor [NAME_11]: [EMAIL_08] [NAME_10]: (555) 987-[BANK_21] Vendor Address: [ADDRESS_09], Suite 300, Springfield, IL [BANK_22] Tax ID (EIN): 12-[BANK_23] University Representative: Name: Dr. [NAME_09] Email: [EMAIL_09] Phone: [PHONE_05] Office Address: [ADDRESS_10], Building 5, Room 204, Springfield, IL [BANK_24] Employee ID: UC123456 Date of Birth: [DOB_08] Social Security Number: [SSN_10] Payment Information: Primary Credit Card: [CREDIT_CARD_07] Bank Account Number: [BANK_25] Routing Number: [SSN_11] SWIFT Code: [SWIFT_01] Technical & Additional Details: IP Address: [IP_05] MAC Address: [MAC_05] System Password: [PASSWORD_05] Official Social Media Handle: [SOCIAL_01] Please process the payment using the above information. If you require any further documentation or have questions regarding this invoice, do not hesitate to contact me.  Thank you for your prompt attention to this matter.  Sincerely, Dr. [NAME_08] Facilities Management University of Springfield Phone: [PHONE_06] Email: [EMAIL_10]
##################################################
