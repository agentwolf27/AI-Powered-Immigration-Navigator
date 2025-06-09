# Placeholder data structures

# VISA_TYPES: A dictionary mapping country codes to a list of visa type names
VISA_TYPES = {
    "US": ["H-1B", "F-1", "B-2"],
    "CA": ["Work Permit", "Student Visa", "Visitor Visa"],
    "UK": ["Tier 2 (General)", "Tier 4 (Student)", "Standard Visitor Visa"]
}

# VISA_STAGES: A dictionary mapping visa types to a list of procedural stages
VISA_STAGES = {
    "H-1B": ["Petition Filing", "USCIS Processing", "Interview", "Visa Stamping"],
    "F-1": ["I-20 Application", "SEVIS Fee Payment", "Visa Interview", "Port of Entry"],
    "B-2": ["Online Application (DS-160)", "Fee Payment", "Visa Interview"],
    "Work Permit": ["LMIA Application (if applicable)", "Work Permit Application", "Biometrics", "Approval"],
    "Student Visa": ["Letter of Acceptance", "Study Permit Application", "Biometrics", "Approval"],
    "Visitor Visa": ["Online Application", "Fee Payment", "Biometrics (if required)", "Interview (if required)"],
    "Tier 2 (General)": ["Certificate of Sponsorship", "Online Application", "TB Test (if applicable)", "Biometrics", "Visa Decision"],
    "Tier 4 (Student)": ["Confirmation of Acceptance for Studies (CAS)", "Online Application", "TB Test (if applicable)", "Biometrics", "Visa Decision"],
    "Standard Visitor Visa": ["Online Application", "TB Test (if applicable)", "Biometrics", "Visa Decision"]
}

# REQUIRED_DOCUMENTS: A dictionary mapping visa types and stages to a list of required documents
# The keys are tuples of (visa_type, stage)
REQUIRED_DOCUMENTS = {
    ("H-1B", "Petition Filing"): ["Form I-129", "Passport Copy", "Educational Certificates", "Experience Letters", "LCA Certificate"],
    ("H-1B", "Interview"): ["Interview Appointment Letter", "DS-160 Confirmation", "Passport", "I-797 Approval Notice"],
    ("F-1", "I-20 Application"): ["Passport Copy", "Proof of Funds", "Academic Transcripts"],
    ("F-1", "Visa Interview"): ["I-20 Form", "SEVIS Fee Receipt", "DS-160 Confirmation", "Passport", "Financial Documents"],
    # Add more sample data as needed
}

# Placeholder functions

def get_visa_types(country: str) -> list[str]:
    """
    Returns a list of visa types for the given country.
    """
    return VISA_TYPES.get(country.upper(), [])

def get_visa_stages(visa_type: str) -> list[str]:
    """
    Returns a list of stages for the given visa type.
    """
    return VISA_STAGES.get(visa_type, [])

def get_required_documents(visa_type: str, stage: str) -> list[str]:
    """
    Returns a list of required documents for the given visa type and stage.
    """
    return REQUIRED_DOCUMENTS.get((visa_type, stage), [])

def get_immigration_steps(country: str, visa_type: str, current_stage: str) -> list[str]:
    """
    Returns a personalized list of next steps based on user's input.
    This is a placeholder and will need more sophisticated logic.
    """
    stages = VISA_STAGES.get(visa_type, [])
    try:
        current_index = stages.index(current_stage)
        return stages[current_index + 1:]
    except (ValueError, IndexError):
        return ["Invalid current stage or no further stages defined."]

def get_document_details(document_name: str) -> dict:
    """
    Returns details for a specific document (e.g., form name, deadline - use placeholders).
    This is a placeholder and will need to be populated with actual document details.
    """
    # Sample document details
    document_details_map = {
        "Form I-129": {"name": "Form I-129, Petition for a Nonimmigrant Worker", "purpose": "To petition U.S. Citizenship and Immigration Services (USCIS) for a foreign national to come to the United States temporarily to perform services or labor, or to receive training.", "link": "https://www.uscis.gov/i-129"},
        "Passport Copy": {"name": "Copy of Passport", "purpose": "To verify identity and nationality.", "notes": "Ensure passport is valid for at least 6 months beyond intended stay."},
        "DS-160 Confirmation": {"name": "DS-160 Confirmation Page", "purpose": "Confirmation page of the submitted Online Nonimmigrant Visa Application.", "link": "https://ceac.state.gov/genniv/"}
    }
    return document_details_map.get(document_name, {"error": "Document details not found."})

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    print("Available visa types for US:", get_visa_types("US"))
    print("Stages for H-1B visa:", get_visa_stages("H-1B"))
    print("Required documents for H-1B Petition Filing:", get_required_documents("H-1B", "Petition Filing"))
    print("Next steps for F-1 after I-20 Application:", get_immigration_steps("US", "F-1", "I-20 Application"))
    print("Details for Form I-129:", get_document_details("Form I-129"))
    print("Details for a non-existent document:", get_document_details("Imaginary Form"))
    print("Visa types for an unknown country:", get_visa_types("XYZ"))
    print("Stages for an unknown visa type:", get_visa_stages("XYZ Visa"))
    print("Documents for H-1B at 'Random Stage':", get_required_documents("H-1B", "Random Stage"))
    print("Next steps for H-1B at 'Visa Stamping' (last stage):", get_immigration_steps("US", "H-1B", "Visa Stamping"))
    print("Next steps for H-1B at 'Invalid Stage':", get_immigration_steps("US", "H-1B", "Invalid Stage"))
    print(get_visa_types("CA"))
    print(get_visa_stages("Work Permit"))
    print(get_required_documents("F-1","Visa Interview"))
