WRoboControl UI (WIP: Updated March 2, 2026)
==========================================

A responsive, high-performance remote control interface featuring a dynamic grid layout, livestream video, and real-time telemetry.

PREREQUISITES
------------------------------------------
1. Node.js (v18 or higher) - For building the frontend.
2. Python 3.x - For running the server script.

QUICK START for Webpage (DEVELOPMENT)
------------------------------------------
1. Open a terminal in this directory.
2. Install dependencies:
   
   `npm install`

3. Start the development server:
   
   `npm run dev`

   This will launch the UI in your default browser at http://localhost:3000.
   The UI automatically adjusts to the device's resolution.

BUILDING FOR PRODUCTION
------------------------------------------
To create a production-ready build:
   npm run build

This creates a 'dist' folder containing the compiled HTML, CSS, and JavaScript.

PROJECT STRUCTURE
------------------------------------------
- /components             : UI components (Video, DPad, Logs)
- /aioice                 : Driver library
- /unitree_webrtc_connect : Sample Dog Examples
- test_webrtc_stream.py   : Python test stream
- vite.config.ts          : Build configuration
- package.json            : Dependency list

PYTHON Environment
------------------------------------------
PYTHON Environment has a few dependencies in order to run and communicate with the robotdog and test scripts.
These dependencies can be found in "requirements.txt"

Start with creating a python virtual environment:
```
python -m venv venv
```
Then activate the virtual environment (you have to do this every time you open a new terminal):
```
source venv/bin/activate
```
Now you should install all the dependencies in the virtual environment:
```
pip install -r requirements.txt
```
And now you should be able to run the Python scripts aswell as the React webpage.

NOTES
------------------------------------------
- The UI is fully responsive and locks scrolling to function like a native app.
- Video playback defaults to a sample stream. You can input your own stream URL in the UI settings.
