"""Small language adaptation layer for the deterministic demo."""

from __future__ import annotations

from typing import Any


DISCLAIMER = {
    "en": (
        "HaqSetu provides a preliminary, evidence-linked screening only. "
        "Official government portals and departments are authoritative; rules, "
        "documents, and deadlines can change. Do not share Aadhaar, OTPs, bank "
        "passwords, or other sensitive credentials here."
    ),
    "hi": (
        "HaqSetu केवल प्रारम्भिक और साक्ष्य-आधारित स्क्रीनिंग देता है। "
        "सरकारी विभाग और आधिकारिक पोर्टल ही अंतिम प्राधिकरण हैं; नियम, दस्तावेज़ "
        "और समय-सीमा बदल सकती है। यहां आधार, OTP, बैंक पासवर्ड या अन्य संवेदनशील "
        "जानकारी साझा न करें।"
    ),
}

TEXT: dict[str, dict[str, str]] = {
    "en": {
        "intake": "Profile facts received for preliminary screening.",
        "verify": "Verify this signal and the required documents on the official portal.",
        "consent": "Before any assisted application, obtain the person's informed consent and show the official portal.",
        "no_consent": "No application was submitted. Consent is not needed for this screening result.",
        "time_saved": "Estimated time saved is a rough comparison with manually scanning the listed schemes; it is not a guarantee.",
    },
    "hi": {
        "intake": "प्रारम्भिक स्क्रीनिंग के लिए प्रोफ़ाइल की जानकारी प्राप्त हुई।",
        "verify": "इस संकेत और आवश्यक दस्तावेज़ों को आधिकारिक पोर्टल पर सत्यापित करें।",
        "consent": "किसी सहायक आवेदन से पहले व्यक्ति की सूचित सहमति लें और आधिकारिक पोर्टल दिखाएं।",
        "no_consent": "कोई आवेदन जमा नहीं किया गया। इस स्क्रीनिंग परिणाम के लिए सहमति आवश्यक नहीं है।",
        "time_saved": "समय-बचत का अनुमान सूचीबद्ध योजनाओं को मैन्युअल रूप से खोजने की तुलना है; यह गारंटी नहीं है।",
    },
}


def lang(value: str | None) -> str:
    return "hi" if value == "hi" else "en"


def localized(scheme: dict[str, Any], language: str, key: str) -> str:
    language = lang(language)
    return str(scheme.get(f"{key}_{language}") or scheme.get(f"{key}_en") or "")
