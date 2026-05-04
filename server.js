const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(path.join(__dirname, 'public')));

// simple endpoint to append logs (tools can POST here or write to a file and this reads it)
app.use(express.json({ limit: '1mb' }));
app.post('/log', (req, res) => {
  const entry = { ts: new Date().toISOString(), ...req.body };
  const line = JSON.stringify(entry) + '\n';
  fs.appendFileSync('tool.log', line);
  io.emit('log', entry);
  res.json({ ok: true });
});

// stream existing log on connect
io.on('connection', (socket) => {
  try {
    if (fs.existsSync('tool.log')) {
      const lines = fs.readFileSync('tool.log', 'utf8').trim().split('\n').slice(-200);
      lines.forEach(l => socket.emit('log', JSON.parse(l)));
    }
  } catch (e) {
    console.error('read log error', e);
  }
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Dashboard running on :${PORT}`));
