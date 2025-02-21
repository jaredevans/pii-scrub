import re
import spacy

# Detection Engine
class DetectionEngine:
    def __init__(self):
        # Load spaCy model for names
        self.nlp = spacy.load("en_core_web_sm")
        
        self.email_regex = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )
        self.phone_regex = re.compile(r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b")
        self.password_regex = re.compile(r"(?i)\bpassword\s*(?::|is)\s*(\S+)")
        self.credit_card_regex = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
        self.ssn_regex = re.compile(r"\b(?:\d{3}-\d{2}-\d{4}|\d{9})\b")
        # Basic street address (number + street name + type)
        self.address_regex = re.compile(
            r"\b\d+\s+[A-Za-z0-9\s]+\s+(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?|Lane|Ln\.?|Drive|Dr\.?)\b",
            re.IGNORECASE,
        )
        self.ip_regex = re.compile(
            r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
        )
        self.dob_regex = re.compile(
            r"\b(?:(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d\d|"
            r"(?:0[1-9]|[12]\d|3[01])-(?:0[1-9]|1[0-2])-(?:19|20)\d\d|"
            r"(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))\b"
        )
        self.bank_info_regex = re.compile(r"\b\d{4,17}\b")
        
        # New detection patterns:
        # Tax Identification Numbers (EIN format: 2 digits, dash, 7 digits)
        self.tax_id_regex = re.compile(r"\b\d{2}-\d{7}\b")
        # Full postal addresses (simple version: street address, city, state, ZIP)
        self.full_address_regex = re.compile(
            r"\b\d+\s+[A-Za-z0-9\s]+\s+(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?|Lane|Ln\.?|Drive|Dr\.?),?\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?\b",
            re.IGNORECASE,
        )
        # Device MAC addresses (six groups of two hex digits separated by colons or hyphens)
        self.mac_regex = re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b")
        # Social Media Handles/Usernames (e.g., Twitter)
        self.social_media_regex = re.compile(r"@[A-Za-z0-9_]+")
        # SWIFT Codes: 8 or 11 alphanumeric characters (4 letters, 2 letters, 2 alphanumeric, optional 3 alphanumeric)
        self.swift_regex = re.compile(r"\b[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b")

    def detect_names(self, text):
        doc = self.nlp(text)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        return names

    def detect_emails(self, text):
        return self.email_regex.findall(text)

    def detect_phone_numbers(self, text):
        return self.phone_regex.findall(text)
    
    def detect_passwords(self, text):
        return self.password_regex.findall(text)
    
    def detect_credit_cards(self, text):
        return self.credit_card_regex.findall(text)
    
    def detect_ssns(self, text):
        return self.ssn_regex.findall(text)
    
    def detect_addresses(self, text):
        return self.address_regex.findall(text)
    
    def detect_ip_addresses(self, text):
        return self.ip_regex.findall(text)
    
    def detect_dobs(self, text):
        return self.dob_regex.findall(text)
    
    def detect_bank_info(self, text):
        return self.bank_info_regex.findall(text)
    
    def detect_tax_ids(self, text):
        return self.tax_id_regex.findall(text)
    
    def detect_full_addresses(self, text):
        return self.full_address_regex.findall(text)
    
    def detect_mac_addresses(self, text):
        return self.mac_regex.findall(text)
    
    def detect_social_handles(self, text):
        return self.social_media_regex.findall(text)
    
    def detect_swift_codes(self, text):
        return self.swift_regex.findall(text)


# Scrubbing Engine
class ScrubbingEngine:
    def __init__(self):
        self.replacement = "[REDACTED]"

    def scrub_names(self, text, names):
        for name in names:
            text = text.replace(name, self.replacement)
        return text

    def scrub_emails(self, text, emails):
        for email in emails:
            text = text.replace(email, self.replacement)
        return text

    def scrub_phone_numbers(self, text, phone_numbers):
        for phone in phone_numbers:
            text = text.replace(phone, self.replacement)
        return text

    def scrub_passwords(self, text, passwords):
        for password in passwords:
            text = text.replace(password, self.replacement)
        return text

    def scrub_credit_cards(self, text, credit_cards):
        for cc in credit_cards:
            text = text.replace(cc, self.replacement)
        return text

    def scrub_ssns(self, text, ssns):
        for ssn in ssns:
            text = text.replace(ssn, self.replacement)
        return text

    def scrub_addresses(self, text, addresses):
        for address in addresses:
            text = text.replace(address, self.replacement)
        return text

    def scrub_ip_addresses(self, text, ip_addresses):
        for ip in ip_addresses:
            text = text.replace(ip, self.replacement)
        return text

    def scrub_dobs(self, text, dobs):
        for dob in dobs:
            text = text.replace(dob, self.replacement)
        return text

    def scrub_bank_info(self, text, bank_infos):
        for info in bank_infos:
            text = text.replace(info, self.replacement)
        return text

    def scrub_tax_ids(self, text, tax_ids):
        for tax_id in tax_ids:
            text = text.replace(tax_id, self.replacement)
        return text

    def scrub_full_addresses(self, text, full_addresses):
        for addr in full_addresses:
            text = text.replace(addr, self.replacement)
        return text

    def scrub_mac_addresses(self, text, mac_addresses):
        for mac in mac_addresses:
            text = text.replace(mac, self.replacement)
        return text

    def scrub_social_handles(self, text, handles):
        for handle in handles:
            text = text.replace(handle, self.replacement)
        return text

    def scrub_swift_codes(self, text, swift_codes):
        for code in swift_codes:
            text = text.replace(code, self.replacement)
        return text


# Scrub Class
class Scrub:
    def __init__(self):
        self.detection_engine = DetectionEngine()
        self.scrubbing_engine = ScrubbingEngine()

    def scrub(self, text):
        names = self.detection_engine.detect_names(text)
        emails = self.detection_engine.detect_emails(text)
        phone_numbers = self.detection_engine.detect_phone_numbers(text)
        passwords = self.detection_engine.detect_passwords(text)
        credit_cards = self.detection_engine.detect_credit_cards(text)
        ssns = self.detection_engine.detect_ssns(text)
        addresses = self.detection_engine.detect_addresses(text)
        ip_addresses = self.detection_engine.detect_ip_addresses(text)
        dobs = self.detection_engine.detect_dobs(text)
        bank_infos = self.detection_engine.detect_bank_info(text)
        tax_ids = self.detection_engine.detect_tax_ids(text)
        full_addresses = self.detection_engine.detect_full_addresses(text)
        mac_addresses = self.detection_engine.detect_mac_addresses(text)
        social_handles = self.detection_engine.detect_social_handles(text)
        swift_codes = self.detection_engine.detect_swift_codes(text)

        text = self.scrubbing_engine.scrub_names(text, names)
        text = self.scrubbing_engine.scrub_emails(text, emails)
        text = self.scrubbing_engine.scrub_phone_numbers(text, phone_numbers)
        text = self.scrubbing_engine.scrub_passwords(text, passwords)
        text = self.scrubbing_engine.scrub_credit_cards(text, credit_cards)
        text = self.scrubbing_engine.scrub_ssns(text, ssns)
        text = self.scrubbing_engine.scrub_addresses(text, addresses)
        text = self.scrubbing_engine.scrub_ip_addresses(text, ip_addresses)
        text = self.scrubbing_engine.scrub_dobs(text, dobs)
        text = self.scrubbing_engine.scrub_bank_info(text, bank_infos)
        text = self.scrubbing_engine.scrub_tax_ids(text, tax_ids)
        text = self.scrubbing_engine.scrub_full_addresses(text, full_addresses)
        text = self.scrubbing_engine.scrub_mac_addresses(text, mac_addresses)
        text = self.scrubbing_engine.scrub_social_handles(text, social_handles)
        text = self.scrubbing_engine.scrub_swift_codes(text, swift_codes)

        return text


# Example Usage
if __name__ == "__main__":
    input_text = (
        "John Doe, email: john.doe@example.com, phone: 123-456-7890, password is supersecret, "
        "credit card: 4111-1111-1111-1111, SSN: 123-45-6789, or 123456789, address: 123 Main Street, "
        "IP: 192.168.1.100, DOB: 12/31/1990, EIN: 12-3456789, full address: 123 Main Street, Springfield, IL 62704, "
        "MAC: AA:BB:CC:DD:EE:FF, SWIFT: ABCDUS33, account number: 123456789012, routing: 123456789. "
        "Also, another card: 5500 0000 0000 0004, and address: 456 Elm Ave, IP: 10.0.0.5, DOB: 1990-12-31, "
        "account is 9876543210, routing number is 987654321, and a random number 1234567. "
        "Follow our social media at @UniversityOfficial."
    )
    scrubber = Scrub()
    scrubbed_text = scrubber.scrub(input_text)
    print("Scrubbed text:")
    print(scrubbed_text)
