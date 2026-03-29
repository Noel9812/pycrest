require('dotenv').config();
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS for frontend
app.use(cors({
  origin: process.env.FRONTEND_ORIGIN || 'http://localhost:5173',
  credentials: true,
}));

// Request logging (without body to avoid stream buffering issues with proxy)
app.use(morgan('[:date[iso]] [GATEWAY] :method :url -> :status | :response-time ms'));

// Health check endpoint
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

// Proxy generator function
const generateProxyOptions = (pathPrefix, targetService) => {
  return createProxyMiddleware({
    target: targetService,
    changeOrigin: true,
    xfwd: true,

    pathRewrite: (path, req) => {
      return path.replace(new RegExp(`^${pathPrefix}`), '');
    },

    onError: (err, req, res) => {
      console.error(`[Proxy Error] ${req.method} ${req.url} -> ${targetService}`, err);
      res.status(503).json({
        error: 'Service unavailable',
        service: targetService,
        status: 503
      });
    }
  });
};

// Route mapping table based on Phase 0 analysis
const routes = {
  '/api/auth': process.env.AUTH_SERVICE_URL,
  '/api/admin/emi': process.env.EMI_SERVICE_URL,
  '/api/loans': process.env.LOAN_SERVICE_URL,
  '/api/customer': process.env.LOAN_SERVICE_URL,
  '/api/emi': process.env.EMI_SERVICE_URL,
  '/api/wallet': process.env.WALLET_SERVICE_URL,
  '/api/transactions': process.env.WALLET_SERVICE_URL,
  '/api/payments': process.env.PAYMENT_SERVICE_URL,
  '/api/verification': process.env.VERIFICATION_SERVICE_URL,
  '/api/admin': process.env.ADMIN_SERVICE_URL,
  '/api/support': process.env.ADMIN_SERVICE_URL,
  '/api/manager': process.env.MANAGER_SERVICE_URL,
};

// Register middlewares for routes
for (const [pathPrefix, targetUrl] of Object.entries(routes)) {
  if (targetUrl) {
    app.use(pathPrefix, generateProxyOptions(pathPrefix, targetUrl));
  } else {
    console.warn(`[WARNING] Target URL not defined for ${pathPrefix}`);
  }
}

app.listen(PORT, () => {
  console.log(`\n🚀 API Gateway is running on http://localhost:${PORT}`);
  console.log(`Front-end allowed origin: ${process.env.FRONTEND_ORIGIN || 'http://localhost:5173'}`);
});
