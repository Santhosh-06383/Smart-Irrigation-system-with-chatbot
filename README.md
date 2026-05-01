🔷 Project Title

Smart Irrigation System using IoT with Telegram Bot Integration

🔷 Overview

This project presents an intelligent IoT-based irrigation system that automates water supply to plants based on real-time soil moisture conditions. It integrates hardware, cloud services, and a chatbot interface to enable both automatic and manual control of irrigation.

The system uses a NodeMCU microcontroller to monitor soil moisture and control a water pump via a relay module. Data is stored and synchronized using Firebase Realtime Database, while a Telegram bot provides remote user interaction through a backend REST API deployed on Render.

🔷 Key Features
🌱 Automatic Irrigation based on soil moisture threshold
📱 Remote Control via Telegram Bot
☁️ Real-time Data Monitoring using Firebase
🔄 Manual + Auto Mode Switching
⚡ Low-cost and energy-efficient design
🌍 Cloud-connected smart agriculture solution
🔷 System Architecture

The system consists of three main layers:

1. Hardware Layer
NodeMCU (ESP8266)
Soil Moisture Sensor
5V Relay Module
Water Pump
Power Supply

2. Cloud & Backend Layer
Firebase Realtime Database (data storage & sync)
REST API (Python-based backend)
Render (cloud deployment)

3. User Interface Layer
Telegram Bot for:
Motor ON/OFF control
Mode switching (Auto/Manual)
Status monitoring

🔷 Working Principle
Soil moisture sensor continuously reads soil condition
NodeMCU processes the data
If moisture is below threshold → Motor turns ON automatically
Data is updated to Firebase in real time
User can control system remotely via Telegram bot
Backend processes Telegram commands and updates Firebase
NodeMCU reads updates and performs actions accordingly

🔷 Technologies Used
Embedded C - Arduino IDE
ESP8266 (NodeMCU)
Firebase Realtime Database
Python (Backend API)
Telegram Bot API
Render (Cloud Deployment)
IoT Communication (Wi-Fi based)


🔷 Project Workflow
Moisture Sensor → NodeMCU → Firebase → Backend → Telegram Bot  
                                   ↓  
                      
                               Relay → Motor Pump
🔷 Applications
Smart Agriculture
Home Gardening Automation
Water Resource Management
Precision Farming Systems

🔷 Advantages
Reduces water wastage
Minimizes manual effort
Enables remote monitoring
Cost-effective and scalable

🔷 Limitations
Requires stable internet connection
Sensor calibration needed for accuracy


🔷 Future Enhancements
Integration with weather forecasting APIs
AI-based irrigation prediction
Mobile app dashboard
Solar-powered system
Multiple sensor support for large farms

🔷 Authors
Santhosh Kumar S, Antony Praveen S, Veera Prakash S
B.E. Electrical and Electronics Engineering

🔷Guided by
Dr. T. Rakesh, ASP/EEE
Department of Electrical and Electronics Engineering
Mepco Schlenk Engineering College, Sivakasi

🔷 How to Run 
1. Clone the repository
2. Upload Arduino code to NodeMCU
3. Configure Firebase credentials
4. Deploy backend on Render
5. Connect Telegram Bot
6. Power the system
