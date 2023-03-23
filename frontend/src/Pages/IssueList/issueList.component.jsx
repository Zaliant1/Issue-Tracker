import React, { useState, useEffect } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import axios from "axios";

import { IssueCard } from "../../Items/Cards/issueCard.component";
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
import { UserForm } from "../SubmissionForm/form.component.jsx";

export const IssueCardList = () => {
  let params = useParams();
  let [searchParams, setSearchParams] = useSearchParams();
  let [issues, setIssues] = useState(null);
  let [editIssue, setEditIssue] = useState({ issue: null, toggle: false });

  const [filterByStatus, setFilterByStatus] = useState();
  const [filterByType, setFilterByType] = useState();
  const archived = searchParams.get("archived") === "true";

  useEffect(() => {
    if (issues === null) {
      axios
        .get(`/api/project/Pale-Court/category/${params.category}/issues`)
        .then((res) => setIssues(res.data));
    }
  });

  useEffect(() => {
    if (issues) {
      axios
        .get(`/api/project/Pale-Court/category/${params.category}/issues`)
        .then((res) => setIssues(res.data));
    }
  }, [params.category]); // eslint-disable-line

  const toggleEdit = (issue) => {
    setEditIssue({ issue: issue, toggle: !editIssue.toggle });
  };

  if (!issues) {
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
      <FormGroup>
        <FormControlLabel
          onChange={(e) => {
            if (!archived) {
              setSearchParams({ archived: true });
            } else {
              setSearchParams();
            }
          }}
          control={<Switch />}
          checked={archived}
          label="Archived"
        />
      </FormGroup>
      <Grid container spacing={2}>
        {issues
          .filter(
            (el) =>
              (!filterByStatus || el.status === filterByStatus) &&
              archived === el.archived
          )
          .map((el, index) => {
            return (
              <Grid item md={4} key={`${index}-${JSON.stringify(el)}`}>
                <IssueCard
                  issue={el}
                  toggleEdit={(issue) => toggleEdit(issue)}
                  onDelete={() =>
                    axios
                      .get(
                        `/api/project/Pale-Court/category/${params.category}/issues`
                      )
                      .then((res) => setIssues(res.data))
                  }
                />
              </Grid>
            );
          })}
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
                    .get(
                      `/api/project/Pale-Court/category/${params.category}/issues`
                    )
                    .then((res) => setIssues(res.data));
                }}
              />
            </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </div>
  );
};
