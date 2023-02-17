require("dotenv").config();
const mongoose = require("mongoose");
const express = require("express");
const cors = require("cors");

const app = express();
app.use(express.json());

const password = encodeURIComponent(`${process.env.PASSWORD}`);

const URI = `mongodb+srv://${process.env.USERNAME}:${password}@${process.env.CLUSTER}/?retryWrites=true&w=majority`;

try {
  mongoose.connect(URI);
  console.log("connected to mongodb");
} catch (error) {
  console.error(error);
}

const issueRouter = require("./routes");
app.use("/api/issue", issueRouter);

app.listen(8000, () => {
  console.log("server up on 8000");
});
