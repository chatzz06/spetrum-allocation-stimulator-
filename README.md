Spectrum Allocation Simulator


📌 Overview

The Spectrum Allocation Simulator is a software project designed to simulate the allocation of available frequency spectrum among multiple users or devices. It demonstrates how spectrum resources can be assigned efficiently using allocation algorithms.

The project is organized into separate modules for algorithms, frontend resources, HTML templates, application logic, and database storage.

✨ Features

Spectrum allocation simulation.
Algorithm-based channel assignment.
Management of available spectrum resources.
Web-based user interface.
SQLite database integration.
Local execution through the terminal.
Browser access through a localhost URL.
🛠️ Technologies Used
Python — Application logic and backend processing.
HTML — Web page structure.
CSS — User interface styling.
JavaScript — Frontend interactions, if implemented.
SQLite — Database storage.
Terminal / Command Prompt — Application execution.
📂 Project Structure
Spectrum-Allocation-Simulator/
│
├── __pycache__/
├── algorithms/
├── static/
├── templates/
├── App.py
└── database.db

File and Folder Description
File / Folder	Description
__pycache__/	Stores automatically generated Python bytecode files.
algorithms/	Contains the spectrum allocation algorithms.
static/	Stores static assets such as CSS, JavaScript, and images.
templates/	Contains HTML templates for the web interface.
App.py	Main Python application entry point.
database.db	SQLite database used for application data.
⚙️ Installation and Setup
1. Clone the Repository
git clone https://github.com/chatzz06/Spectrum-Allocation-Simulator.git

2. Navigate to the Project Directory
cd Spectrum-Allocation-Simulator

3. Install Dependencies

If the application uses Flask, install it with:

pip install flask


Install any additional dependencies required by the project.

4. Run the Application

Start the application using:

python App.py


If your system uses Python 3 through a separate command, run:

python3 App.py

5. Access the Application

After starting the application, check the terminal for the local server URL.

For example:

http://127.0.0.1:5000


Open the URL displayed in your terminal in a web browser. The actual address and port depend on the application's configuration.

💻 Finding Your Local IP Address

To find your computer's local network IP address, use the appropriate terminal command.

Windows

ipconfig


Look for the IPv4 Address under your active network adapter.

Linux

hostname -I


macOS

ipconfig getifaddr en0


Note: localhost and 127.0.0.1 refer to your own computer. Your local network IP address is different and may be required if you want to access the application from another device on the same network. The server must be configured to accept network connections for this to work.

🔄 How It Works

Start the application from the terminal.
Open the localhost URL in a web browser.
Provide the required inputs through the application interface.
Execute the spectrum allocation algorithm.
View the resulting channel assignments and allocation status.

The exact workflow depends on the algorithms and features implemented in the project.

🚀 Future Enhancements
Visualize spectrum allocation using graphical charts.
Implement additional spectrum allocation algorithms.
Add channel interference detection.
Support dynamic allocation based on user demand.
Compare the performance of different allocation strategies.
Improve spectrum utilization and resource management.
👨‍💻 Author

chatzz06

GitHub: https://github.com/chatzz06

📝 Conclusion

The Spectrum Allocation Simulator provides a practical way to explore spectrum management and resource allocation in wireless communication systems. Its modular structure separates allocation algorithms, application logic, frontend resources, templates, and database storage.

The application can be started through the terminal and accessed locally through a web browser using the server URL displayed during execution.
