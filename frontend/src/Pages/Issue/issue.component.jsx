import React, { useState, useEffect } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import axios from "axios";

import { IssueCard } from "../../Items/Cards/card.component";
import { toTitleCase } from "../../utils";

import {
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  CircularProgress,
  Box,
} from "@mui/material";
import { UserForm } from "../../SubmissionForm/form.component";

export const IssuePage = () => {
  let params = useParams();
  let navigate = useNavigate();
  let [issue, setIssue] = useState(null);
  let [editIssue, setEditIssue] = useState({ issue: null, toggle: false });

  useEffect(() => {
    if (issue === null) {
      axios
        .get(`/api/issue/${params.issueId}`)
        .then((res) => setIssue(res.data));
    }
  });

  const toggleEdit = (issue) => {
    setEditIssue({ issue: issue, toggle: !editIssue.toggle });
  };

  if (!issue) {
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
        <Grid item md={12} key={`${JSON.stringify(issue)}`}>
          <IssueCard
            issue={issue}
            toggleEdit={(issue) => toggleEdit(issue)}
            onDelete={() =>
              axios
                .get(`/api/issue/category/${params.category}`)
                .then((res) => navigate("/"))
            }
          />
        </Grid>
      </Grid>
      <Dialog
        open={editIssue.toggle}
        onClose={() => setEditIssue({ issue: null, toggle: false })}
        fullWidth
        maxWidth="xl"
      >
        <DialogTitle>Edit Issue</DialogTitle>
        <DialogContent>
          <Grid container sx={{ pt: 1 }}>
            <Grid item>
              <UserForm
                issue={editIssue.issue || {}}
                isUpdate={true}
                onSubmit={() => {
                  setEditIssue({ issue: null, toggle: false });
                  axios
                    .get(`/api/issue/category/${params.category}`)
                    .then((res) => setIssue(res.data));
                }}
              />
            </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </div>
  );
};
