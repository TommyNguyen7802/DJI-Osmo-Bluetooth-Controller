OmniControl UI
==========================================

A responsive, high-performance remote control interface featuring a dynamic grid layout, livestream video, and real-time telemetry.

PREREQUISITES
------------------------------------------
1. Node.js (v18 or higher) - For building the frontend.
2. Python 3.x - For running the server script (optional).

QUICK START (DEVELOPMENT)
------------------------------------------
1. Open a terminal in this directory.
2. Install dependencies:
   npm install

3. Start the development server:
   npm run dev

   This will launch the UI in your default browser at http://localhost:5173.
   The UI automatically adjusts to the device's resolution.

BUILDING FOR PRODUCTION
------------------------------------------
To create a production-ready build:
   npm run build

This creates a 'dist' folder containing the compiled HTML, CSS, and JavaScript.

RUNNING WITH PYTHON
------------------------------------------
Per your request for Python code integration:

1. First, build the project:
   npm run build

2. Run the provided Python server script:
   python server.py

3. Open http://localhost:8000 in your browser.

PROJECT STRUCTURE
------------------------------------------
- /src             : React source code
- /components      : UI components (Video, DPad, Logs)
- server.py        : Python host script
- vite.config.ts   : Build configuration
- package.json     : Dependency list

NOTES
------------------------------------------
- The UI is fully responsive and locks scrolling to function like a native app.
- Video playback defaults to a sample stream. You can input your own stream URL in the UI settings.
