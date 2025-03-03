import re
import spacy

# Detection Engine
class DetectionEngine:
    def __init__(self):
        # Load spaCy model for name detection
        self.nlp = spacy.load("en_core_web_sm")

        # Date regex supporting common formats (MM/DD/YYYY, DD-MM-YYYY, YYYY-MM-DD)
        self.date_regex = re.compile(
            r"\b(?:(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d\d|"
            r"(?:0[1-9]|[12]\d|3[01])-(?:0[1-9]|1[0-2])-(?:19|20)\d\d|"
            r"(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))\b"
        )
        # Phone regex to capture:
        # (555) 987-6543, (555)987-6543, 555-987-6543, 5559876543
        # Negative lookbehind/lookahead ensures a 10-digit match is standalone.
        self.phone_regex = re.compile(
            r"(?:\(\d{3}\)[-\s]?\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|(?<!\d)\d{10}(?!\d))"
        )
        # Social Security Number regex (format xxx-xx-xxxx or 9 digits)
        self.ssn_regex = re.compile(r"\b(?:\d{3}-\d{2}-\d{4}|\d{9})\b")
        # Email regex
        self.email_regex = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )
        # IP address regex (IPv4)
        self.ip_regex = re.compile(
            r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
        )
        # MAC address regex
        self.mac_regex = re.compile(
            r"\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b"
        )
        # Full address regex (street address, city, state, zip)
        self.full_address_regex = re.compile(
            r"\b\d+\s+[A-Za-z0-9\s]+\s+(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?|Lane|Ln\.?|Drive|Dr\.?),?\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?\b",
            re.IGNORECASE,
        )
        # Password regex (captures any non-space sequence after "password:" or "password is")
        self.password_regex = re.compile(r"(?i)\bpassword\s*(?::|is)\s*(\S+)")
        # Social media handle regex
        self.social_media_regex = re.compile(r"@[A-Za-z0-9_]+")
        # SWIFT code regex (4 letters, 2 letters, 2 alphanumeric, optional 3 alphanumeric)
        self.swift_regex = re.compile(r"\b[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b")
        # Any sequence of numbers (catch-all; standalone digits)
        self.numbers_regex = re.compile(r"\b\d+\b")

    def detect_dates(self, text):
        return self.date_regex.findall(text)

    def detect_phone_numbers(self, text):
        return self.phone_regex.findall(text)

    def detect_ssns(self, text):
        return self.ssn_regex.findall(text)

    def detect_emails(self, text):
        return self.email_regex.findall(text)

    def detect_ip_addresses(self, text):
        return self.ip_regex.findall(text)

    def detect_mac_addresses(self, text):
        return self.mac_regex.findall(text)

    def detect_names(self, text):
        doc = self.nlp(text)
        # Return list of tuples: (start_index, end_index, name)
        return [(ent.start_char, ent.end_char, ent.text) for ent in doc.ents if ent.label_ == "PERSON"]

    def detect_full_addresses(self, text):
        return self.full_address_regex.findall(text)

    def detect_passwords(self, text):
        return self.password_regex.findall(text)

    def detect_social_handles(self, text):
        return self.social_media_regex.findall(text)

    def detect_swift_codes(self, text):
        return self.swift_regex.findall(text)

    def detect_numbers(self, text):
        return self.numbers_regex.findall(text)


# Scrubbing Engine with counters for tokens
class ScrubbingEngine:
    def __init__(self):
        self.counters = {
            "DATE": 1,
            "PHONE": 1,
            "SSN": 1,
            "EMAIL": 1,
            "IP": 1,
            "MAC": 1,
            "NAME": 1,
            "ADDRESS": 1,
            "PASSWORD": 1,
            "SOCIAL": 1,
            "SWIFT": 1,
            "NUM": 1,
        }

    def _replace_next(self, text, target, prefix):
        index = text.find(target)
        if index == -1:
            return text
        token = f"[{prefix}_{self.counters[prefix]:02d}]"
        self.counters[prefix] += 1
        return text[:index] + token + text[index+len(target):]

    def scrub_dates(self, text, dates):
        for date in dates:
            text = self._replace_next(text, date, "DATE")
        return text

    def scrub_phone_numbers(self, text, phone_numbers):
        for phone in phone_numbers:
            text = self._replace_next(text, phone, "PHONE")
        return text

    def scrub_ssns(self, text, ssns):
        for ssn in ssns:
            text = self._replace_next(text, ssn, "SSN")
        return text

    def scrub_emails(self, text, emails):
        for email in emails:
            text = self._replace_next(text, email, "EMAIL")
        return text

    def scrub_ip_addresses(self, text, ip_addresses):
        for ip in ip_addresses:
            text = self._replace_next(text, ip, "IP")
        return text

    def scrub_mac_addresses(self, text, mac_addresses):
        for mac in mac_addresses:
            text = self._replace_next(text, mac, "MAC")
        return text

    def scrub_names(self, text, name_matches):
        # Process names in reverse order to avoid shifting indices
        for start, end, name in sorted(name_matches, key=lambda x: x[0], reverse=True):
            token = f"[NAME_{self.counters['NAME']:02d}]"
            self.counters["NAME"] += 1
            text = text[:start] + token + text[end:]
        return text

    def scrub_full_addresses(self, text, full_addresses):
        for addr in full_addresses:
            text = self._replace_next(text, addr, "ADDRESS")
        return text

    def scrub_passwords(self, text, passwords):
        for pwd in passwords:
            text = self._replace_next(text, pwd, "PASSWORD")
        return text

    def scrub_social_handles(self, text, handles):
        for handle in handles:
            text = self._replace_next(text, handle, "SOCIAL")
        return text

    def scrub_swift_codes(self, text, swift_codes):
        for code in swift_codes:
            text = self._replace_next(text, code, "SWIFT")
        return text

    def scrub_numbers(self, text, numbers):
        for number in numbers:
            text = self._replace_next(text, number, "NUM")
        return text


