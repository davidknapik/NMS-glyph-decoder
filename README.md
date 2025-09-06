# No Man's Sky Portal Decoder

An interactive Python utility that automates the decoding of No Man's Sky portal glyphs directly from your screen. The script uses image recognition to read the 12-glyph address and converts it into the corresponding Galactic Coordinates, saving you from manual transcription errors.

---

## Features

-   **On-Demand Screen Capture**: Press a key to instantly read the glyphs visible on your screen. No need for screenshots.
-   **Portal to Galactic Coordinate Conversion**: Automatically converts the 12-character portal code into the standard `XXXX:YYYY:ZZZZ:SSSS` format.
-   **Interactive CLI**: Simple and clear command-line interface. Just run the script and press keys when prompted.
-   **Robust and Testable**: Includes a full testing suite to verify both image recognition and coordinate conversion logic.
-   **Organized Project Structure**: Code, image assets, and tests are cleanly separated for easy maintenance and contribution.

---

## Requirements

-   **Python 3.6+**
-   **Screen Resolution**: The script is currently hardcoded for a **1920x1080** resolution. The glyphs must appear at their default location on the screen in photo mode.
-   **Operating System**: Works on Windows. Untested on macOS and Linux.
    -   **Linux Users**: This script requires `sudo` privileges to access keyboard events. You must run it with `sudo python nms_address.py`.

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/davidknapik/no-mans-sky-decoder.git
    cd no-mans-sky-decoder
    ```
2. **Set up Virtual env
    ```bash
    python -m venv .venv
    ```
3. **Activate Virtual env
    ```bash
    .\.venv\Scripts\activate
    ```
4.  **Upgrade pip and Install the required Python packages:**
    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

5.  **Verify Asset Location**: Ensure the 16 glyph images (`symbol_0.png` through `symbol_f.png`) are located inside the `assets/symbols/` directory.

6.  **Run self tests
   ```bash
    python .\tests\run_tests.py
   ```
   ```bash
   python .\tests\test_logic.py
   ```

---

## How to Use

1.  **Run the script** from the project's root directory:
    ```bash
    python nms_address.py
    ```

2.  You will see the following message in your terminal:
    ```
    --- No Man's Sky Portal Decoder ---

    Press [`] while glyphs are visible in photo mode.
    Press [ctrl+c] to quit the application.
    ------------------------------
    ```

3.  **In No Man's Sky**, activate your camera (photo mode). Once the 12 glyphs are visible at the bottom-left of your screen (usually in Photo Mode), switch back to the terminal.

4.  **Press the '`' key.** The script will immediately scan the predefined screen locations, detect the glyphs, and print the decoded address.

    ```
    --- Decoded Address ---
    Portal Code: 1:07A:FA:929:14D
    Galactic Coordinates: 094C:0079:0128:007A
    ```

5.  **Press `ctrl+c`** at any time to quit the application.

---

## How It Works

The script uses the following core components:

-   **PyAutoGUI**: A powerful library used to perform image recognition on the screen. It takes small template images of the glyphs (from the `assets/symbols/` folder) and searches for them in specific, hardcoded regions of the screen.
-   **Keyboard**: A simple library used to listen for global key presses (`SPACE` and `Q`) to trigger the detection cycle and to quit the application.
-   **Coordinate Logic**: The `portal_to_galactic_coords` function contains the mathematical conversion logic, which involves applying specific offsets and modular arithmetic to translate the portal code into galactic coordinates.

---

## Testing the Application

The project includes a comprehensive test suite to ensure everything works as expected.

### 1. Integration Test (Image Recognition)

This test displays a full-screen image and runs the actual `pyautogui` detection logic against it.

-   **Setup**: Place your own full-screen (1920x1080) test PNGs inside the `tests/test_images/` directory. Open `tests/run_tests.py` and update the `TEST_CASES` dictionary to map your image filenames to their known, correct portal codes.
-   **Run**:
    ```bash
    python tests/run_tests.py
    ```

### 2. Unit Test (Conversion Logic)

This test validates the `portal_to_galactic_coords` function without any screen interaction, ensuring the math is correct.

-   **Setup**: You can add your own known portal-to-coordinate pairs to the `KNOWN_CONVERSIONS` dictionary in `tests/test_logic.py`.
-   **Run**:
    ```bash
    python tests/test_logic.py
    ```

---
## Troubleshooting

### WARNING:root:No symbol detected in region (xxx)
    Typically this occurs if there is not enough contrast between the symbols and the background.

    Best results is if you move the camera so the background behind the symobls is dark, and consistent.
    Might be able to lower the confidence variable.

## Contributing

Contributions are welcome! If you have ideas for new features, find a bug, or want to improve the code, please feel free to open an issue or submit a pull request.

Areas for future improvement could include:
-   Support for different screen resolutions.
-   A graphical user interface (GUI).
-   Automatic detection of when glyphs are on-screen.
-   Better symbol detection when there is less consistent background

---

## License


This project is licensed under the MIT License. See the `LICENSE` file for details.
