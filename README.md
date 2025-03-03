# pii-scrub
Scrub all sorts of PII information from a text string

requirements.txt to help with install of modules.

Get the spacey en_core_web_sm:

python -m spacy download en_core_web_sm

Covered many corner cases, but there may be more lurking in the dark.  If find any, let me know!

Sample pii-scrubbing:

##################################################
Original text:
Subject: Payment Confirmation for Invoice INV-2023-0456
Dear Accounts Payable Team,
 I am writing to confirm the payment for the building maintenance services provided under invoice INV-2023-0456 at the University's Engineering Complex.
 Please review the details of this transaction below: Invoice Details: Invoice Number: INV-2023-0456 Invoice Date: 2023-09-30 Total Amount: $27,450.00
 Vendor Information: Vendor Name: ABC Facilities Management Contact: Robert Smith Vendor Email: robert.smith@abcfacilities.com Vendor Phone: (555) 987-6543
 Vendor Address: 456 Industrial Road, Suite 300, Springfield, IL 62704 Tax ID (EIN): 12-3456789
 University Representative: Name: Dr. Emily Carter Email: emily.carter@university.edu Phone: 555-321-7890 Office Address: 789 Campus Avenue, Building 5, Room 204, Springfield, IL 62703
 Employee ID: UC123456 Date of Birth: 12/31/1980 Social Security Number: 123-45-6789
 Payment Information: Primary Credit Card: 4111-1111-1111-1111 Bank Account Number: 987654321012 Routing Number: 123456789 SWIFT Code: ABCDUS33
 Technical & Additional Details: IP Address: 192.168.1.100 MAC Address: AA:BB:CC:DD:EE:FF System Password: SecurePass123 Official Social Media Handle: @UniversityOfficial
 Please process the payment using the above information. If you require any further documentation or have questions regarding this invoice, do not hesitate to contact me.
 Thank you for your prompt attention to this matter. Sincerely, Dr. Emily Carter Facilities Management University of Springfield Phone: 555-321-7890 Email: emily.carter@university.edu


#################

Scrubbed text:
Subject: Payment Confirmation for Invoice INV-[NUM_0[NUM_27]]-[NUM_02]
Dear Accounts Payable Team,
 I am writing to confirm the payment for the building maintenance services provided under invoice INV-[NUM_03]-[NUM_04] at the University's Engineering Complex.
 Please review the details of this transaction below: Invoice Details: Invoice Number: INV-[NUM_0[NUM_18]]-[NUM_06] Invoice Date: [DATE_01] Total Amount: $[NUM_08],[NUM_09].[NUM_10]
 Vendor Information: Vendor Name: ABC Facilities Management Contact: [NAME_05] Vendor [NAME_04]: [EMAIL_01] [NAME_03]: [PHONE_01]
 Vendor Address: [NUM_13] Industrial Road, Suite [NUM_07]0, Springfield, IL [NUM_14] Tax ID (EIN): [NUM_15]-[NUM_16]
 University Representative: Name: Dr. [NAME_02] Email: [EMAIL_02] Phone: [PHONE_02] Office Address: [NUM_17] Campus Avenue, Building 5, Room [NUM_19], Springfield, IL [NUM_20]
 Employee ID: UC[NUM_21]3[NUM_22]6 Date of Birth: [DATE_02] Social Security Number: [SSN_01]
 Payment Information: Primary Credit Card: [NUM_23]-[NUM_24]-[NUM_25]-[NUM_26] Bank Account Number: [NUM_11][NUM_12]21012 Routing Number: [SSN_02] SWIFT Code: [SWIFT_01]
 Technical & Additional Details: IP Address: [IP_01] MAC Address: [MAC_01] System Password: [PASSWORD_01] Official Social Media Handle: [SOCIAL_01]
 Please process the payment using the above information. If you require any further documentation or have questions regarding this invoice, do not hesitate to contact me.
 Thank you for your prompt attention to this matter. Sincerely, Dr. [NAME_01] Facilities Management University of Springfield Phone: [PHONE_03] Email: [EMAIL_03]
(scrub) jared.evans@JARED-EVANS-C02G14ZWQ05N scrub %
