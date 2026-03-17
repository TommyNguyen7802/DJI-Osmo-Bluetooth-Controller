import express from "express";
import { exec } from "child_process";

const app = express();
// Change depending on machine!
const dji_python_script = "python3 /home/mason/Desktop/Repos/Senior-Capstone-Project/DJI-Osmo-Bluetooth-Controller/DJI\ Scripts/compiled_main.py"

app.post("/run-dji-backend-script", (req, res) => {
    exec(dji_python_script, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).send("Failed to run script");
        }

        console.log(stdout);
        console.error(stderr);

        res.send("Script started");
    });
});

app.listen(8010, () => {
    console.log("Server running on port 8010");
});