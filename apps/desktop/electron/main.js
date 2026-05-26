const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
require("./tray");

let backendProcess;

function startBackend() {
  const exePath = path.join(
    process.resourcesPath,
    "backend",
    "nebula_backend.exe"
  );

  backendProcess = spawn(exePath, [], {
    windowsHide: true
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 900,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js")
    }
  });

  win.loadFile(path.join(__dirname, "../ui/dist/index.html"));
  startBackend();
}

app.whenReady().then(createWindow);
