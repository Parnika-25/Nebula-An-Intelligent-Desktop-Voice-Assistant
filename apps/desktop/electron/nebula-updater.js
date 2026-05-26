const { autoUpdater } = require("electron-updater");
const { app } = require("electron");

function initAutoUpdater() {
  autoUpdater.checkForUpdatesAndNotify();

  autoUpdater.on("update-downloaded", () => {
    autoUpdater.quitAndInstall();
  });
}

app.whenReady().then(initAutoUpdater);
