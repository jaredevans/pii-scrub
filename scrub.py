import re
import spacy

PII_CONFIG = [
    {
        "name": "NAME",
        "prefix": "NAME",
        "detector_method_name": "detect_names",
        "scrubber_method_name": "scrub_names",
    },
    {
        "name": "DATE",
        "prefix": "DATE",
        "regex": re.compile(
            r"\b(?:(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d\d|"
            r"(?:0[1-9]|[12]\d|3[01])-(?:0[1-9]|1[0-2])-(?:19|20)\d\d|"
            r"(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))\b"
        ),
    },
    {
        "name": "PHONE_NUMBER",
        "prefix": "PHONE",
        "regex": re.compile(
            r"(?:\(\d{3}\)[-\s]?\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|(?<!\d)\d{10}(?!\d))"
        ),
    },
    {
        "name": "SSN",
        "prefix": "SSN",
        "regex": re.compile(r"\b(?:\d{3}-\d{2}-\d{4}|\d{9})\b"),
    },
    {
        "name": "EMAIL",
        "prefix": "EMAIL",
        "regex": re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        ),
    },
    {
        "name": "IP_ADDRESS",
        "prefix": "IP",
        "regex": re.compile(
            r"\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
        ),
    },
    {
        "name": "MAC_ADDRESS",
        "prefix": "MAC",
        "regex": re.compile(
            r"\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b"
        ),
    },
    {
        "name": "FULL_ADDRESS",
        "prefix": "ADDRESS",
        "regex": re.compile(
            r"\b\d+\s+[A-Za-z0-9\s]+\s+(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?|Lane|Ln\.?|Drive|Dr\.?),?\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?\b",
            re.IGNORECASE,
        ),
    },
    {
        "name": "PASSWORD",
        "prefix": "PASSWORD",
        "regex": re.compile(r"(?i)\bpassword\s*(?::|is)\s*(\S+)"),
    },
    {
        "name": "SOCIAL_HANDLE",
        "prefix": "SOCIAL",
        "regex": re.compile(r"@[A-Za-z0-9_]+"),
    },
    {
        "name": "SWIFT_CODE",
        "prefix": "SWIFT",
        "regex": re.compile(r"\b[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b"),
    },
    {
        "name": "NUMBERS",
        "prefix": "NUM",
        "regex": re.compile(r"\b\d+\b"),
    },
]

# Detection Engine
class DetectionEngine:
    def __init__(self):
        # Load spaCy model for name detection
        self.nlp = spacy.load("en_core_web_sm")

    def detect_by_regex(self, text, regex_pattern):
        return regex_pattern.findall(text)

    def detect_names(self, text):
        doc = self.nlp(text)
        # Return list of tuples: (start_index, end_index, name)
        return [(ent.start_char, ent.end_char, ent.text) for ent in doc.ents if ent.label_ == "PERSON"]


# Scrubbing Engine with counters for tokens
class ScrubbingEngine:
    def __init__(self):
        self.counters = {config["prefix"]: 1 for config in PII_CONFIG}

    def scrub_by_pattern(self, text, items_to_scrub, prefix):
        for item in items_to_scrub:
            token = f"[{prefix}_{self.counters[prefix]:02d}]"
            self.counters[prefix] += 1
            text = text.replace(item, token, 1)
        return text

    def scrub_names(self, text, name_matches):
        # Process names in reverse order to avoid shifting indices
        for start, end, name in sorted(name_matches, key=lambda x: x[0], reverse=True):
            token = f"[NAME_{self.counters['NAME']:02d}]"
            self.counters["NAME"] += 1
            text = text[:start] + token + text[end:]
        return text


# Main Scrub Class that processes in the specified order
class Scrub:
    def __init__(self):
        self.detection_engine = DetectionEngine()
        self.scrubbing_engine = ScrubbingEngine()

    def scrub(self, text):
        for config in PII_CONFIG:
            pii_name = config["name"]
            prefix = config["prefix"]
            
            # Determine detector method
            detector_method_name = config.get("detector_method_name")
            if detector_method_name:
                detector_method = getattr(self.detection_engine, detector_method_name)
                detected_items = detector_method(text)
            elif "regex" in config:
                detected_items = self.detection_engine.detect_by_regex(text, config["regex"])
            else:
                # Should not happen if config is well-defined
                continue

            if not detected_items:
                continue

            # Determine scrubber method
            scrubber_method_name = config.get("scrubber_method_name")
            if scrubber_method_name:
                scrubber_method = getattr(self.scrubbing_engine, scrubber_method_name)
                text = scrubber_method(text, detected_items)
            elif "regex" in config: # Implies generic scrubbing for regex-based items
                text = self.scrubbing_engine.scrub_by_pattern(text, detected_items, prefix)
            else:
                # Should not happen
                continue
        return text


