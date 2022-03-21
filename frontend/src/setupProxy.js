/*const createProxyMiddleware = require("http-proxy-middleware");

module.exports = function (app) {
  ["/login", "/api/*"].forEach((route) => {
    app.use(
      route,
      createProxyMiddleware({
        target: "http://localhost:5000",
        changeOrigin: true,
      })
    );
  });
};*/
const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:5000",
      changeOrigin: true,
    })
  );
  app.use(
    "/login",
    createProxyMiddleware({
      target: "http://localhost:5000",
      changeOrigin: true,
    })
  );
};
