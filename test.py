from scrub import Scrub

def main():
    test_prompts = [
        # Combined PII types with new ones
        ("John Doe, email: john.doe@example.com, phone: 123-456-7890, password is supersecret, "
         "credit card: 4111-1111-1111-1111, SSN: 123-45-6789, or 123456789, address: 123 Main Street, "
         "IP: 192.168.1.100, DOB: 12/31/1990, EIN: 12-3456789, full address: 123 Main Street, Springfield, IL 62704, "
         "MAC: AA:BB:CC:DD:EE:FF, account number: 123456789012, routing: 123456789."),
        "Jane Smith's password is mypassword123",
        "Please send an email to support@example.org and call 555.123.4567",
        "Employee: Michael Jordan, email: mj23@nba.com, phone: (555) 987-6543",
        "Contact number: 444-555-6666, SSN: 123456789",
        "Credit card: 5500 0000 0000 0004, address: 789 Maple Blvd.",
        "IP: 10.0.0.1, DOB: 01/15/1985, EIN: 98-7654321",
        "DOB: 1985-01-15, bank info: 1234567890123456, full address: 456 Oak Road, Somecity, TX 75001",
        "Routing: 123456789, account: 1234567890123456",
        "Send package to 456 Elm Street",
        "Phone: 123.456.7890, Email: test_email+label@example.com",
        "Password: secret_pass",
        "Name: Dr. Emily Watson, email: emily.watson@example.com, MAC: 00:1A:2B:3C:4D:5E",
        "Server IP is 192.168.0.101, credit card: 4111111111111111, full address: 789 Broadway Ave., New York, NY 10001",
        "SSN: 987-65-4321, also SSN: 987654321",
        "Email alternative: test.email+alias@example.co.uk",
        "Phone alternative: (123) 456-7890",
        "Password alternative: Password: AnotherSecret",
        "Credit card alternative: 4111111111111111",
        "SSN alternative: 987-65-4321 and also 987654321",
        "Address alternative: 100 Broadway Ave., Los Angeles, CA 90012",
        "IP alternative: 255.255.255.255",
        "DOB alternative: 07/04/2020",           # MM/DD/YYYY
        "DOB alternative: 2020-07-04",           # YYYY-MM-DD
        "DOB alternative: 04-07-2020",           # DD-MM-YYYY
        "Bank info alternative: 1234",
        "Bank info alternative: 12345678901234567",
        "Name with title: Dr. Sarah Connor, email: sarah.connor@future.com",
        "Random text without any PII.",
        "Tax ID: 12-3456789, and another one: 98-7654321",
        "Full postal address: 1600 Pennsylvania Avenue, Washington, DC 20500",
        "MAC addresses: AA-BB-CC-DD-EE-FF and aa:bb:cc:dd:ee:ff",
        "Subject: Payment Confirmation for Invoice INV-2023-0456 Dear Accounts Payable Team, I am writing to confirm the payment for the building maintenance services provided under invoice INV-2023-0456 at the University's Engineering Complex. Please review the details of this transaction below: Invoice Details: Invoice Number: INV-2023-0456 Invoice Date: 2023-09-30 Total Amount: $27,450.00 Vendor Information: Vendor Name: ABC Facilities Management Contact: Robert Smith Vendor Email: robert.smith@abcfacilities.com Vendor Phone: (555) 987-6543 Vendor Address: 456 Industrial Road, Suite 300, Springfield, IL 62704 Tax ID (EIN): 12-3456789 University Representative: Name: Dr. Emily Carter Email: emily.carter@university.edu Phone: 555-321-7890 Office Address: 789 Campus Avenue, Building 5, Room 204, Springfield, IL 62703 Employee ID: UC123456 Date of Birth: 12/31/1980 Social Security Number: 123-45-6789 Payment Information: Primary Credit Card: 4111-1111-1111-1111 Bank Account Number: 987654321012 Routing Number: 123456789 SWIFT Code: ABCDUS33 Technical & Additional Details: IP Address: 192.168.1.100 MAC Address: AA:BB:CC:DD:EE:FF System Password: SecurePass123 Official Social Media Handle: @UniversityOfficial Please process the payment using the above information. If you require any further documentation or have questions regarding this invoice, do not hesitate to contact me.  Thank you for your prompt attention to this matter.  Sincerely, Dr. Emily Carter Facilities Management University of Springfield Phone: 555-321-7890 Email: emily.carter@university.edu",
        "Give me a 5 questions quiz about university biology 101 in multiple choice questions formatted for Blackboard Ultra in tab delimited UTF-8?"
    ]
    
    scrubber = Scrub()
    for i, prompt in enumerate(test_prompts, start=1):
        scrubbed = scrubber.scrub(prompt)
        print("#" * 50)
        print(f"Test {i}:")
        print("Original: ", prompt)
        print("-" * 30)
        print("Scrubbed: ", scrubbed)

if __name__ == "__main__":
    main()