if __name__ == "__main__":
    input_text = (
    "Subject: Payment & Contract Confirmation – Invoice INV-2023-0456\n\n"
    "To: Accounts Payable Team\n"
    "From: Dr. Emily Carter (emily.carter@university.edu)\n"
    "Date: 2023-10-02\n\n"

    "1. Invoice & Transaction Details\n"
    "Invoice Number: INV-2023-0456\n"
    "Invoice Date: 2023-09-30\n"
    "Purchase Order #: PO-8814-2023\n"
    "Total Amount: $27,450.00\n"
    "Payment Due: 2023-10-15\n\n"

    "2. Vendor Information\n"
    "Vendor Name: ABC Facilities Management\n"
    "Contact Name: Robert Smith\n"
    "Contact Email: robert.smith@abcfacilities.com\n"
    "Contact Phone: (555) 987-6543\n"
    "Vendor Address:\n"
    "456 Industrial Road, Suite 300\n"
    "Springfield, IL 62704\n"
    "Vendor Tax ID (EIN): 12-3456789\n"
    "Vendor Bank Account: 987654320123\n"
    "Vendor Routing Number: 123456780\n\n"

    "3. University Contact\n"
    "Representative: Dr. Emily Carter\n"
    "University Email: emily.carter@university.edu\n"
    "Work Phone: (555) 321-7890\n"
    "Mobile Phone: (555) 222-1122\n"
    "Employee ID: UC123456\n"
    "Date of Birth: 12/31/1980\n"
    "Social Security Number: 123-45-6789\n"
    "Office Address:\n"
    "789 Campus Avenue, Building 5, Room 204\n"
    "Springfield, IL 62703\n\n"

    "4. Payment & Financial Information\n"
    "Primary Credit Card: 4111-1111-1111-1111 (Exp: 11/28, CVV: 123)\n"
    "Secondary Credit Card: 5500-0000-0000-0004 (Exp: 08/26, CVV: 321)\n"
    "Bank Account Number: 987654321012\n"
    "Routing Number: 123456789\n"
    "SWIFT Code: ABCDUS33\n"
    "IBAN: US12 3456 7890 1234 5678 90\n"
    "Check Number: 102345\n\n"

    "5. Technical & Security Details\n"
    "User Login: ecarter\n"
    "Password: SecurePass123\n"
    "Temporary Password: Temp#2023$Pay!\n"
    "IP Address: 192.168.1.100\n"
    "Alternate IP: 10.0.0.15\n"
    "MAC Address: AA:BB:CC:DD:EE:FF\n"
    "VPN Login: emilycarter@srv-university (pass: Pa$$word987)\n"
    "Official Social Media: @UniversityOfficial\n\n"

    "6. Additional PII for Testing Robustness\n"
    "Passport Number: 981234567\n"
    "Driver’s License: S123-4567-8901-2345 (IL)\n"
    "License Plate: SPR-4567\n"
    "Student ID: S20231234\n"
    "Personal Email: emily.carter@gmail.com\n"
    "Home Address: 345 Maple Lane, Springfield, IL 62702\n"
    "Emergency Contact:\n"
    "Name: Mark Carter\n"
    "Phone: (555) 789-1234\n"
    "Relation: Spouse\n\n"

    "7. Internal Notes (For Processing Only)\n"
    "Robert Smith authorized payment via email (see attached .eml)\n"
    "Dr. Carter prefers text message notifications (SMS: 555-222-1122)\n"
    "All confidential information must be handled per HIPAA and FERPA guidelines.\n\n"

    "If you require any further documentation or have questions regarding this invoice, please contact:\n\n"
    "Dr. Emily Carter\n"
    "Facilities Management, University of Springfield\n"
    "Phone: (555) 321-7890\n"
    "Email: emily.carter@university.edu\n"
    )


    scrubber = Scrub()
    scrubbed_text = scrubber.scrub(input_text)
    print("Original text:")
    print(input_text)
    print("\n\n#################\n\nScrubbed text:")
    print(scrubbed_text)
