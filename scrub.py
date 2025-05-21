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
