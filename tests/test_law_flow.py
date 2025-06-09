import unittest
from ..law_flow import (
    get_visa_types,
    get_visa_stages,
    get_required_documents,
    get_immigration_steps,
    VISA_TYPES,
    VISA_STAGES,
    REQUIRED_DOCUMENTS
)

class TestLawFlow(unittest.TestCase):

    def test_get_visa_types(self):
        """Test getting visa types for a known country."""
        country_code = "US" # Known country from VISA_TYPES
        visa_types = get_visa_types(country_code)
        self.assertIsInstance(visa_types, list)
        self.assertEqual(visa_types, VISA_TYPES.get(country_code))
        # Test for an unknown country
        self.assertEqual(get_visa_types("XX"), [])

    def test_get_visa_stages(self):
        """Test getting visa stages for a known visa type."""
        visa_type = "H-1B" # Known visa type from VISA_STAGES
        stages = get_visa_stages(visa_type)
        self.assertIsInstance(stages, list)
        self.assertEqual(stages, VISA_STAGES.get(visa_type))
        # Test for an unknown visa type
        self.assertEqual(get_visa_stages("Unknown Visa"), [])

    def test_get_required_documents(self):
        """Test getting required documents for a known visa type and stage."""
        visa_type = "H-1B"
        stage = "Petition Filing" # Known stage for H-1B
        documents = get_required_documents(visa_type, stage)
        self.assertIsInstance(documents, list)
        self.assertEqual(documents, REQUIRED_DOCUMENTS.get((visa_type, stage)))
        # Test for an unknown stage or visa type
        self.assertEqual(get_required_documents(visa_type, "Unknown Stage"), [])
        self.assertEqual(get_required_documents("Unknown Visa", stage), [])

    def test_get_immigration_steps(self):
        """Test getting immigration steps."""
        country = "US"
        visa_type = "F-1"
        current_stage = "I-20 Application" # A stage that has subsequent stages

        steps = get_immigration_steps(country, visa_type, current_stage)
        self.assertIsInstance(steps, list)

        all_stages_for_visa = VISA_STAGES.get(visa_type, [])
        if current_stage in all_stages_for_visa:
            current_index = all_stages_for_visa.index(current_stage)
            expected_steps = all_stages_for_visa[current_index + 1:]
            self.assertEqual(steps, expected_steps)
        else:
            self.assertIn("Invalid current stage", steps[0])

        # Test with last stage
        last_stage = VISA_STAGES.get(visa_type, [])[-1] if VISA_STAGES.get(visa_type) else "SomeStage"
        steps_at_last_stage = get_immigration_steps(country, visa_type, last_stage)
        self.assertEqual(steps_at_last_stage, []) # Expect empty list if it's the last stage

        # Test with invalid stage
        steps_invalid_stage = get_immigration_steps(country, visa_type, "Invalid Stage")
        self.assertIsInstance(steps_invalid_stage, list)
        self.assertTrue("Invalid current stage" in steps_invalid_stage[0])

if __name__ == '__main__':
    unittest.main()
