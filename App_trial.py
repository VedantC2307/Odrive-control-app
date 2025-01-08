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
        self.ip_entry.insert(0, "localhost")

        self.port_label = ctk.CTkLabel(tcp_frame, text="Port:")
        self.port_label.grid(row=0, column=2, padx=10, pady=5)
        self.port_entry = ctk.CTkEntry(tcp_frame, corner_radius=10)
        self.port_entry.grid(row=0, column=3, padx=10, pady=5)
        self.port_entry.insert(0, "12345")

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

        # Data Recording Frame
        data_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        data_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.topic_label = ctk.CTkLabel(data_frame, text="Topic Name:")
        self.topic_label.grid(row=0, column=0, padx=10, pady=5)

        self.topic_entry = ctk.CTkEntry(data_frame, corner_radius=10)
        self.topic_entry.grid(row=0, column=1, padx=10, pady=5)

        self.topic_entry1 = ctk.CTkEntry(data_frame, corner_radius=10)
        self.topic_entry1.grid(row=1, column=1, padx=10, pady=5)

        self.file_label = ctk.CTkLabel(data_frame, text="File Name:")
        self.file_label.grid(row=0, column=2, padx=10, pady=5)
        self.file_entry = ctk.CTkEntry(data_frame, corner_radius=10)
        self.file_entry.grid(row=0, column=3, padx=10, pady=5)

        # Toggle button for start/stop recording
        self.is_recording = False
        self.start_recording_btn = ctk.CTkButton(data_frame, text="Start", corner_radius=10, hover_color="#357ABD", command=self.toggle_recording)
        self.start_recording_btn.grid(row=0, column=4, padx=10, pady=5)

        # Main container frame for Motor State and Buttons
        main_container_frame = ctk.CTkFrame(self.gradient_frame, corner_radius=15)
        main_container_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        main_container_frame.grid_columnconfigure(0, weight=1)
        main_container_frame.grid_columnconfigure(1, weight=1)
        
        # Motor Toggle Frame (Left Side)
        motor_frame = ctk.CTkFrame(main_container_frame, corner_radius=15)
        motor_frame.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="w")

        motor_label = ctk.CTkLabel(motor_frame, text="Motor State", font=("Arial", 14, "bold"))
        motor_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.motor_state_switch = ctk.CTkSwitch(motor_frame, text=" ", onvalue="CLOSED LOOP", offvalue="IDLE", command=self.toggle_motor_state)
        self.motor_state_switch.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.motor_state_switch.deselect()  # Set default state to "IDLE"

        # Display current state label next to the switch
        self.current_state_label = ctk.CTkLabel(motor_frame, text="IDLE", font=("Arial", 14))
        self.current_state_label.grid(row=1, column=1, padx=(0,100), pady=5, sticky="w")

        # Controller & Odrive Node Start Button Frame (Right Side)
        motor_frame1 = ctk.CTkFrame(main_container_frame, corner_radius=15)
        motor_frame1.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="e")

        self.odrive_node_active = False
        self.controller_active = False
        self.odrive_node_btn = ctk.CTkButton(motor_frame1, text="Start Odrive Node", corner_radius=10, command=self.toggle_odrive_node)
        self.odrive_node_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.controller_btn = ctk.CTkButton(motor_frame1, text="Start Controller", corner_radius=10, command=self.toggle_controller)
        self.controller_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")


    def toggle_odrive_node(self):
        self.odrive_node_active = not self.odrive_node_active
        command = "Start Odrive Node" if self.odrive_node_active else "Stop Odrive Node"
        self.odrive_node_btn.configure(text=command)
        self.send_tcp_message(command)

    def toggle_controller(self):
        self.controller_active = not self.controller_active
        command = "Start Controller" if self.controller_active else "Stop Controller"
        self.controller_btn.configure(text=command)
        self.send_tcp_message(command)

    def send_tcp_message(self, message):
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
        print(current_state)
        
        # Send motor state over TCP
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(current_state.encode('utf-8'))
                print(f"Sent motor state command: {current_state}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending motor state command: {e}")


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

    def toggle_recording(self):
        if not self.is_recording:
            # Start recording
            self.is_recording = True
            self.start_recording()
            self.start_recording_btn.configure(text="Stop")
        else:
            # Stop recording
            self.is_recording = False
            self.stop_recording()
            self.start_recording_btn.configure(text="Start")

    def start_recording(self):
        topic_name = self.topic_entry.get()
        topic_name_1 = self.topic_entry1.get()
        file_name = self.file_entry.get()

        # Create the message based on the available topic names
        message = f"{self.is_recording},{topic_name}"
        if topic_name_1:
            message += f",{topic_name_1}"
        message += f",{file_name}"

        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print(f"Recording started for Topic: {message}")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

    def stop_recording(self):
        file_name = self.file_entry.get()
        message = f"{self.is_recording},{file_name}"
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.sendall(message.encode('utf-8'))
                print("Recording stopped.")
            else:
                print("No active connection. Please connect to the server first.")
        except Exception as e:
            print(f"Error sending command: {e}")

if __name__ == '__main__':
    app = ModernApp()
    app.mainloop()
