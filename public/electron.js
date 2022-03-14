// Modules to control application life and create native browser window
const {dialog, ipcMain, app, BrowserWindow} = require('electron')
const path = require('path')
const isDev = require('electron-is-dev')
const zmq = require('zeromq')
const {spawn} = require("child_process")
var sock;

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  // hide the menu options (Files, Edit, ect)
  mainWindow.removeMenu()

  // and load the index.html of the app.
  mainWindow.loadURL(
    isDev
      ? "http://localhost:3000"
      : `file://${path.join(__dirname, '../build/index.html')}`
  );

  // Open the DevTools.
  if(isDev){
    mainWindow.webContents.openDevTools({mode: "detach"})
  }

  return mainWindow
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  mainWindow = createWindow()

  runZmq(mainWindow)

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// function to create ZMQ client socket.
async function runZmq(mainWindow) {
  sock = new zmq.Pair

  sock.connect("tcp://127.0.0.1:3001")
  console.log("Client bound to port 3001.")

  // loop and listen for msgs
  while (true) {
    // listen to socket
    const [msg] = await sock.receive()
    var msgObj = JSON.parse(msg.toString())
    console.log(msgObj)
    if(msgObj.fun == "updateSong"){
      // send event
      mainWindow.webContents.send("newSong",
        {newSong: msgObj.data.song, newArtist: msgObj.data.artist, newDuration: msgObj.data.duration, newArt: msgObj.data.art, newCurrTime: msgObj.data.currTime, newCurrPerc: msgObj.data.currPerc}
      )
    }
    else if(msgObj.fun == "errorMsg"){
      // display error msg
      dialog.showMessageBox(mainWindow, {message: msgObj.data.msg, type: "info", title: msgObj.data.title})
    }
  }
}

var python_server = null
// function to spawn the main python process
function spawnPythonServer(){
  let main_path = path.join(__dirname, "../backend", "main.py")
  python_server = spawn("python", [main_path])
  if(python_server != null){
    console.log("Python server spawned.")
    python_server.stdout.on("data", (data) =>{
      console.log("PYTHON: " + data)
    });
    python_server.stderr.on("data", (data) =>{
      console.log("PYTHON:\n" + data)
    });
  }
}

// function to kill main python process
function killPythonServer(){
  python_server.kill()
  python_server = null
}

// async IPC replies
ipcMain.on("scrobbleSong", (event, args) => {
  sock.send(JSON.stringify(args))
})

ipcMain.on("scrobbleMic", (event, args) => {
  sock.send(JSON.stringify(args))
})

app.on("ready", spawnPythonServer)

app.on("will-quit", killPythonServer)
