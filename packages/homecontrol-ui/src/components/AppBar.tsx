import AccountCircle from "@mui/icons-material/AccountCircle";
import MUIAppBar from "@mui/material/AppBar";
import IconButton from "@mui/material/IconButton";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import NavigationMenu from "./NavigationMenu";

export default async function AppBar() {
  return (
    <MUIAppBar
      position="relative"
      sx={{
        // zIndex: (theme) => theme.zIndex.drawer + 1 doesnt work with SSR
        // so just hardcode here for now
        zIndex: 1201,
      }}
    >
      <Toolbar>
        <NavigationMenu />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          HomeControl
        </Typography>
        <IconButton size="large" color="inherit">
          <AccountCircle />
        </IconButton>
      </Toolbar>
    </MUIAppBar>
  );
}
