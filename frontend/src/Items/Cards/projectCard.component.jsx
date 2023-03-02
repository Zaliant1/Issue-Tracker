import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import axios from "axios";

import {
  Card,
  CardContent,
  Button,
  IconButton,
  Typography,
  Chip,
  Box,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Divider,
  Grid,
  MenuItem,
  Menu,
  ListItemText,
  ListItemIcon,
  FormGroup,
  Switch,
  FormControlLabel,
} from "@mui/material";

import EditIcon from "@mui/icons-material/Edit";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import ArticleIcon from "@mui/icons-material/Article";
import CloseIcon from "@mui/icons-material/Close";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import { toTitleCase } from "../../utils";

const getStatusColor = (status) => {
  switch (status) {
    case "reported":
      return "default";
    case "in-progress":
      return "warning";
    case "completed":
      return "success";
    case "won't-fix":
      return "success";
    case "closed":
      return "success";
    default:
      return "default";
  }
};

const getTypeColor = (type) => {
  switch (type) {
    case "bug":
      return "warning";
    case "suggestion":
      return "primary";
    case "feature-request":
      return "secondary";
    default:
      return "default";
  }
};

const getPriorityColor = (priority) => {
  switch (priority) {
    case "low":
      return "primary";
    case "medium":
      return "warning";
    case "high":
      return "error";
    default:
      return "default";
  }
};

export const ProjectCard = (props) => {
  let navigate = useNavigate();
  const [project, setProject] = useState({ ...props.issue });
  const [toggleModlogs, setToggleModlogs] = useState(false);
  const [toggleAttachments, setToggleAttachments] = useState(false);
  const [menuOpen, setMenuOpen] = useState(null);

  //   const handleCardDelete = () => {
  //     axios.delete(`/api/projects`).then(() => {
  //       if (props.onDelete) {
  //         props.onDelete();
  //       }
  //     });
  //   };

  //   const handleModlogsToggle = () =>
  //     !toggleModlogs ? setToggleModlogs(true) : setToggleModlogs(false);

  //   const handleAttachmentsToggle = () =>
  //     !toggleAttachments
  //       ? setToggleAttachments(true)
  //       : setToggleAttachments(false);

  return (
    <>
      <Card>{props.project.name}</Card>
      {/* <Card>
        <CardContent sx={{ pt: 0 }}>
          <Grid container spacing={2}>
            <Grid item lg="11">
              <Box
                component="h4"
                sx={{ ml: 1 }}
                onClick={() => navigate(`/issue/${issue._id}`)}
              >
                {issue.summary}
              </Box>
            </Grid>
            <Grid item lg="1" sx={{ mt: 2, textAlign: "right" }}>
              <IconButton
                onClick={(e) => {
                  setMenuOpen(e.currentTarget);
                }}
                aria-controls={Boolean(menuOpen) ? "menu" : undefined}
                aria-expanded={Boolean(menuOpen) ? "true" : undefined}
                aria-haspopup="true"
              >
                <MoreVertIcon />
              </IconButton>
              <Menu
                anchorEl={menuOpen}
                open={Boolean(menuOpen)}
                onClose={() => setMenuOpen(null)}
                onClick={() => setMenuOpen(null)}
                anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
                transformOrigin={{ horizontal: "right", vertical: "top" }}
                id="menu"
              >
                <MenuItem onClick={handleModlogsToggle}>
                  <ListItemIcon>
                    <ArticleIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>View Mod Logs</ListItemText>
                </MenuItem>
                <MenuItem onClick={handleAttachmentsToggle}>
                  <ListItemIcon>
                    <AttachFileIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>View Attachment</ListItemText>
                </MenuItem>
                <Divider />
                <MenuItem onClick={() => props.toggleEdit(issue)}>
                  <ListItemIcon>
                    <EditIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>Edit</ListItemText>
                </MenuItem>
                <Grid container>
                  <Grid item md="3">
                    <Switch
                      size="small"
                      control={<Switch />}
                      checked={issue.archived}
                      label="Archived"
                      onChange={() => {
                        if (
                          issue.status === "completed" ||
                          issue.status === "won't-fix"
                        ) {
                          issue.archived = !issue.archived;
                          axios.post(`/api/issue/${props.issue._id}`, issue);
                        } else {
                          window.alert(
                            'Status must be "Completed" or "Won\'t Fix" in order to archive'
                          );
                        }
                      }}
                    />
                  </Grid>
                  <Grid item sx={{ pl: 0.5 }}>
                    <Typography>Archived</Typography>
                  </Grid>
                </Grid>

                <Divider />
                <MenuItem onClick={handleCardDelete}>
                  <ListItemIcon>
                    <CloseIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>Delete</ListItemText>
                </MenuItem>
              </Menu>
            </Grid>
            <Grid item md="11">
              <Box component="span" sx={{ pr: 1 }}>
                <Chip
                  color={getStatusColor(issue.status)}
                  label={toTitleCase(issue.status)}
                />
              </Box>
              <Box component="span" sx={{ pr: 1 }}>
                <Chip
                  color={getTypeColor(issue.type)}
                  label={toTitleCase(issue.type)}
                />
              </Box>
              <Box component="span" sx={{ pr: 1 }}>
                <Chip
                  color={getPriorityColor(issue.priority)}
                  label={toTitleCase(`${issue.priority} Priority`)}
                />
              </Box>
            </Grid>

            <Grid item md="12" sx={{ mt: 2 }}>
              <Typography variant="body1" color="text.secondary">
                {issue.description}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card> */}
      {/* <Dialog
        fullWidth
        maxWidth={"lg"}
        open={toggleModlogs}
        onClose={handleModlogsToggle}
      >
        <DialogTitle>{issue.modlogs.title}</DialogTitle>
        <DialogContent>
          <DialogContentText component="pre">
            {issue.modlogs.body}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleModlogsToggle}>Close</Button>
        </DialogActions>
      </Dialog>
      <Dialog
        fullWidth
        maxWidth={"lg"}
        open={toggleAttachments}
        onClose={handleAttachmentsToggle}
      >
        <DialogTitle>Attachments</DialogTitle>
        <DialogContent>
          <Box>
            <div
              dangerouslySetInnerHTML={{
                __html: issue.attachments.embed_source,
              }}
            />
            <Button
              onClick={() =>
                window.open(issue.attachments.general_url, "_blank")
              }
            >
              Go to URL
            </Button>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleAttachmentsToggle}>Close</Button>
        </DialogActions>
      </Dialog> */}
    </>
  );
};
