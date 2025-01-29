# ODrive TCP/IP Control App

[![Example App Image](link_to_your_app_screenshot.png)](link_to_your_app_screenshot.png)

A modern, user-friendly application built with CustomTkinter for controlling ODrive motor controllers over TCP/IP. This application allows users to set control modes, send commands, and manage motor states for their ODrive setups.

## Table of Contents
*   [Features](#features)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Usage](#usage)
*   [How it Works](#how-it-works)
*   [Configuration](#configuration)
*   [Contributing](#contributing)
*   [License](#license)
*   [Credits](#credits)
*   [Contact](#contact)


## Features

*   **Modern UI:** Built with `customtkinter` for a clean and responsive user interface.
*   **TCP/IP Communication:** Connect to your ODrive via a configurable IP address and port.
*   **Control Mode Selection:** Choose between Position, Velocity, and Torque control modes.
*   **Command Sending:** Send numerical values for your selected control mode.
*   **Motor State Management:** Toggle motor between 'IDLE' and 'CLOSED LOOP' modes.
*   **ODrive Setup Functions:** Includes options to initialize ODrive, clear errors, and perform calibration routines.
*   **Graceful Exit:** Handles keyboard interrupts (Ctrl+C) for a smooth exit.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.7+:** Make sure you have Python 3.7 or a more recent version.
*   **CustomTkinter:**  Install `customtkinter` with pip.
*   **An ODrive Setup:** An ODrive motor controller and a server application running on the ODrive or a connected host which accepts TCP/IP messages like Raspberry Pi.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/VedantC2307/Odrive-control-app.git 
    cd Odrive-control-app
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  **Run the application:**

    ```bash
    python App.py
    ```

2.  **Connect to your ODrive:**
    *   Enter the IP address and port of your ODrive's TCP/IP server in the respective fields.
    *   Click "Connect".

3.  **Select Control Mode:**
    *   Choose your desired control mode (Position, Velocity, or Torque).

4.  **Send Commands:**
    *   Enter the value you want to send in the text field.
    *   Click the "Send" button.

5.  **Control the Motor State:**
     *  Toggle the motor between "IDLE" and "CLOSED LOOP" using the toggle switch.

6.  **Use the ODrive setup buttons**
     *  You can use buttons to intialise the odrive, clear errors and carryout motor calibration

7.  **Disconnect:**
    *   Click the "Disconnect" button when finished.

## How it Works

This app interacts with the ODrive using TCP/IP sockets. When you enter commands in the app, they're sent as strings to the server associated with your ODrive. The server on the ODrive or connected host interprets these messages and adjusts the motor control accordingly.

The main.py implements this behaviour and takes the user input to perform this task. The customtkinter library provides the means to create the GUI and allow the user to have a visual interface to interact with.

## Configuration

*   The default IP and Port is 172.26.33.8:1234. You may need to change them as required.

## Credits
This project was built using Python and the customtkinter library.
