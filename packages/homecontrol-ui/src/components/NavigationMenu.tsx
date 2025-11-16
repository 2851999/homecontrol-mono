"use client";

import MenuIcon from "@mui/icons-material/Menu";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import SwipeableDrawer from "@mui/material/SwipeableDrawer";
import React from "react";

export default function NavigationMenu() {
  const [drawerOpen, setDrawerOpen] = React.useState<boolean>(false);

  return (
    <>
      <IconButton
        size="large"
        edge="start"
        color="inherit"
        sx={{ mr: 2 }}
        onClick={() => setDrawerOpen(!drawerOpen)}
      >
        {drawerOpen ? <MenuOpenIcon /> : <MenuIcon />}
      </IconButton>
      <SwipeableDrawer
        anchor="left"
        open={drawerOpen}
        onOpen={() => setDrawerOpen(true)}
        onClose={() => setDrawerOpen(false)}
      >
        <Box role="presentation" sx={{ width: 250 }}></Box>
      </SwipeableDrawer>
    </>
  );
}
