import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Divider, ListItemIcon, Menu, MenuItem } from "@material-ui/core";
import * as React from "react";
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { addDashboard, selectDashboard } from '../actions';
import DashboardConfigDialog from "../components/DashboardConfigDialog";
import { DashboardConfig, DashboardConfigMap, State } from "../types";
import { FormattedMessage } from "react-intl";
// import { dialogTransition } from "./tools";

export type DispatchProps = {
    selectDashboard: (id: string) => void,
    addDashboard: (name: string, stepSize: number) => void,
}

export type StateProps = {
    currentDashboardId: string,
    dashboards: DashboardConfigMap,
}

function DashboardSelector(props: StateProps & DispatchProps) {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [isDialogShown, showDialog] = React.useState(false);
    const [name, setName] = React.useState('');
    const [stepSize, setStepSize] = React.useState(10);

    function openMenu(event) {
        setAnchorEl(event.currentTarget);
    }

    function closeMenu() {
        setAnchorEl(null);
    }

    function chooseMenu(id: string) {
        props.selectDashboard(id)
        closeMenu()
    }

    function closeDialog() {
        showDialog(false)
        setName('')
        setStepSize(10)
    }

    function openDialog() {
        showDialog(true)
        closeMenu()
    }

    const submit = (data: DashboardConfig) => {
        props.addDashboard(data.name, data.stepSize);
        closeDialog();
    }

    const dashboards = Object.values(props.dashboards);

    return (
        <React.Fragment>
            <Button aria-controls="DashboardSelector" aria-haspopup="true" variant="contained" size="small" color="primary"
                onClick={openMenu}>
                <FormattedMessage id="controlBar.dashboards" />
            </Button>
            <Menu
                id="DashboardSelector"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={closeMenu}
            >
                <MenuItem key={0} onClick={openDialog}><FormattedMessage id="controlBar.newDashboard" /></MenuItem>
                {dashboards.length ? <Divider /> : null}
                {dashboards.map(d =>
                    <MenuItem key={d.id} onClick={chooseMenu.bind(this, d.id)}>
                        <ListItemIcon>
                            {d.id == props.currentDashboardId ? <FontAwesomeIcon icon="check" /> : <span />}
                        </ListItemIcon>
                        {d.name}
                    </MenuItem>
                )}
            </Menu>

            <DashboardConfigDialog show={isDialogShown} title="Dashboard settings" onClose={closeDialog} submit={submit}  />

        </React.Fragment>
    )
}

function mapStateToProps(state: State): StateProps {
    const { currentDashboardId, dashboards } = state;
    return {
        currentDashboardId,
        dashboards,
    }
}

// TODO: typize
const mapDispatchToProps = dispatch => bindActionCreators({selectDashboard, addDashboard}, dispatch)

export default connect<StateProps, DispatchProps>(mapStateToProps, mapDispatchToProps)(DashboardSelector);

