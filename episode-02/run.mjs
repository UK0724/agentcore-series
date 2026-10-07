// Starts agent.py with the environment Node loaded from --env-file (the key is never printed).
import { spawn } from "node:child_process";
spawn("../.venv/Scripts/python.exe", ["-u", "agent.py"], { stdio: "inherit", env: process.env });
