// Modules to control application life and create native browser window
const {ipcMain, app, BrowserWindow} = require('electron')
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

  run_zmq(mainWindow)

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

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.


// function to create ZMQ client socket.
async function run_zmq(mainWindow) {
  sock = new zmq.Pair

  sock.connect("tcp://127.0.0.1:3001")
  console.log("Client bound to port 3001.")

  // send message
  data = {
    "type": "POST",
    "data": "Hello"
  }
  await sock.send(JSON.stringify(data))

  // print recieved reply
  const [msg] = await sock.receive()
  console.log("Client recieved: " + msg)

  while (true) {
    // listen to socket
    const [msg] = await sock.receive()
    var msgObj = JSON.parse(msg.toString())
    if(msgObj.fun == "updateSong"){
      // send event
      mainWindow.webContents.send("newSong",
        {newSong: msgObj.data.song, newArtist: msgObj.data.artist, newDuration: msgObj.data.duration, newArt: msgObj.data.art, newCurrTime: msgObj.data.currTime, newCurrPerc: msgObj.data.currPerc}
      )
    }
  }
}

var python_server = null
// function to spawn the main python process
function spawn_python_server(){
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
function kill_python_server(){
  python_server.kill()
  python_server = null
}

ipcMain.on("scrobbleSong", (event, args) => {
  sock.send(JSON.stringify(args))
})

app.on("ready", spawn_python_server)

app.on("will-quit", kill_python_server)
