const mongoose = require("mongoose");

const issueSchema = new mongoose.Schema({
  status: String,
  summary: String,
  category: String,
  type: String,
  priority: String,
  playerName: String,
  version: String,
  description: String,
  modLogs: {
    title: String,
    body: String,
  },
  archived: Boolean,
  attachments: {
    embedSource: String ? String : null,
    generalUrl: String ? String : null,
  },
});

module.exports = mongoose.model("Issue", issueSchema);
