module.exports = {
  apps: [
    {
      name: "aiems-frontend",
      cwd: "/opt/aeims/website/frontend",
      script: "npm",
      args: "start",
      env: {
        NODE_ENV: "production",
        PORT: 3000,
      },
    },
  ],
};