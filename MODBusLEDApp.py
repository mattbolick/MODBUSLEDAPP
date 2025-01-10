import tkinter as tk
from pymodbus.client.sync import ModbusTcpClient

class RGBControllerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("RGB LED Controller")

        # Modbus TCP client setup
        self.client = ModbusTcpClient('192.168.1.100')  # Replace with your Modbus server IP

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Red component
        self.red_label = tk.Label(self.master, text="Red:")
        self.red_label.grid(row=0, column=0, padx=10, pady=10)
        self.red_scale = tk.Scale(self.master, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color)
        self.red_scale.grid(row=0, column=1, padx=10, pady=10)

        # Green component
        self.green_label = tk.Label(self.master, text="Green:")
        self.green_label.grid(row=1, column=0, padx=10, pady=10)
        self.green_scale = tk.Scale(self.master, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color)
        self.green_scale.grid(row=1, column=1, padx=10, pady=10)

        # Blue component
        self.blue_label = tk.Label(self.master, text="Blue:")
        self.blue_label.grid(row=2, column=0, padx=10, pady=10)
        self.blue_scale = tk.Scale(self.master, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color)
        self.blue_scale.grid(row=2, column=1, padx=10, pady=10)

        # Apply button
        self.apply_button = tk.Button(self.master, text="Apply", command=self.apply_color)
        self.apply_button.grid(row=3, column=0, columnspan=2, pady=10)

    def update_color(self, event=None):
        # Get the current RGB values
        red = self.red_scale.get()
        green = self.green_scale.get()
        blue = self.blue_scale.get()

        # Update the background color of the window to show the selected color
        self.master.configure(bg=f'#{red:02x}{green:02x}{blue:02x}')

    def apply_color(self):
        # Get the current RGB values
        red = self.red_scale.get()
        green = self.green_scale.get()
        blue = self.blue_scale.get()

        # Send the RGB values to the Modbus server
        self.client.write_registers(0, [red, green, blue])
        print(f"Applied color: R={red}, G={green}, B={blue}")

    def close(self):
        # Close the Modbus client connection
        self.client.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RGBControllerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
