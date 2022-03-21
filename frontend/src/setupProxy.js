const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  ["/login", "/logout", "/api/*"].forEach((route) => {
    app.use(
      route,
      createProxyMiddleware({
        target: "http://localhost:5000",
        changeOrigin: true,
      })
    );
  });
};
