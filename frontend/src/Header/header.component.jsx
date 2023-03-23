import React, { useState, useEffect } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import axios from "axios";

import {
  Box,
  Drawer,
  AppBar,
  CssBaseline,
  List,
  Typography,
  ListItemButton,
  ListItem,
  ListItemText,
  Toolbar,
  Fab,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { Outlet, useNavigate, useLocation } from "react-router-dom";

const drawerWidth = 240;

export const Header = () => {
  const [categories, setCategories] = useState([]);
  let [searchParams, setSearchParams] = useSearchParams();

  let code = searchParams.get("code");

  const navigate = useNavigate();
  const location = useLocation();
  let params = useParams();

  useEffect(() => {
    if (!categories[0]) {
      axios
        .get(`/api/project/Pale-Court/categories`)
        .then((res) => setCategories(res.data));
    }
  }, [categories]);

  // if (location.pathname.includes("code")) {
  //   console.log(params);
  //   console.log("hi");
  //   // axios.post(`/api/auth`);
  // }

  if (location.pathname.includes("/projects")) {
    return (
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar
          position="fixed"
          sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
        >
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Project Management
            </Typography>

            <Fab variant="extended" onClick={() => navigate("/form")}>
              Project
              <AddIcon />
            </Fab>
          </Toolbar>
        </AppBar>
        <Toolbar />
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          <Outlet />
        </Box>
      </Box>
    );
  } else {
    return (
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar
          position="fixed"
          sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
        >
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Project Management
            </Typography>

            <Fab variant="extended" onClick={() => navigate("/form")}>
              Issue
              <AddIcon />
            </Fab>
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: {
              width: drawerWidth,
              boxSizing: "border-box",
            },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: "auto" }}>
            <List>
              {categories.map((el, index) => {
                return (
                  <ListItem
                    disablePadding
                    key={el.route}
                    onClick={() => navigate(`/issues/${el.toLowerCase()}`)}
                  >
                    <ListItemButton>
                      <ListItemText primary={el} />
                    </ListItemButton>
                  </ListItem>
                );
              })}
            </List>
          </Box>
        </Drawer>
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          <Outlet />
        </Box>
      </Box>
    );
  }
};