# Main Scrub Class that processes in the specified order
class Scrub:
    def __init__(self):
        self.detection_engine = DetectionEngine()
        self.scrubbing_engine = ScrubbingEngine()

    def scrub(self, text):
        # Detect entities in the specified order:
        names = self.detection_engine.detect_names(text)
        dates = self.detection_engine.detect_dates(text)
        phone_numbers = self.detection_engine.detect_phone_numbers(text)
        ssns = self.detection_engine.detect_ssns(text)
        emails = self.detection_engine.detect_emails(text)
        ip_addresses = self.detection_engine.detect_ip_addresses(text)
        mac_addresses = self.detection_engine.detect_mac_addresses(text)
        full_addresses = self.detection_engine.detect_full_addresses(text)
        passwords = self.detection_engine.detect_passwords(text)
        social_handles = self.detection_engine.detect_social_handles(text)
        swift_codes = self.detection_engine.detect_swift_codes(text)
        numbers = self.detection_engine.detect_numbers(text)

        # Scrub in the same order:
        text = self.scrubbing_engine.scrub_names(text, names)
        text = self.scrubbing_engine.scrub_dates(text, dates)
        text = self.scrubbing_engine.scrub_phone_numbers(text, phone_numbers)
        text = self.scrubbing_engine.scrub_ssns(text, ssns)
        text = self.scrubbing_engine.scrub_emails(text, emails)
        text = self.scrubbing_engine.scrub_ip_addresses(text, ip_addresses)
        text = self.scrubbing_engine.scrub_mac_addresses(text, mac_addresses)
        text = self.scrubbing_engine.scrub_full_addresses(text, full_addresses)
        text = self.scrubbing_engine.scrub_passwords(text, passwords)
        text = self.scrubbing_engine.scrub_social_handles(text, social_handles)
        text = self.scrubbing_engine.scrub_swift_codes(text, swift_codes)
        text = self.scrubbing_engine.scrub_numbers(text, numbers)

        return text


if __name__ == "__main__":
    input_text = (
        "Subject: Payment Confirmation for Invoice INV-2023-0456 \n"
        "Dear Accounts Payable Team,\n "
        "I am writing to confirm the payment for the building maintenance services provided under invoice INV-2023-0456 at the University's Engineering Complex.\n "
        "Please review the details of this transaction below: "
        "Invoice Details: Invoice Number: INV-2023-0456 Invoice Date: 2023-09-30 Total Amount: $27,450.00\n "
        "Vendor Information: Vendor Name: ABC Facilities Management Contact: Robert Smith Vendor Email: robert.smith@abcfacilities.com Vendor Phone: (555) 987-6543\n "
        "Vendor Address: 456 Industrial Road, Suite 300, Springfield, IL 62704 Tax ID (EIN): 12-3456789\n "
        "University Representative: Name: Dr. Emily Carter Email: emily.carter@university.edu Phone: 555-321-7890 Office Address: 789 Campus Avenue, Building 5, Room 204, Springfield, IL 62703\n "
        "Employee ID: UC123456 Date of Birth: 12/31/1980 Social Security Number: 123-45-6789\n "
        "Payment Information: Primary Credit Card: 4111-1111-1111-1111 Bank Account Number: 987654321012 Routing Number: 123456789 SWIFT Code: ABCDUS33\n "
        "Technical & Additional Details: IP Address: 192.168.1.100 MAC Address: AA:BB:CC:DD:EE:FF System Password: SecurePass123 Official Social Media Handle: @UniversityOfficial\n "
        "Please process the payment using the above information. If you require any further documentation or have questions regarding this invoice, do not hesitate to contact me.\n "
        "Thank you for your prompt attention to this matter. Sincerely, Dr. Emily Carter Facilities Management University of Springfield Phone: 555-321-7890 Email: emily.carter@university.edu"
    )

    scrubber = Scrub()
    scrubbed_text = scrubber.scrub(input_text)
    print("Original text:")
    print(input_text)
    print("\n\n#################\n\nScrubbed text:")
    print(scrubbed_text)
