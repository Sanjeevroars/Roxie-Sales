import express from "express";
import { spawn } from "child_process";
import path from "path";
import cors from "cors";

const app = express();
const port = 3001;

app.use(cors());

app.get("/run-exe", (req, res) => {
  const exePath = path.join(
    "C:",
    "Users",
    "hp",
    "Downloads",
    "roxie",
    "dell",
    "qt_output.exe"
  );

  const exeDirectory = path.join(
    "C:",
    "Users",
    "hp",
    "Downloads",
    "roxie",
    "dell"
  );

  const exeProcess = spawn(exePath, [], {
    cwd: exeDirectory,
    // detached: true,
    stdio: "ignore",
  });

  exeProcess.on("error", (error) => {
    console.error(`Error spawning the process: ${error}`);
    return res.status(500).send("Error running the EXE file");
  });

  exeProcess.on("exit", (code) => {
    console.log(`EXE file exited with code ${code}`);
    res.send("EXE file executed successfully");
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
