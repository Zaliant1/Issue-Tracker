import React, { useState, useEffect, useContext } from "react";
import { UserContext } from "../../context/authprovider.component";
import axios from "axios";

import {
  Radio,
  FormControlLabel,
  FormControl,
  FormLabel,
  TextField,
  MenuItem,
  Button,
  Stack,
  Grid,
  Alert,
  AlertTitle,
  CircularProgress,
  IconButton,
} from "@mui/material/";
import RadioGroup from "@mui/material/RadioGroup";
import SendIcon from "@mui/icons-material/Send";
import RefreshIcon from "@mui/icons-material/Refresh";

export const UserForm = (props) => {
  const { tokenInfo } = useContext(UserContext);
  const [categories, setCategories] = useState([]);
  const [modlogsButtonColor, setModlogsButtonColor] = useState("primary");
  const [modlogsButtonText, setModlogsButtonText] = useState("Upload Modlogs");
  const [embedHelperValidation, setEmbedHelperValidation] = useState("");
  const [generalHelperValidation, setGeneralHelperValidation] = useState("");
  const [embedFieldColor, setEmbedFieldColor] = useState("primary");
  const [generalFieldColor, setgeneralFieldColor] = useState("primary");
  const [submitFormColor, setSubmitFormColor] = useState("primary");
  const [submitFormText, setSubmitFormText] = useState("Submit");
  const [newIssue, setNewIssue] = useState(
    props.issue || {
      status: "reported",
      summary: "",
      category: "",
      type: "",
      priority: "",
      playerData: {
        name: !tokenInfo.data.username ? "" : tokenInfo.data.username,
        id: !tokenInfo.data.id ? "" : tokenInfo.data.id,
        avatar: !tokenInfo.data.avatar ? "" : tokenInfo.data.avatar,
      },
      version: "",
      description: "",
      modlogs: {
        title: "",
        body: "",
      },
      archived: false,
      attachments: {
        embed_source: "",
        general_url: "",
      },
    }
  );

  let updateNewIssue = (field, value) => {
    if (field === "modlogs") {
      const reader = new FileReader();
      reader.readAsText(value);
      reader.onload = () => {
        setNewIssue({
          ...newIssue,
          modlogs: { title: value.name, body: reader.result },
        });
        setModlogsButtonColor("success");
        setModlogsButtonText("Success!");
      };
      reader.onerror = () => {
        console.log("file error", reader.error);
      };
    } else if (field === "attachmentsUrl") {
      setNewIssue({
        ...newIssue,
        attachments: { ...newIssue.attachments, general_url: value },
      });
    } else if (field === "attachmentsEmbedSource") {
      setNewIssue({
        ...newIssue,
        attachments: { ...newIssue.attachments, embed_source: value },
      });
    } else {
      let issue = { ...newIssue };
      issue[field] = value;

      setNewIssue(issue);
    }
  };
  useEffect(() => {
    if (!categories[0]) {
      axios
        .get(`api/project/Pale-Court/categories`)
        .then((res) => setCategories(res.data));
    }

    if (
      newIssue.attachments.general_url.match(
        /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g
      )
    ) {
      setGeneralHelperValidation("Valid URL!");
      setgeneralFieldColor("success");
    } else {
      setGeneralHelperValidation("Please enter a valid URL");
      setgeneralFieldColor("warning");
    }

    if (newIssue.attachments.embed_source.includes("iframe")) {
      setEmbedHelperValidation("Valid Embed!");
      setEmbedFieldColor("success");
    } else {
      setEmbedHelperValidation("Please enter a valid embed link");
      setEmbedFieldColor("warning");
    }
  }, [newIssue, submitFormColor, submitFormText, categories]);

  const handleFormSubmit = async () => {
    await axios.post(`/api/issue/findexact`, newIssue).then((res) => {
      if (res.data) {
        window.alert("this issue already exists");
      } else {
        try {
          let promise;
          let updatedIssue = {
            ...newIssue,
            category: newIssue.category.toLowerCase(),
          };
          if (props.isUpdate) {
            promise = axios
              .put(`/api/issue/${props.issue._id}`, updatedIssue)
              .then(() => window.alert("issue updated!"));
          } else {
            promise = axios.post("/api/issue", updatedIssue);
            console.log(updatedIssue);
          }
          promise.then(() => {
            if (!props.onSubmit) {
              setNewIssue({
                status: "reported",
                summary: "",
                category: "",
                type: "",
                priority: "",
                playerData: {
                  name: !tokenInfo.data.username ? "" : tokenInfo.data.username,
                  id: !tokenInfo.data.id ? "" : tokenInfo.data.id,
                  avatar: !tokenInfo.data.avatar ? "" : tokenInfo.data.avatar,
                },
                version: "",
                description: "",
                modlogs: {
                  title: "",
                  body: "",
                },
                archived: false,
                attachments: {
                  embed_source: "",
                  general_url: "",
                },
              });
              setSubmitFormColor("success");
              setSubmitFormText("Success!");
              setTimeout(() => {
                setSubmitFormColor("primary");
                setSubmitFormText("Submit");
                setModlogsButtonColor("primary");
                setModlogsButtonText("Upload Modlogs");
              }, 500);
            } else {
              props.onSubmit(newIssue);
            }
          });
        } catch (error) {
          console.log(error);
        }
      }
    });
  };

  return !tokenInfo.data ? (
    <div>
      <Alert severity="warning">
        <AlertTitle>Cannot Submit Form</AlertTitle>
        You cannot submit a form —{" "}
        <strong>
          Please login{" "}
          <a href="https://discord.com/api/oauth2/authorize?client_id=1074939657902637058&redirect_uri=http%3A%2F%2F127.0.0.1%3A3000&response_type=code&scope=identify">
            here{" "}
          </a>
          to be able to submit a form for this project
        </strong>
        <br></br>
        <Grid container>
          <h3>
            If you are already logged in and are still seeing this, try
            refreshing the page
          </h3>

          <IconButton onClick={() => window.location.reload()} color="primary">
            <RefreshIcon />
          </IconButton>
        </Grid>
      </Alert>
      <div
        style={{
          position: "absolute",
          left: "55%",
          top: "52%",
          transform: "translate(-50%, -50%)",
        }}
      >
        <CircularProgress />
      </div>
    </div>
  ) : (
    <div>
      <FormControl>
        <Grid container spacing={3}>
          <Grid item md={12}>
            <TextField
              id="summary"
              label="Summary"
              placeholder="Summary"
              multiline
              value={newIssue.summary}
              onChange={(e) => updateNewIssue("summary", e.target.value)}
              fullWidth
            />
          </Grid>

          <Grid item md={4}>
            <Grid container>
              <Grid item md={12}>
                <TextField
                  id="category-select"
                  label="Category"
                  value={newIssue.category}
                  select
                  fullWidth
                  sx={{ pb: 2 }}
                  onChange={(e) => updateNewIssue("category", e.target.value)}
                >
                  <MenuItem defaultValue="none">
                    <em>None</em>
                  </MenuItem>
                  {categories.map((category) => (
                    <MenuItem key={category} value={category}>
                      {category}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item md={12}>
                <TextField
                  id="player-name"
                  label="Player"
                  variant="standard"
                  value={newIssue.playerData.name}
                  defaultValue={tokenInfo.username}
                  onChange={(e) => updateNewIssue("playerName", e.target.value)}
                  sx={{ pb: 2 }}
                  fullWidth
                />
              </Grid>
              <Grid item md={12}>
                <TextField
                  id="version"
                  label="Version"
                  variant="standard"
                  value={newIssue.version}
                  onChange={(e) => updateNewIssue("version", e.target.value)}
                  fullWidth
                />
              </Grid>
            </Grid>
          </Grid>

          <Grid item md={2}>
            <FormLabel id="type-label-group">Type</FormLabel>
            <RadioGroup id="type-radio" sx={{ pb: 3 }}>
              <FormControlLabel
                label="Bug"
                checked={newIssue.type === "bug"}
                value="bug"
                control={
                  <Radio
                    onChange={(e) => updateNewIssue("type", e.target.value)}
                  />
                }
              />
              <FormControlLabel
                label="Suggestion"
                checked={newIssue.type === "suggestion"}
                value="suggestion"
                control={
                  <Radio
                    onChange={(e) => updateNewIssue("type", e.target.value)}
                  />
                }
              />
            </RadioGroup>
          </Grid>

          <Grid item md={2}>
            <FormLabel sx={{ pt: 3 }} id="priority-label-group">
              Priority
            </FormLabel>
            <RadioGroup id="priority-radio" sx={{ pb: 3 }}>
              <FormControlLabel
                label="Low Priority"
                checked={newIssue.priority === "low"}
                value="low"
                control={
                  <Radio
                    onChange={(e) => updateNewIssue("priority", e.target.value)}
                  />
                }
              />
              <FormControlLabel
                label="Medium Priority"
                checked={newIssue.priority === "medium"}
                value="medium"
                control={
                  <Radio
                    onChange={(e) => updateNewIssue("priority", e.target.value)}
                  />
                }
              />
              <FormControlLabel
                label="High Priority"
                checked={newIssue.priority === "high"}
                value="high"
                control={
                  <Radio
                    onChange={(e) => updateNewIssue("priority", e.target.value)}
                  />
                }
              />
            </RadioGroup>
          </Grid>

          <Grid item md={2}>
            <FormLabel sx={{ pt: 3 }} id="status-label-group">
              Status
            </FormLabel>
            <RadioGroup id="status-radio" sx={{ pb: 3 }}>
              <FormControlLabel
                value="reported"
                label="Reported"
                checked={newIssue.status === "reported"}
                control={
                  <Radio
                    onChange={(e) => updateNewIssue("status", e.target.value)}
                  />
                }
              />
              <FormControlLabel
                label="In Progress"
                checked={newIssue.status === "in-progress"}
                value="in-progress"
                control={
                  <Radio
                    onChange={(e) => updateNewIssue("status", e.target.value)}
                  />
                }
              />
              <FormControlLabel
                label="Completed"
                checked={newIssue.status === "completed"}
                value="completed"
                control={
                  <Radio
                    onChange={(e) => {
                      updateNewIssue("status", e.target.value);
                    }}
                  />
                }
              />
              <FormControlLabel
                label="Won't Fix"
                checked={newIssue.status === "won't-fix"}
                value="won't-fix"
                control={
                  <Radio
                    onChange={(e) => updateNewIssue("status", e.target.value)}
                  />
                }
              />
            </RadioGroup>
          </Grid>

          <Grid item md={12}>
            <TextField
              id="description"
              label="Description"
              placeholder="Description"
              multiline
              value={newIssue.description}
              onChange={(e) => updateNewIssue("description", e.target.value)}
              minRows={6}
              maxRows={20}
              fullWidth
              variant="filled"
            />
          </Grid>
          <Grid item md={6}>
            <Button
              color={modlogsButtonColor}
              variant="contained"
              component="label"
            >
              {modlogsButtonText}
              <input
                hidden
                accept="text/*"
                type="file"
                onChange={(e) => updateNewIssue("modlogs", e.target.files[0])}
              />
            </Button>
          </Grid>
          <Grid item md={6}>
            <Grid container spacing={2}>
              <Grid item md={12}>
                <FormLabel sx={{ pt: 3 }} id="attachments-group">
                  Attachments
                </FormLabel>
              </Grid>
              <Grid item md={6}>
                <TextField
                  color={embedFieldColor}
                  id="embed"
                  label="Embed"
                  placeholder="Embed"
                  value={newIssue.attachments.embedSource}
                  onChange={(e) =>
                    updateNewIssue("attachmentsEmbedSource", e.target.value)
                  }
                  helperText={embedHelperValidation}
                  fullWidth
                />
              </Grid>
              <Grid item md={6}>
                <TextField
                  color={generalFieldColor}
                  id="generic"
                  label="URL"
                  placeholder="URL"
                  value={newIssue.attachments.generalUrl}
                  onChange={(e) =>
                    updateNewIssue("attachmentsUrl", e.target.value)
                  }
                  helperText={generalHelperValidation}
                  fullWidth
                />
              </Grid>
            </Grid>
          </Grid>
          <Grid item md={12}>
            <Stack direction="row" spacing={2}>
              <Button
                color={submitFormColor}
                variant="contained"
                onClick={handleFormSubmit}
                endIcon={<SendIcon />}
              >
                {submitFormText}
              </Button>
            </Stack>
          </Grid>
        </Grid>
      </FormControl>
    </div>
  );
};
