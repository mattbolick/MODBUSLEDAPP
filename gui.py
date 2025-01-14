import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import modbus_client
import utils
from PIL import Image, ImageTk

class RGBControllerGUI:
    def __init__(self, master):
        self.master = master
        master.title("RGB LED Controller")
        self.rotation_interval = 3000  # 3 seconds in milliseconds
        self.rotation_task = None  # To keep track of the rotation task
        self.is_rotating = False  # Add a flag to indicate rotation state
        self.current_color_index = 0 # Keep track of the current color index

        # --- Load and display the logo ---
        try:
            self.logo_image = Image.open("logo.png")
            self.logo_image = self.logo_image.resize((240, 28), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(master, image=self.logo_photo)
            self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw", columnspan=2)
        except FileNotFoundError:
            print("Logo image not found. Skipping logo display.")

        # --- Add custom text ---
        self.custom_text = tk.Label(master, text="FortiLED Modbus Control", font=("Arial", 14, "bold"))
        self.custom_text.grid(row=1, column=0, padx=10, pady=10, sticky="nw", columnspan=2)

        self.modbus_client = modbus_client.ModbusClient()

        # --- Connection Frame ---
        self.connection_frame = ttk.LabelFrame(master, text="Connection")
        self.connection_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.ip_label = ttk.Label(self.connection_frame, text="IP Address:")
        self.ip_label.grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = ttk.Entry(self.connection_frame)
        self.ip_entry.insert(0, "192.168.11.66")
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        self.port_label = ttk.Label(self.connection_frame, text="Port:")
        self.port_label.grid(row=1, column=0, padx=5, pady=5)
        self.port_entry = ttk.Entry(self.connection_frame)
        self.port_entry.insert(0, "502")
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)

        self.connect_button = ttk.Button(self.connection_frame, text="Connect", command=self.connect_to_modbus)
        self.connect_button.grid(row=2, column=0, padx=5, pady=5)

        self.disconnect_button = ttk.Button(self.connection_frame, text="Disconnect", command=self.disconnect_from_modbus, state="disabled")
        self.disconnect_button.grid(row=2, column=1, padx=5, pady=5)

        self.status_label = ttk.Label(self.connection_frame, text="Status: Disconnected", foreground="red")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # --- Color Control Frame ---
        self.color_frame = ttk.LabelFrame(master, text="Color Control")
        self.color_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.red_label = ttk.Label(self.color_frame, text="Red:")
        self.red_label.grid(row=0, column=0, padx=5, pady=5)
        self.red_slider = ttk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color)
        self.red_slider.grid(row=0, column=1, padx=5, pady=5)

        self.green_label = ttk.Label(self.color_frame, text="Green:")
        self.green_label.grid(row=1, column=0, padx=5, pady=5)
        self.green_slider = ttk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color)
        self.green_slider.grid(row=1, column=1, padx=5, pady=5)

        self.blue_label = ttk.Label(self.color_frame, text="Blue:")
        self.blue_label.grid(row=2, column=0, padx=5, pady=5)
        self.blue_slider = ttk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_color)
        self.blue_slider.grid(row=2, column=1, padx=5, pady=5)

        self.color_preview = tk.Canvas(self.color_frame, width=100, height=100, bg="black")
        self.color_preview.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.color_picker_button = ttk.Button(self.color_frame, text="Pick Color", command=self.open_color_picker)
        self.color_picker_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.send_button = ttk.Button(self.color_frame, text="Send Color", command=self.send_color)
        self.send_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # --- Rotation Control Frame ---
        self.rotation_frame = ttk.LabelFrame(master, text="Rotation Control")
        self.rotation_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.rotate_button = ttk.Button(self.rotation_frame, text="Start Rotation", command=self.toggle_rotation)
        self.rotate_button.grid(row=0, column=0, padx=5, pady=5)

        self.lights_off_button = ttk.Button(self.rotation_frame, text="Lights Off", command=self.lights_off)
        self.lights_off_button.grid(row=0, column=1, padx=5, pady=5)

    def connect_to_modbus(self):
        ip_address = self.ip_entry.get()
        port = int(self.port_entry.get())

        if self.modbus_client.connect(ip_address, port):
            self.status_label.config(text="Status: Connected", foreground="green")
            self.connect_button.config(state="disabled")
            self.disconnect_button.config(state="normal")  # Enable disconnect button
        else:
            self.status_label.config(text="Status: Connection Failed", foreground="red")

    def disconnect_from_modbus(self):
        self.modbus_client.disconnect()
        self.status_label.config(text="Status: Disconnected", foreground="red")
        self.connect_button.config(state="normal")  # Re-enable connect button
        self.disconnect_button.config(state="disabled")  # Disable disconnect button

    def update_color(self, event=None):
        red = int(self.red_slider.get())
        green = int(self.green_slider.get())
        blue = int(self.blue_slider.get())
        hex_color = utils.rgb_to_hex(red, green, blue)
        self.color_preview.config(bg=hex_color)

    def open_color_picker(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[0]:
            rgb = [int(c) for c in color_code[0]]
            self.red_slider.set(rgb[0])
            self.green_slider.set(rgb[1])
            self.blue_slider.set(rgb[2])
            self.update_color()

    def send_color(self):
        red = int(self.red_slider.get())
        green = int(self.green_slider.get())
        blue = int(self.blue_slider.get())

        if self.modbus_client.is_connected:
            self.modbus_client.write_color(red, green, blue)
            print(f"Sent Color: R={red}, G={green}, B={blue}")
        else:
            print("Not connected to Modbus server.")
            self.status_label.config(text="Status: Not Connected", foreground="red")

    def toggle_rotation(self):
        if self.is_rotating:
            self.stop_rotation()
        else:
            self.start_rotation()

    def start_rotation(self):
        self.is_rotating = True
        self.rotate_button.config(text="Stop Rotation")
        self.rotation_task = self.master.after(self.rotation_interval, self.rotate_colors)

    def stop_rotation(self):
        self.is_rotating = False
        self.rotate_button.config(text="Start Rotation")
        if self.rotation_task is not None:
            self.master.after_cancel(self.rotation_task)
            self.rotation_task = None

    def rotate_colors(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

        if self.modbus_client.is_connected:
            red, green, blue = colors[self.current_color_index]
            self.modbus_client.write_color(red, green, blue)
            print(f"Sent Color: R={red}, G={green}, B={blue}")

            # Update sliders and preview
            self.red_slider.set(red)
            self.green_slider.set(green)
            self.blue_slider.set(blue)
            self.update_color()

            self.current_color_index = (self.current_color_index + 1) % len(colors)

        if self.is_rotating:  # Check if still rotating
            self.rotation_task = self.master.after(self.rotation_interval, self.rotate_colors)

    def lights_off(self):
        if self.modbus_client.is_connected:
            self.modbus_client.write_color(0, 0, 0)
            print("Sent Color: R=0, G=0, B=0")

            # Update sliders and preview
            self.red_slider.set(0)
            self.green_slider.set(0)
            self.blue_slider.set(0)
            self.update_color()