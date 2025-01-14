# RGB LED Controller

This application provides a graphical user interface (GUI) for controlling an RGB LED light via MODBus TCP. You can set the LED to any color, rotate through red, green, and blue colors, and turn the LED off. This app was designed specifically for the RESI-1LED-ETH, but other MODBus LED devices may work. 

## Features

*   Connect to an RGB LED controller using MODBus TCP.
*   Set the LED color using sliders or a color picker.
*   Display a color preview.
*   Rotate through red, green, and blue colors at a configurable interval.
*   Turn off the LED.
*   Display connection status.
*   Customizable logo and application title.

## Installation

### Prerequisites

*   **Python:**  This application requires Python 3.7 or higher. You can download it from [python.org](https://www.python.org/).
*   **MODBus RGB LED Controller:** You need an RGB LED light/controller that supports MODBus TCP communication. Ensure you know its IP address, port, and MODBus register addresses for controlling the color. his app was designed specifically for the RESI-1LED-ETH, but other MODBus LED devices may work. 
https://www.resi.cc/resi/catalog/files/RESI-CATALOG-GATEWAYS-EN-Pages/RESI-CATALOG-GATEWAYS-EN-GW-48-RESI-1LED-ETH.pdf

### Steps

1.  **Clone the Repository (Optional):**

    If the project is hosted on a platform like GitHub, you can clone it using Git:

    ```bash
    git clone https://github.com/mattbolick/MODBUSLEDAPP
    cd main
    ```

    If you don't want to use Git, you can download the project as a ZIP file and extract it.

2.  **Install Required Libraries:**

    Open a terminal or command prompt and install the following Python libraries using `pip`:

    ```bash
    pip install pymodbus Pillow
    ```


3.  **Place Your Logo (Optional):**

    If you want to use a custom logo, place your logo image file (e.g., `logo.png`) in the same directory as the application files. Edit the `gui.py` file and update the `Image.open("logo.png")` line with the correct filename if necessary.

## Running the Application

1.  **Configure MODBus Settings:**

    *   Open the `gui.py` file.
    *   Locate the `ip_entry` and `port_entry` initial values:
        *   Change the default IP address (`"192.168.1.10"`) to the actual IP address of your RGB LED controller.
        *   Change the default port (`"502"`) if your controller uses a different MODBus TCP port.
    *   Locate the `modbus_client.write_color()` function in `modbus_client.py`:
        *   **Important:** Verify and modify the MODBus register addresses (currently set to `0` for the starting address) and the unit/slave ID (currently set to `0xFF` or `255`) according to your LED controller's documentation.

2.  **Run the Application:**

    *   **Python:** Open a terminal, navigate to the application directory, and run:

        ```bash
        python main.py
        ```

3.  **Using the Application:**

    *   Enter the IP address and port of your LED controller (if you didn't modify the defaults in the code).
    *   Click the **Connect** button. The status label will indicate if the connection was successful.
    *   Use the sliders or the color picker to set the desired color. Click **Send Color** to update the LED.
    *   Click **Start Rotation** to cycle through red, green, and blue colors every 3 seconds. Click **Stop Rotation** to stop.
    *   Click **Lights Off** to turn off the LED.
    *   Click **Disconnect** to disconnect from the LED controller.

## Versions

*   **Python:**
    *   **Language:** Python 3.7+
    *   **Libraries:**
        *   `tkinter` (built-in)
        *   `pymodbus` (for MODBus communication)
        *   `Pillow` (for image/logo handling)

## Troubleshooting

*   **Connection Issues:**
    *   Double-check the IP address, port, and MODBus settings.
    *   Ensure that your LED controller is powered on and connected to the network.
    *   Check your firewall settings to make sure that MODBus TCP traffic (usually port 502) is allowed.
*   **Logo Not Displayed:**
    *   Verify that the logo image file is in the correct directory and that the filename is correct in the `gui.py` (or `gui/gui.go`) file.
    *   Make sure you have installed the `Pillow` library for the Python version.
*   **MODBus Errors:**
    *   Consult your LED controller's documentation for the correct MODBus register addresses and unit/slave ID.

## License

This project is licensed under the GNU GPL version 3 license - see the LICENSE file for details. 