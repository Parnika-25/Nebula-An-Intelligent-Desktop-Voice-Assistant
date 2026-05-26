  const { contextBridge } = require("electron");

  contextBridge.exposeInMainWorld("nebula", {
    apiBase: "http://127.0.0.1:5055"
  });
