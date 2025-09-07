"""
Test runner for the No Man's Sky address decoder.

This script displays test images full-screen, runs the glyph detection logic
from the main application, and compares the output to a known correct address.
"""
import os
import sys
import time
import tkinter as tk
from PIL import Image, ImageTk

# --- Test Configuration ---

# This dictionary maps your test image filenames to their known, correct portal codes.
# !! YOU MUST FILL THIS OUT WITH YOUR ACTUAL DATA !!
TEST_CASES = {
    "TestImage01.png": "107AFA92914D",  
    "TestImage02.png": "13F1024185B8",  
    "TestImage03.png": "10EF004175B8",  
    "TestImage04.png": "10D6024185B8",  
    "TestImage05.png": "122CF79B1D82",  

}

# --- Setup for Importing from Parent Directory ---

# This is a standard way to allow a script in a subdirectory to import modules
# from its parent directory.
# We get the path to the 'tests' directory and then go one level up.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now we can import the functions from nms_address.py
from nms_address import get_portal_code, calculate_overall_confidence, get_confidence_rank
# --- Test Execution ---

def run_test(image_path, expected_code):
    """Displays an image, runs detection, and returns the results."""
    
    # Create a full-screen, borderless window
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='black') # Set a black background

    # Load and display the image
    img = Image.open(image_path)
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=tk_img, borderwidth=0)
    label.pack()
    
    # This is a variable that will hold the result from the detection
    detected_code = None
    confidence_scores = []

    try:
        # We must update the window to ensure it is drawn before pyautogui scans it.
        root.update()
        
        # Give the system a brief moment to stabilize the display
        time.sleep(1)

        print(f"\nScanning for glyphs in {os.path.basename(image_path)}...")
        
        # --- Run the actual detection from the main script ---
        # The function now returns a tuple: (code, scores)
        detected_code, confidence_scores = get_portal_code()

    finally:
        # IMPORTANT: Always destroy the window, even if the test fails
        root.destroy()
        
    return detected_code, confidence_scores


def main():
    """Main function to iterate through and run all defined test cases."""
    print("--- Starting NMS Address Decoder Test Suite ---")
    
    # Path to the directory where test images are stored
    images_dir = os.path.join(current_dir, "test_images")
    
    passed_count = 0
    failed_count = 0

    for filename, expected_code in TEST_CASES.items():
        image_path = os.path.join(images_dir, filename)

        if not os.path.exists(image_path):
            print(f"❌ FAIL: Test image not found at {image_path}")
            failed_count += 1
            continue
            
        # Run the test and get both the code and the scores
        actual_code, scores = run_test(image_path, expected_code)
        
        # Calculate overall confidence for a more informative output
        overall_confidence = 0.0
        rank = "N/A"
        if scores:
            overall_confidence = calculate_overall_confidence(scores)
            rank = get_confidence_rank(overall_confidence)

        # Compare the results, focusing on the portal code itself
        if actual_code == expected_code:
            print(f"✅ PASS: Detected code matches expected code.")
            print(f"   - Detected:   {actual_code}")
            print(f"   - Confidence: {overall_confidence:.2%} ({rank})")
            passed_count += 1
        else:
            print(f"❌ FAIL: Detected code does not match expected code!")
            print(f"   - Expected:   {expected_code}")
            print(f"   - Detected:   {actual_code}")
            if scores:
                 print(f"   - Confidence: {overall_confidence:.2%} ({rank})")
            failed_count += 1

    print("\n--- Test Summary ---")
    print(f"Total Tests: {len(TEST_CASES)}")
    print(f"✅ Passed:    {passed_count}")
    print(f"❌ Failed:    {failed_count}")
    print("--------------------")

if __name__ == "__main__":
    main()