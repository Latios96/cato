const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  ["/login", "/logout", "/auth", "/api/*"].forEach((route) => {
    app.use(
      route,
      createProxyMiddleware({
        target: "http://127.0.0.1:5000/",
        changeOrigin: true,
      })
    );
  });
};
