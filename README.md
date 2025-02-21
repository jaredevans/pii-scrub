# pii-scrub
Scrub all sorts of PII information from a text string

requirements.txt to help with install of modules.

Get the spacey en_core_web_sm:
python -m spacy download en_core_web_sm

Covered many corner cases, but there may be more lurking in the dark.  If find any, let me know!

Sample pii-scrubbing:

##################################################

Test 33:

Original:  

Subject: Payment Confirmation for Invoice INV-2023-0456 Dear Accounts Payable Team, I am writing to confirm the payment for the building maintenance services provided under invoice INV-2023-0456 at the University's Engineering Complex. Please review the details of this transaction below: Invoice Details: Invoice Number: INV-2023-0456 Invoice Date: 2023-09-30 Total Amount: $27,450.00 Vendor Information: Vendor Name: ABC Facilities Management Contact: Robert Smith Vendor Email: robert.smith@abcfacilities.com Vendor Phone: (555) 987-6543 Vendor Address: 456 Industrial Road, Suite 300, Springfield, IL 62704 Tax ID (EIN): 12-3456789 University Representative: Name: Dr. Emily Carter Email: emily.carter@university.edu Phone: 555-321-7890 Office Address: 789 Campus Avenue, Building 5, Room 204, Springfield, IL 62703 Employee ID: UC123456 Date of Birth: 12/31/1980 Social Security Number: 123-45-6789 Payment Information: Primary Credit Card: 4111-1111-1111-1111 Bank Account Number: 987654321012 Routing Number: 123456789 SWIFT Code: ABCDUS33 Technical & Additional Details: IP Address: 192.168.1.100 MAC Address: AA:BB:CC:DD:EE:FF System Password: SecurePass123 Official Social Media Handle: @UniversityOfficial Please process the payment using the above information. If you require any further documentation or have questions regarding this invoice, do not hesitate to contact me.  Thank you for your prompt attention to this matter.  Sincerely, Dr. Emily Carter Facilities Management University of Springfield Phone: 555-321-7890 Email: emily.carter@university.edu

------------------------------

Scrubbed:  

Subject: Payment Confirmation for Invoice INV-[REDACTED]-[REDACTED] Dear Accounts Payable Team, I am writing to confirm the payment for the building maintenance services provided under invoice INV-[REDACTED]-[REDACTED] at the University's Engineering Complex. Please review the details of this transaction below: Invoice Details: Invoice Number: INV-[REDACTED]-[REDACTED] Invoice Date: [REDACTED] Total Amount: $27,450.00 Vendor Information: Vendor Name: ABC Facilities Management Contact: [REDACTED] Vendor [REDACTED]: [REDACTED] [REDACTED]: (555) 987-[REDACTED] Vendor Address: [REDACTED], Suite 300, Springfield, IL [REDACTED] Tax ID (EIN): 12-[REDACTED] University Representative: Name: Dr. [REDACTED] [REDACTED]: [REDACTED] Phone: [REDACTED] Office Address: [REDACTED], Building 5, Room 204, Springfield, IL [REDACTED] Employee ID: UC123456 Date of Birth: [REDACTED] Social Security Number: [REDACTED] Payment Information: Primary Credit Card: [REDACTED] Bank Account Number: 987[REDACTED]21012 Routing Number: [REDACTED] SWIFT Code: [REDACTED] Technical & Additional Details: IP Address: [REDACTED] MAC Address: [REDACTED] System Password: [REDACTED] Official Social Media Handle: [REDACTED] Please process the payment using the above information. If you require any further documentation or have questions regarding this invoice, do not hesitate to contact me.  Thank you for your prompt attention to this matter.  Sincerely, Dr. [REDACTED] Facilities Management University of Springfield Phone: [REDACTED] [REDACTED]: [REDACTED]

##################################################
