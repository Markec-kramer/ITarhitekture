const express = require("express");
const path = require("path");
const usersRoutes = require("./routes/usersRoutes");

const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));

app.use("/api/users", usersRoutes);

module.exports = app;