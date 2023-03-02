import React, { useState, useEffect } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import axios from "axios";

import { IssueCard } from "../../Items/Cards/issueCard.component";
import { toTitleCase } from "../../utils";

import {
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  CircularProgress,
  Box,
} from "@mui/material";
import { UserForm } from "../SubmissionForm/form.component";

export const ProjectPage = () => {
  let params = useParams();
  let navigate = useNavigate();
  let [project, setProject] = useState(null);
  let [editProject, setEditProject] = useState({
    project: null,
    toggle: false,
  });

  useEffect(() => {
    if (project === null) {
      axios.get(`/api/projects/`).then((res) => setProject(res.data));
    }
  });

  const toggleEdit = (project) => {
    setEditProject({ project: project, toggle: !editProject.toggle });
  };

  if (!project) {
    return (
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
    );
  }

  return (
    <div>
      <Grid container>
        <Grid item md={12} key={`${JSON.stringify(project)}`}>
          <IssueCard
            project={project}
            toggleEdit={(project) => toggleEdit(project)}
            onDelete={() =>
              axios.get(`/api/projects`).then((res) => navigate("/"))
            }
          />
        </Grid>
      </Grid>
      <Dialog
        open={editProject.toggle}
        onClose={() => setEditProject({ project: null, toggle: false })}
        fullWidth
        maxWidth="xl"
      >
        <DialogTitle>Edit Issue</DialogTitle>
        <DialogContent>
          <Grid container sx={{ pt: 1 }}>
            <Grid item>
              <UserForm
                project={editProject.project || {}}
                isUpdate={true}
                onSubmit={() => {
                  setEditProject({ project: null, toggle: false });
                  axios
                    .get(`/api/projects`)
                    .then((res) => setProject(res.data));
                }}
              />
            </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </div>
  );
};
