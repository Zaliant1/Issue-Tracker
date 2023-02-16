const express = require("express");
const router = express.Router();
const Issue = require("../db/db");

router.get("/", async (req, res) => {
  try {
    const getIssues = await Issue.find();
    res.json(getIssues);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get("/:id", async (req, res) => {
  try {
    const getIssueById = await Issue.findById(req.params.id);
    res.json(getIssueById);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post("/findexact", async (req, res) => {
  try {
    const getIssueByContent = await Issue.find(req.body).exec();
    console.log(getIssueByContent);
    res.json(getIssueByContent);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get("/category/:category", async (req, res) => {
  const getIssuesByCategory = await Issue.find({
    category: req.params.category,
  }).exec();
  res.send(getIssuesByCategory);
  console.log(getIssuesByCategory);
});

router.put("/", async (req, res) => {
  const issue = new Issue(req.body);

  try {
    const newIssue = await issue.save();
    res.status(201).json(newIssue);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

router.post("/:id", async (req, res) => {
  const issue = await Issue.findById(req.params.id);

  for (let i in req.body) {
    if (i === "__v" || i === "_id") {
      continue;
    }

    issue[i] = req.body[i];
  }

  const newIssue = await issue.save();

  res.send(newIssue.toJSON());
});

router.delete("/:id", async (req, res) => {
  const issueToDelete = await Issue.findById(req.params.id);

  try {
    await issueToDelete.remove();
    res.send(200);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
