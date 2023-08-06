import { Button, Menu, MenuItem } from "@material-ui/core";
import * as React from "react";
import widgetRegistry from "../widgetRegistry";
import { State } from "../types";
import { connect } from "react-redux";
import { FormattedMessage } from "react-intl";

type OwnProps = {
    addWidget: (widgetType: string) => void,
}

type StateProps = {
    currentDashboardId: string,
}

function AddWidgetMenu(props: StateProps & OwnProps ) {
    const dbId = props.currentDashboardId;

    const [anchorEl, setAnchorEl] = React.useState(null);

    function handleClick(event) {
        setAnchorEl(event.currentTarget);
    }

    function handleClose() {
        setAnchorEl(null);
    }

    return (
        <React.Fragment>
            <Button aria-controls="simple-menu" aria-haspopup="true" variant="contained" size="small" color="primary" onClick={handleClick}>
                <FormattedMessage id="controlBar.addWidget" />
            </Button>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                {Object.keys(widgetRegistry).sort().map(k => (
                    <MenuItem key={k} onClick={props.addWidget.bind(this, k)}>{widgetRegistry[k].title}</MenuItem>
                ))}
            </Menu>
        </React.Fragment>
    )
}

function mapStateToProps(state: State): StateProps {
    const { currentDashboardId } = state;
    return {
        currentDashboardId,
    }
}

export default connect<StateProps>(mapStateToProps)(AddWidgetMenu);
