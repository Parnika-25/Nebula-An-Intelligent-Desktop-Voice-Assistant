const { Tray, Menu, app } = require("electron");
const path = require("path");

let tray = null;

function createTray() {
  tray = new Tray(path.join(__dirname, "icon.png"));

  const contextMenu = Menu.buildFromTemplate([
    { label: "Nebula AI Running", enabled: false },
    { type: "separator" },
    {
      label: "Open Nebula",
      click: () => {
        app.emit("activate");
      }
    },
    {
      label: "Exit",
      click: () => {
        app.quit();
      }
    }
  ]);

  tray.setToolTip("Nebula AI");
  tray.setContextMenu(contextMenu);
}

module.exports = { createTray };
