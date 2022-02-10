// Modules to control application life and create native browser window
const {app, BrowserWindow} = require('electron')
const path = require('path')
const isDev = require('electron-is-dev')
const zmq = require('zeromq')
const {spawn} = require("child_process")

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    }
  })

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
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  run_zmq()

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
async function run_zmq() {
  const sock = new zmq.Request

  sock.connect("tcp://127.0.0.1:3001")
  console.log("Client bound to port 3001.")

  // send message
  await sock.send("Hello")

  // print recieved reply
  const [msg] = await sock.receive()
  console.log("Client recieved: " + msg)
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

app.on("ready", spawn_python_server)

app.on("will-quit", kill_python_server)