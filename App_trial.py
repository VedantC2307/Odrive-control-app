import customtkinter as ctk
import socket
import threading

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Control App")
        self.geometry("800x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Initialize socket to None
        self.client_socket = None

        # Adding a gradient frame
        self.gradient_frame = ctk.CTkFrame(self, fg_color=("gray15", "gray25"))
        self.gradient_frame.pack(fill="both", expand=True)

        # Initialize all UI components
        self.init_tcp_frame()
        self.init_control_frame()
        self.init_data_frame()
        self.init_motor_frame()

    def init_tcp_frame(self):
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

    def connect(self):
        ip_address = self.ip_entry.get()
        port = self.port_entry.get()

        if not self.client_socket:  # Avoid multiple connections
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connecting to {ip_address} on port {port}...")
            try:
                threading.Thread(target=self.client_socket.connect, args=((ip_address, int(port)),)).start()
                print(f"Successfully connected to {ip_address} on port {port}")
            except Exception as e:
                print(f"Failed to connect to {ip_address} on port {port}: {e}")
                self.client_socket = None

    def disconnect(self):
        if self.client_socket:
            try:
                self.client_socket.close()
                print("Disconnected from the server.")
            except Exception as e:
                print(f"Error while disconnecting: {e}")
            finally:
                self.client_socket = None
        else:
            print("No active connection to disconnect.")

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
    
    def toggle_motor_state(self):
        # Update the state label based on the toggle switch state
        current_state = self.motor_state_switch.get()
        self.current_state_label.configure(text=current_state)
        print(current_state)

if __name__ == '__main__':
    app = ModernApp()
    app.mainloop()
