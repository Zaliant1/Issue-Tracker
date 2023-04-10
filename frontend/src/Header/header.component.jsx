import React, { useState, useEffect, useContext } from "react";
import { UserContext } from "../context/authprovider.component";
import {
  Outlet,
  useLocation,
  useParams,
  useSearchParams,
  useNavigate,
} from "react-router-dom";

import axios from "axios";

import {
  Avatar,
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
import LoginIcon from "@mui/icons-material/Login";
import { createTheme, ThemeProvider } from "@mui/material/styles";

const drawerWidth = 240;
const theme = createTheme({
  palette: {
    discord: {
      main: "#5865F2",
    },
  },
});

export const Header = () => {
  const [categories, setCategories] = useState([]);
  const [searchParams, setSearchParams] = useSearchParams();
  const [userData, setUserData] = useState();
  const navigate = useNavigate();
  const location = useLocation();
  let params = useParams();

  let code = searchParams.get("code");
  if (code) {
    axios.post(`/api/user/discord/${code}`).then((res) => {
      if (res.data) {
        localStorage.setItem("user_auth", JSON.stringify(res.data));
        axios
          .get("https://discord.com/api/v8/users/@me", {
            headers: {
              Authorization: `Bearer ${res.data.access_token}`,
            },
          })
          .then((discordRes) => {
            setUserData(discordRes.data);
            localStorage.setItem("user_info", JSON.stringify(discordRes.data));
            navigate("/");
          });
      }
    });
  }

  if (!userData && localStorage.getItem(["user_info"])) {
    setUserData(JSON.parse(localStorage.getItem(["user_info"])));
  }

  useEffect(() => {
    if (!categories[0]) {
      axios
        .get(`/api/project/Pale-Court/categories`)
        .then((res) => setCategories(res.data));
    }
  }, [categories]);

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

            <Fab
              variant="extended"
              onClick={() => navigate("/form")}
              sx={{ margin: 1 }}
            >
              Project
              <AddIcon />
            </Fab>
            {userData ? (
              <ThemeProvider theme={theme}>
                <Fab
                  color="discord"
                  variant="circular"
                  onClick={() => navigate(`/user/${userData.id}`)}
                >
                  <Avatar
                    src={`https://cdn.discordapp.com/avatars/${userData.id}/${userData.avatar}.png`}
                    alt={userData.username}
                    sx={{ width: 50, height: 50 }}
                  />
                </Fab>
              </ThemeProvider>
            ) : (
              <ThemeProvider theme={theme}>
                <Fab
                  color="discord"
                  variant="extended"
                  href="https://discord.com/api/oauth2/authorize?client_id=1074939657902637058&redirect_uri=http%3A%2F%2F127.0.0.1%3A3000&response_type=code&scope=identify"
                >
                  Discord Login
                  <LoginIcon sx={{ pl: 0.5 }} />
                </Fab>
              </ThemeProvider>
            )}
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

            {userData ? (
              <div>
                <Fab
                  variant="extended"
                  onClick={() => navigate("/form")}
                  sx={{ margin: 1 }}
                >
                  Issue
                  <AddIcon sx={{ pl: 0.5 }} />
                </Fab>
                <ThemeProvider theme={theme}>
                  <Fab
                    color="discord"
                    variant="circular"
                    onClick={() => navigate(`/user/${userData.id}`)}
                  >
                    <Avatar
                      src={`https://cdn.discordapp.com/avatars/${userData.id}/${userData.avatar}.png`}
                      alt={userData.username}
                      sx={{ width: 50, height: 50 }}
                    />
                  </Fab>
                </ThemeProvider>
              </div>
            ) : (
              <div>
                <ThemeProvider theme={theme}>
                  <Fab
                    color="discord"
                    variant="extended"
                    href="https://discord.com/api/oauth2/authorize?client_id=1074939657902637058&redirect_uri=http%3A%2F%2F127.0.0.1%3A3000&response_type=code&scope=identify"
                  >
                    Discord Login
                    <LoginIcon sx={{ pl: 0.5 }} />
                  </Fab>
                </ThemeProvider>
              </div>
            )}
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
