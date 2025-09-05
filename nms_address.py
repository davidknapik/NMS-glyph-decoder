"""
Main routine for No Man's Sky screenshot address decoder.

This script detects a 12-character portal address on the screen,
decodes it, and converts it into galactic coordinates.
"""
import sys
import time
import logging
import pyautogui

# --- Configuration ---

# Set to True to prevent the script from moving the mouse to the top-left corner
# of the screen and raising an exception.
pyautogui.FAILSAFE = True

# Configure logging to show informational messages.
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# A dictionary mapping glyph characters to their corresponding image filenames.
SYMBOL_FILES = {
    "0": "symbol_0.png", "1": "symbol_1.png", "2": "symbol_2.png", "3": "symbol_3.png",
    "4": "symbol_4.png", "5": "symbol_5.png", "6": "symbol_6.png", "7": "symbol_7.png",
    "8": "symbol_8.png", "9": "symbol_9.png", "A": "symbol_a.png", "B": "symbol_b.png",
    "C": "symbol_c.png", "D": "symbol_d.png", "E": "symbol_e.png", "F": "symbol_f.png"
}

# A list of tuples defining the screen region for each of the 12 glyph locations.
# Each tuple is in the format (left, top, width, height).
GLYPH_LOCATIONS = [
    (10, 1015, 32, 32),   # Location 0 (Planet)
    (43, 1015, 32, 32),   # Location 1 (System - 1)
    (75, 1015, 32, 32),   # Location 2 (System - 2)
    (107, 1015, 32, 32),  # Location 3 (System - 3)
    (139, 1015, 32, 32),  # Location 4 (Y - 1)
    (171, 1015, 32, 32),  # Location 5 (Y - 2)
    (203, 1015, 32, 32),  # Location 6 (Z - 1)
    (235, 1015, 32, 32),  # Location 7 (Z - 2)
    (267, 1015, 32, 32),  # Location 8 (Z - 3)
    (299, 1015, 32, 32),  # Location 9 (X - 1)
    (331, 1015, 32, 32),  # Location 10 (X - 2)
    (363, 1015, 32, 32)   # Location 11 (X - 3)
]

# --- Core Functions ---

def detect_symbol(region, confidence=0.9):
    """
    Detects which glyph symbol is present in a given screen region.

    Args:
        region (tuple): The (left, top, width, height) of the screen region to search.
        confidence (float): The confidence level for image matching.

    Returns:
        str: The character ('0'-'F') of the detected symbol, or None if no symbol is found.
    """
    for symbol, filename in SYMBOL_FILES.items():
        try:
            if pyautogui.locateOnScreen(filename, region=region, confidence=confidence):
                logging.info(f"Detected symbol '{symbol}' in region {region}.")
                return symbol

        except pyautogui.ImageNotFoundException as e:
            logging.debug(f"Image not found {symbol} @ {region}: {e}")

        except pyautogui.PyAutoGUIException as e:
            # This can happen if the image file is not found.
            logging.error(f"Error processing {filename}: {e}")
            # To avoid repeated errors for the same missing file, we can exit.
            sys.exit(1)
        except Exception as e:
            # Catch other potential exceptions, though less likely.
            logging.warning(f"An unexpected error occurred for {filename} in {region}: {e}")
            
    logging.warning(f"No symbol detected in region {region}.")
    return None


def get_portal_code():
    """
    Scans all glyph locations on the screen and assembles the full 12-character portal code.

    Returns:
        str: The complete 12-character portal code, or None if any symbol is not detected.
    """
    portal_code = ""
    for i, location in enumerate(GLYPH_LOCATIONS):
        symbol = detect_symbol(location)
        if symbol:
            portal_code += symbol
        else:
            logging.error(f"Could not decode symbol at location {i+1}. Aborting.")
            return None
    return portal_code


def portal_to_galactic_coords(portal_code):
    """
    Converts a 12-digit portal code into galactic coordinates.

    Args:
        portal_code (str): The 12-character portal code.

    Returns:
        tuple: A tuple containing the galactic coordinates string and the original portal code.
               Returns (None, None) if the portal code is invalid.
    """
    if not portal_code or len(portal_code) != 12:
        logging.error("Invalid portal code provided.")
        return None, None

    # Extract components from the portal code: P SSS YY ZZZ XXX
    p = portal_code[0]
    sss = portal_code[1:3]
    yy = portal_code[4:5]
    zzz = portal_code[6:8]
    xxx = portal_code[9:11]

    # Convert hex components to integers
    p_dec = int(p, 16)
    sss_dec = int(sss, 16)
    yy_dec = int(yy, 16)
    zzz_dec = int(zzz, 16)
    xxx_dec = int(xxx, 16)

    # Apply offsets for galactic coordinates calculation
    x_offset = xxx_dec - 2047
    y_offset = yy_dec - 127
    z_offset = zzz_dec - 2047
    
    # Format the final galactic coordinates string: XXXX:YYYY:ZZZZ:SSSS
    galactic_coordinates = (f"{x_offset:04X}:{y_offset:04X}:{z_offset:04X}:{sss_dec:04X}")

    return galactic_coordinates, portal_code

# --- Main Execution ---

def main():
    """
    Main function to run the portal address decoder continuously.
    """
    logging.info("Starting No Man's Sky Portal Decoder. Press Ctrl+C to exit.")
    
    while True:
        try:
            print("-" * 30)
            logging.info("Attempting to decode portal address...")
            
            # 1. Get the full portal code from the screen
            code = get_portal_code()

            if code:
                logging.info(f"Successfully decoded Portal Code: {code}")
                
                # 2. Convert the portal code to galactic coordinates
                galactic_coords, _ = portal_to_galactic_coords(code)

                if galactic_coords:
                    print(f"\n--- Decoded Address ---")
                    print(f"Portal Code: {code}")
                    print(f"Galactic Coordinates: {galactic_coords}\n")
            
            # Wait for a couple of seconds before trying again
            time.sleep(2)

        except KeyboardInterrupt:
            logging.info("Script stopped by user.")
            sys.exit(0)
        except Exception as e:
            logging.error(f"An unexpected error occurred in the main loop: {e}")
            time.sleep(5) # Wait a bit longer after an unexpected error

if __name__ == "__main__":
    main()