import React, { useState, useEffect } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import axios from "axios";

import { ProjectCard } from "../../Items/Cards/projectCard.component";
import { toTitleCase } from "../../utils";

import {
  Grid,
  FormGroup,
  FormControlLabel,
  Switch,
  Dialog,
  DialogTitle,
  DialogContent,
  CircularProgress,
  Box,
} from "@mui/material";
import { UserForm } from "../../Pages/SubmissionForm/form.component";

export const ProjectCardList = () => {
  let params = useParams();
  let [searchParams, setSearchParams] = useSearchParams();
  let [projects, setProjects] = useState(null);
  let [editProject, setEditProject] = useState({
    issue: null,
    toggle: false,
  });

  const [filterByStatus, setFilterByStatus] = useState();
  const [filterByType, setFilterByType] = useState();

  useEffect(() => {
    if (projects === null) {
      axios.get(`/api/projects`).then((res) => setProjects(res.data));
      console.log(projects);
    }
  });

  const toggleEdit = (issue) => {
    setEditProject({ issue: issue, toggle: !setEditProject.toggle });
  };

  if (!projects) {
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
      <Grid container spacing={2}>
        {projects.map((el, index) => {
          return (
            <Grid item md={4} key={`${index}-${JSON.stringify(el)}`}>
              <ProjectCard
                issue={el}
                toggleEdit={(issue) => toggleEdit(issue)}
                onDelete={() =>
                  axios
                    .get(
                      `/api/project/Pale-Court/categories/${params.category}/issues`
                    )
                    .then((res) => setProjects(res.data))
                }
              />
            </Grid>
          );
        })}
      </Grid>
      <Dialog
        open={editProject.toggle}
        onClose={() => setEditProject({ issue: null, toggle: false })}
        fullWidth
        maxWidth="xl"
      >
        <DialogTitle>Edit Issue</DialogTitle>
        <DialogContent>
          <Grid container sx={{ pt: 1 }}>
            <Grid item>
              <UserForm
                issue={editProject.issue || {}}
                isUpdate={true}
                onSubmit={() => {
                  setEditProject({ issue: null, toggle: false });
                  axios
                    .get(`/api/projects`)
                    .then((res) => setProjects(res.data));
                }}
              />
            </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </div>
  );
};
