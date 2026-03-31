require('dotenv').config();
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

// ── CORS ─────────────────────────────────────────────────────────────────────
const allowedOrigins = [
  'http://localhost:5173',
  'http://localhost:5174',
  'http://localhost:5175',
  'http://44.223.16.184',
  'http://44.223.16.184:80',
];

if (process.env.FRONTEND_ORIGIN) {
  const origin = process.env.FRONTEND_ORIGIN;
  if (!allowedOrigins.includes(origin)) {
    allowedOrigins.push(origin);
  }
}

const corsOptions = {
  origin: (origin, callback) => {
    if (!origin) {
      // Allow requests with no origin (curl, Postman, server-to-server)
      return callback(null, true);
    }

    if (allowedOrigins.includes(origin)) {
      return callback(null, true);
    }

    // Also allow if origin hostname matches FRONTEND_ORIGIN hostname
    // This handles http://IP vs http://IP:80 mismatches
    try {
      const frontendHost = process.env.FRONTEND_ORIGIN
        ? new URL(process.env.FRONTEND_ORIGIN).hostname
        : null;
      const originHost = new URL(origin).hostname;

      if (frontendHost && originHost && frontendHost === originHost) {
        return callback(null, true);
      }
    } catch (e) {
      // invalid URL, fall through to rejection
    }

    callback(new Error(`CORS: origin ${origin} not allowed`));
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'Idempotency-Key', 'X-Internal-Token'],
};

app.use(cors(corsOptions));

// Handle OPTIONS preflight for ALL routes before proxies touch them
app.options('*', cors(corsOptions));

// ── Logging ───────────────────────────────────────────────────────────────────
app.use(morgan('[:date[iso]] [GATEWAY] :method :url -> :status | :response-time ms'));

// ── Health check ──────────────────────────────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    gateway: 'running',
    timestamp: new Date().toISOString(),
    services: {
      'auth-service': process.env.AUTH_SERVICE_URL,
      'loan-service': process.env.LOAN_SERVICE_URL,
      'emi-service': process.env.EMI_SERVICE_URL,
      'wallet-service': process.env.WALLET_SERVICE_URL,
      'payment-service': process.env.PAYMENT_SERVICE_URL,
      'verification-service': process.env.VERIFICATION_SERVICE_URL,
      'admin-service': process.env.ADMIN_SERVICE_URL,
      'manager-service': process.env.MANAGER_SERVICE_URL,
    }
  });
});

// ── Proxy factory ─────────────────────────────────────────────────────────────
const generateProxyOptions = (pathPrefix, targetService) => {
  return createProxyMiddleware({
    target: targetService,
    changeOrigin: true,
    xfwd: true,
    pathRewrite: (path) => path.replace(new RegExp(`^${pathPrefix}`), ''),
    onError: (err, req, res) => {
      console.error(`[Proxy Error] ${req.method} ${req.url} -> ${targetService}`, err.message);
      res.status(503).json({ error: 'Service unavailable', service: targetService, status: 503 });
    }
  });
};

// ── Route table ───────────────────────────────────────────────────────────────
const routes = {
  '/api/auth':         process.env.AUTH_SERVICE_URL,
  '/api/admin/emi':    process.env.EMI_SERVICE_URL,
  '/api/loans':        process.env.LOAN_SERVICE_URL,
  '/api/customer':     process.env.LOAN_SERVICE_URL,
  '/api/emi':          process.env.EMI_SERVICE_URL,
  '/api/wallet':       process.env.WALLET_SERVICE_URL,
  '/api/transactions': process.env.WALLET_SERVICE_URL,
  '/api/payments':     process.env.PAYMENT_SERVICE_URL,
  '/api/verification': process.env.VERIFICATION_SERVICE_URL,
  '/api/admin':        process.env.ADMIN_SERVICE_URL,
  '/api/support':      process.env.ADMIN_SERVICE_URL,
  '/api/manager':      process.env.MANAGER_SERVICE_URL,
};

for (const [pathPrefix, targetUrl] of Object.entries(routes)) {
  if (targetUrl) {
    app.use(pathPrefix, generateProxyOptions(pathPrefix, targetUrl));
  } else {
    console.warn(`[WARNING] No URL configured for ${pathPrefix}`);
  }
}

// ── Start ─────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`\n🚀 API Gateway is running on http://localhost:${PORT}`);
  console.log(`Front-end allowed origins: ${allowedOrigins.join(', ')}`);
});