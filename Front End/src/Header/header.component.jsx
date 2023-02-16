import React from "react";

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
import { Outlet, useNavigate } from "react-router-dom";

const drawerWidth = 240;

const MENU_CATEGORIES = [
  {
    label: "Zemer",
    route: "/issues/zemer",
  },
  {
    label: "Dryya",
    route: "/issues/dryya",
  },
  {
    label: "Hegemol",
    route: "/issues/hegemol",
  },
  {
    label: "Isma",
    route: "/issues/isma",
  },
  {
    label: "Charms",
    route: "/issues/charms",
  },
  {
    label: "Champion's Call",
    route: "/issues/campions-call",
  },
  {
    label: "Base Game",
    route: "/issues/base-game",
  },
  {
    label: "Menu",
    route: "/issues/menu",
  },
  {
    label: "Technical",
    route: "/issues/technical",
  },
];

export const Header = () => {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Issue Tracker
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
            {MENU_CATEGORIES.map((el, index) => {
              return (
                <ListItem
                  disablePadding
                  key={el.route}
                  onClick={() => navigate(el.route)}
                >
                  <ListItemButton>
                    <ListItemText primary={el.label} />
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
};
