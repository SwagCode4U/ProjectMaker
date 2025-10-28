# backend/app/services/frameworks/backend/koa.py
from pathlib import Path
from typing import Dict


def normalize(v: str) -> str:
    return 'koa'


def meta() -> Dict:
    return {'id': 'koa', 'port': 3000}


def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    return {
        'name': name,
        'type': 'directory',
        'children': [
            {
                'name': 'src', 'type': 'directory', 'children': [
                    {'name': 'controllers', 'type': 'directory', 'children': [
                        {'name': 'message.controller.js', 'type': 'file'},
                    ]},
                    {'name': 'middlewares', 'type': 'directory', 'children': [
                        {'name': 'errorHandler.js', 'type': 'file'},
                    ]},
                    {'name': 'routes', 'type': 'directory', 'children': [
                        {'name': 'message.routes.js', 'type': 'file'},
                    ]},
                    {'name': 'app.js', 'type': 'file'},
                    {'name': 'server.js', 'type': 'file'},
                    {'name': 'websocket.js', 'type': 'file'},
                    {'name': 'config.js', 'type': 'file'},
                ]
            },
            {'name': 'package.json', 'type': 'file'},
            {'name': '.env', 'type': 'file'},
        ]
    }


def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        # Dirs
        (base / 'src' / 'controllers').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'middlewares').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'routes').mkdir(parents=True, exist_ok=True)

        files: Dict[str, str] = {
            'package.json': """{
  "name": "koa-boilerplate",
  "version": "1.0.0",
  "private": true,
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js"
  },
  "dependencies": {
    "koa": "^2.13.4",
    "koa-router": "^10.0.0",
    "koa-bodyparser": "^4.4.0",
    "dotenv": "^10.0.0",
    "ws": "^8.0.0",
    "@koa/cors": "^5.0.0"
  },
  "devDependencies": {
    "nodemon": "^2.0.12"
  }
}
""",
            '.env': """PORT=3000
""",
            'src/config.js': """const { config } = require('dotenv');
config();
module.exports = { PORT: process.env.PORT || 3000 };
""",
            'src/app.js': """const Koa = require('koa');
const Router = require('koa-router');
const cors = require('@koa/cors');
const bodyParser = require('koa-bodyparser');
const messageRoutes = require('./routes/message.routes');
const errorHandler = require('./middlewares/errorHandler');

const app = new Koa();
const router = new Router();

app.use(cors());
app.use(bodyParser());
app.use(errorHandler);
app.use(router.routes()).use(router.allowedMethods());

app.use(messageRoutes.routes()).use(messageRoutes.allowedMethods());

module.exports = app;
""",
            'src/server.js': """const http = require('http');
const app = require('./app');
const { PORT } = require('./config');
const startWebSocketServer = require('./websocket');

const server = http.createServer(app.callback());
startWebSocketServer(server);

server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
""",
            'src/middlewares/errorHandler.js': """module.exports = async (ctx, next) => {
  try {
    await next();
  } catch (err) {
    ctx.status = err.status || 500;
    ctx.body = { message: err.message };
    ctx.app.emit('error', err, ctx);
  }
};
""",
            'src/routes/message.routes.js': """const Router = require('koa-router');
const { sendMessage } = require('../controllers/message.controller');

const router = new Router();
router.post('/api/messages', sendMessage);

module.exports = router;
""",
            'src/controllers/message.controller.js': """const messages = [];

module.exports.sendMessage = async (ctx) => {
  const { content } = ctx.request.body || {};
  if (typeof content !== 'string' || !content.trim()) {
    ctx.status = 400;
    ctx.body = { message: 'content is required' };
    return;
  }
  messages.push(content);
  ctx.body = { message: 'Message received', content };
};
""",
            'src/websocket.js': """const WebSocket = require('ws');

module.exports = function startWebSocketServer(server) {
  const wss = new WebSocket.Server({ server });
  wss.on('connection', (ws) => {
    ws.on('message', (message) => {
      for (const client of wss.clients) {
        if (client.readyState === WebSocket.OPEN) {
          client.send(message.toString());
        }
      }
    });
  });
};
""",
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return {'operations': ops, 'errors': errs, 'backend_type': 'koa'}
