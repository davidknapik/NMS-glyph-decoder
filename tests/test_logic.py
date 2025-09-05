"""
Unit tests for the logic functions in the NMS address decoder.

This script tests the portal-to-galactic coordinate conversion logic
without any dependency on screen reading or image recognition.
"""
import os
import sys
import unittest

# --- Setup for Importing from Parent Directory ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import the function we want to test
from nms_address import portal_to_galactic_coords

class TestCoordinateConversion(unittest.TestCase):
    """Test suite for the portal_to_galactic_coords function."""

    # A dictionary of known portal codes and their expected galactic coordinate outputs.
    # Format: "PORTAL_CODE": "XXXX:YYYY:ZZZZ:SSSS"
    # Data is sourced from the NMS community and known locations.
    KNOWN_CONVERSIONS = {
        "107AFA92914D" : "094C:0079:0128:007A", # Address from TestImage01
        "13F1024185B8" : "0DB7:0081:0C17:03F1", # Address from TestImage02
        "10EF004175B8" : "0DB7:007F:0C16:00EF", # Address from TestImage03
        "10D6024185B8" : "0DB7:0081:0C17:00D6", # Address from TestImage04
        "122CF79B1D82" : "0581:0076:01B0:022C", # Address from TestImage05
        "109A039BAE4B" : "064A:0082:01B9:009A", # Pilgram Star
    }
    
    def test_known_addresses(self):
        """
        Tests several known portal addresses against their correct galactic coordinates.
        This will help verify the offset math in the conversion function.
        """
        for portal_code, expected_coords in self.KNOWN_CONVERSIONS.items():
            # The 'with self.subTest(...)' block allows us to see which specific
            # portal code failed if there is an issue, instead of the whole test failing.
            with self.subTest(portal_code=portal_code):
                
                # Run the conversion function from your main script
                actual_coords, _ = portal_to_galactic_coords(portal_code)
                
                # Assert that the actual result matches the expected result
                self.assertEqual(actual_coords, expected_coords,
                                 f"Conversion failed for portal code {portal_code}")

    def test_invalid_code_handling(self):
        """
        Tests that the function correctly handles invalid input by returning (None, None).
        """
        invalid_codes = [
            "12345",         # Too short
            "0123456789ABCDEF", # Too long
            "",              # Empty string
            None,            # None value
            "GHIJKLMNOPQRSTUVWXYZ"   # Contains invalid hex characters
        ]
        
        for code in invalid_codes:
            with self.subTest(invalid_code=code):
                result = portal_to_galactic_coords(code)
                self.assertEqual(result, (None, None),
                                 f"Function did not correctly handle invalid code: {code}")


# This allows the script to be run directly from the command line
if __name__ == '__main__':
    unittest.main(verbosity=2)