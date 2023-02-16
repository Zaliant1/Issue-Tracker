import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { Header } from "./Header/header.component";
import { IssueCardList } from "./Pages/IssueList/issueList.component";
import { IssuePage } from "./Pages/Issue/issue.component";
import { UserForm } from "./SubmissionForm/form.component";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

const App = () => {
  return (
    <ThemeProvider theme={darkTheme}>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Header />}>
              <Route path="/Form" element={<UserForm />} />
              <Route path="/issues/:category" element={<IssueCardList />} />
              <Route path="/issue/:issueId" element={<IssuePage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </div>
    </ThemeProvider>
  );
};

export default App;
