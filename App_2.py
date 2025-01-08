import customtkinter as ctk
import socket

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Control App")
        self.geometry("800x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Adding a subtle gradient to the main window (using a frame overlay)
        self.gradient_frame = ctk.CTkFrame(self, fg_color=("gray15", "gray25"))
        self.gradient_frame.pack(fill="both", expand=True)

        # TCP Connect Frame
        tcp_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        tcp_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.ip_label = ctk.CTkLabel(tcp_frame, text="IP Address:")
        self.ip_label.grid(row=0, column=0, padx=10, pady=5)
        self.ip_entry = ctk.CTkEntry(tcp_frame, corner_radius=10)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5)
        self.ip_entry.insert(0, "192.168.0.133")

        self.port_label = ctk.CTkLabel(tcp_frame, text="Port:")
        self.port_label.grid(row=0, column=2, padx=10, pady=5)
        self.port_entry = ctk.CTkEntry(tcp_frame, corner_radius=10)
        self.port_entry.grid(row=0, column=3, padx=10, pady=5)
        self.port_entry.insert(0, "1234")

        self.connect_btn = ctk.CTkButton(tcp_frame, text="Connect", corner_radius=10, hover_color="#357ABD", command=self.connect)
        self.connect_btn.grid(row=0, column=4, padx=10, pady=5)
        self.disconnect_btn = ctk.CTkButton(tcp_frame, text="Disconnect", corner_radius=10, hover_color="#D9534F", command=self.disconnect)
        self.disconnect_btn.grid(row=0, column=5, padx=10, pady=5)

        # Control Mode Frame
        control_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        control_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        control_label = ctk.CTkLabel(control_frame, text="Control Mode", font=("Arial", 14, "bold"))
        control_label.grid(row=0, column=0, padx=10, pady=5)

        self.control_mode = ctk.StringVar(value="Position")
        self.position_radio = ctk.CTkRadioButton(control_frame, text="Position", variable=self.control_mode, value="Position", hover_color="#5DADE2")
        self.position_radio.grid(row=1, column=0, padx=10, pady=5)
        self.velocity_radio = ctk.CTkRadioButton(control_frame, text="Velocity", variable=self.control_mode, value="Velocity", hover_color="#5DADE2")
        self.velocity_radio.grid(row=1, column=1, padx=10, pady=5)
        self.torque_radio = ctk.CTkRadioButton(control_frame, text="Torque", variable=self.control_mode, value="Torque", hover_color="#5DADE2")
        self.torque_radio.grid(row=1, column=2, padx=10, pady=5)

        self.value_entry = ctk.CTkEntry(control_frame, placeholder_text="Value", corner_radius=10)
        self.value_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.send_btn = ctk.CTkButton(control_frame, text="Send", corner_radius=10, hover_color="#357ABD", command=self.send_command)
        self.send_btn.grid(row=2, column=2, padx=10, pady=5)

        # Motor Toggle Frame
        motor_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        motor_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        motor_label = ctk.CTkLabel(motor_frame, text="Motor State", font=("Arial", 14, "bold"))
        motor_label.grid(row=0, column=0, padx=10, pady=5)

        self.motor_state_switch = ctk.CTkSwitch(motor_frame, text=" ", onvalue="CLOSED LOOP", offvalue="IDLE", command=self.toggle_motor_state)
        self.motor_state_switch.grid(row=1, column=1, padx=20, pady=5)
        self.motor_state_switch.deselect()  # Set default state to "IDLE"

        # Display current state label
        self.current_state_label = ctk.CTkLabel(motor_frame, text="IDLE", font=("Arial", 14))
        self.current_state_label.grid(row=1, column=2, padx=10, pady=0)

        # Encoder Offset Calibration Button
        self.calibration_btn = ctk.CTkButton(motor_frame, text="ENCODER_OFFSET_CALIBRATION", corner_radius=10, 
                                             command=self.encoder_offset_calibration)
        self.calibration_btn.grid(row=1, column=4, padx=60, pady=5)

    def encoder_offset_calibration(self):
        message = "ENCODER_OFFSET_CALIBRATION"

        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Sent command: {message}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def toggle_motor_state(self):
        # Update the state label based on the toggle switch state
        current_state = self.motor_state_switch.get()
        self.current_state_label.configure(text=current_state)
        # print(current_state)
        message = f"{current_state}"

        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Sent command: {message}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def connect(self):
        ip_address = self.ip_entry.get()
        port = int(self.port_entry.get())

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {ip_address} on port {port}...")
        try:
            self.client_socket.connect((ip_address, port))
            print(f"Successfully connected to {ip_address} on port {port}")
        except Exception as e:
            print(f"Failed to connect to {ip_address} on port {port}: {e}")

    def disconnect(self):
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.close()
                print("Disconnected from the server.")
            else:
                print("No active connection to disconnect.")
        except Exception as e:
            print(f"Error while disconnecting: {e}")

    def send_command(self):
        mode = self.control_mode.get()
        value = self.value_entry.get()

        message = f"{mode}:{value}"
        
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Sent command: {message}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

if __name__ == '__main__':
    app = ModernApp()
    app.mainloop()
