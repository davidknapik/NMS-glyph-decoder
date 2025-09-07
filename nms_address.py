"""
Main routine for No Man's Sky screenshot address decoder.

This script detects a 12-character portal address on the screen,
decodes it, and converts it into galactic coordinates using a
best-match confidence algorithm.
"""
import os
import sys
import time
import logging
import pyautogui
import keyboard
import math # <-- Needed for geometric mean calculation

# --- Configuration ---

# Set to True to prevent the script from moving the mouse to the top-left corner
# of the screen and raising an exception.
pyautogui.FAILSAFE = True

# Configure logging to show informational messages.
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Get the absolute path of the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the symbols folder
SYMBOLS_DIR = os.path.join(BASE_DIR, "assets", "symbols")

# A dictionary mapping glyph characters to their full, absolute image filepaths.
SYMBOL_FILES = {
    "0": os.path.join(SYMBOLS_DIR, "symbol_0.png"),
    "1": os.path.join(SYMBOLS_DIR, "symbol_1.png"),
    "2": os.path.join(SYMBOLS_DIR, "symbol_2.png"),
    "3": os.path.join(SYMBOLS_DIR, "symbol_3.png"),
    "4": os.path.join(SYMBOLS_DIR, "symbol_4.png"),
    "5": os.path.join(SYMBOLS_DIR, "symbol_5.png"),
    "6": os.path.join(SYMBOLS_DIR, "symbol_6.png"),
    "7": os.path.join(SYMBOLS_DIR, "symbol_7.png"),
    "8": os.path.join(SYMBOLS_DIR, "symbol_8.png"),
    "9": os.path.join(SYMBOLS_DIR, "symbol_9.png"),
    "A": os.path.join(SYMBOLS_DIR, "symbol_a.png"),
    "B": os.path.join(SYMBOLS_DIR, "symbol_b.png"),
    "C": os.path.join(SYMBOLS_DIR, "symbol_c.png"),
    "D": os.path.join(SYMBOLS_DIR, "symbol_d.png"),
    "E": os.path.join(SYMBOLS_DIR, "symbol_e.png"),
    "F": os.path.join(SYMBOLS_DIR, "symbol_f.png"),
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

def find_best_symbol(region):
    """
    Finds the symbol that matches the given region with the highest confidence.

    Iterates from confidence 0.99 down to 0.25, checking all 16 symbols at
    each step. The first symbol found is the best possible match.

    Returns:
        tuple: A tuple containing (best_symbol, confidence_score) or (None, 0) if no match is found.
    """
    # Iterate downwards from 99% confidence to 25%
    for i in range(99, 25, -5):
        confidence = i / 100.0
        for symbol, filename in SYMBOL_FILES.items():
            try:
                if pyautogui.locateOnScreen(filename, region=region, confidence=confidence):
                    logging.info(f"Best match is '{symbol}' in {region} with confidence {confidence:.2f}")
                    return symbol, confidence
                
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
                    
    logging.warning(f"No symbol detected in region {region} with confidence > 25%.")
    return None, 0.0


def calculate_overall_confidence(scores):
    """
    Calculates the overall confidence using the Geometric Mean of individual scores.
    Returns 0 if any score is 0 to avoid math errors.
    """
    if not scores or any(s <= 0 for s in scores):
        return 0.0
    
    # Calculate the product of all scores
    product = math.prod(scores)
    # Return the nth root, where n is the number of scores
    return math.pow(product, 1.0 / len(scores))


def get_confidence_rank(score):
    """Converts a numerical confidence score (0.0-1.0) into a ranking."""
    if score >= 0.75:
        return "High"
    elif score >= 0.50:
        return "Medium"
    elif score >= 0.25:
        return "Low"
    else:
        return "None"


def get_portal_code():
    """
    Scans all glyph locations and assembles the portal code and confidence scores.

    Returns:
        tuple: (portal_code, confidence_scores) or (None, []) if any symbol fails.
    """
    portal_code = ""
    confidence_scores = []
    for i, location in enumerate(GLYPH_LOCATIONS):
        symbol, confidence = find_best_symbol(location)
        if symbol:
            portal_code += symbol
            confidence_scores.append(confidence)
        else:
            logging.error(f"Could not decode symbol at location {i+1}. Aborting.")
            return None, []
            
    return portal_code, confidence_scores


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
    sss = portal_code[1:4]
    yy = portal_code[4:6]
    zzz = portal_code[6:9]
    xxx = portal_code[9:12]

    # Just checking that the string is parsed correctly
    logging.debug(f"{p}:{sss}:{yy}:{zzz}:{xxx}")
    
    # Convert components from hex to integers
    sss_dec = int(sss, 16)
    yy_dec = int(yy, 16)
    zzz_dec = int(zzz, 16)
    xxx_dec = int(xxx, 16)

    # Apply the offsets. These values are confirmed to work with the wrapping logic.
    x_coord = xxx_dec - 2049
    y_coord = yy_dec - 129
    z_coord = zzz_dec - 2049
    
    # This wrapping logic is ESSENTIAL for the coordinate system.
    # It ensures that coordinates are always represented as positive hex values.
    if x_coord < 0:
        x_coord += 4096
    if y_coord < 0:
        y_coord += 256
    if z_coord < 0:
        z_coord += 4096

    # Format the final galactic coordinates string: XXXX:YYYY:ZZZZ:SSSS
    galactic_coordinates = (f"{x_coord:04X}:{y_coord:04X}:{z_coord:04X}:{sss_dec:04X}")

    return galactic_coordinates, portal_code


def run_detection_cycle():
    """
    Runs one full cycle of detection, conversion, and confidence analysis.
    """
    print("#" * 60)
    logging.info("Scanning for portal address using best-match algorithm...")
    
    # 1. Get the full portal code from the screen
    code, scores = get_portal_code()
    if code:
        logging.info(f"Successfully decoded Portal Code: {code}")
        
        # 2. Convert the portal code to galactic coordinates
        galactic_coords, _ = portal_to_galactic_coords(code)
        
        # Calculate and rank the overall confidence
        overall_confidence = calculate_overall_confidence(scores)
        rank = get_confidence_rank(overall_confidence)

        # 3. Output the results
        if galactic_coords:
            print(f"\n--- Decoded Address ---")
            print(f"Portal Code:          {code[0]}:{code[1:4]}:{code[4:6]}:{code[6:9]}:{code[9:12]}")
            print(f"Galactic Coordinates: {galactic_coords}")
            print(f"Overall Confidence:   {overall_confidence:.2%} ({rank})") # Formats as percentage
            print(f"Individual Scores:    {[f'{s:.2%}' for s in scores]}")
            print("")

    print("#" * 60)

# --- Main Execution ---

def main():
    """
    Main function to run the portal address decoder on keypress.
    Waits for user to press '`' to capture or 'ctrl+c' to quit.
    """
    print("--- No Man's Sky Portal Decoder ---")
    print("\nPress [`] while glyphs are visible in photo mode.")
    print("Press [ctrl+c] to quit the application.")
    print("#" * 60)
    
    while True:
        try:
            # Wait for the next key press event
            key_event = keyboard.read_event()
            
            # We only care about the moment the key is pressed down
            if key_event.event_type == keyboard.KEY_DOWN:
                
                # If the defined key was pressed, run the detection
                if key_event.name == '`':
                    run_detection_cycle()
                    # After running, prompt the user again for clarity
                    print("Ready. Press [`] to capture again or [ctrl+c] to quit.")
                
                # If 'q' was pressed, exit the application
                elif key_event.name == 'ctrl+c':
                    logging.info("ctrl+c' pressed. Exiting application.")
                    break  # Exit the while loop
                    
        except KeyboardInterrupt:
            logging.info("Script stopped by user (Ctrl+C).")
            break
        except Exception as e:
            logging.error(f"An unexpected error occurred in the main loop: {e}")
            break

if __name__ == "__main__":
    main()