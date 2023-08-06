import { createStyles, Drawer, withStyles, WithStyles } from '@material-ui/core';
import * as React from "react";
import { useState } from "react";
import {connect, useStore} from 'react-redux';
import { State, DashboardConfig } from '../types';
import AddWidgetMenu from './AddWidgetMenu';
import DashboardSelector from "./DashboardSelector";
import DashboardSettingsButton from './DashboardSettingsButton';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {addWidget} from "../actions";
import { claudeThemes } from '../themes';

type StateProps = {
    currentDashboardHasWidget: boolean,
    currentDashboard: DashboardConfig,
    isIdle: boolean,
}

const styles = () => createStyles({
    opener: {
        position: 'fixed',
        left: 5,
        top: 0,
        width: 30,
        height: 30,
        fontSize: 20,
        cursor: 'pointer',
        color: (props: StateProps) => props.currentDashboard ? claudeThemes[props.currentDashboard.theme].controlBar.openerColor : 'grey',
        opacity: (p: StateProps) => p.isIdle ? 0 : 1,
        transition: 'opacity 1s',
    },
    title: {
        padding: 15,
    },
    menubar: {
        display: 'flex',
        alignItems: 'center',
    },
    spacer: {
        width: 15,
    },
    separator: {
        width: 1,
        borderRight: '1px solid #777',
        marginLeft: 15,
        marginRight: 15,
        height: 25,
    },
    currentDashboard: {
        display: 'flex',
        flexDirection: 'column',
    },
});

const ControlBar = withStyles(styles)((props: StateProps &  WithStyles<typeof styles>) => {
    const [opened, setOpened] = useState(false);
    const store = useStore();

    const {classes, currentDashboard, currentDashboardHasWidget, isIdle} = props;

    function Spacer() {
        return <div className={classes.spacer} />
    }

    function Separator() {
        return <div className={classes.separator} />
    }

    const openDrawer = !isIdle && (opened || currentDashboard == undefined || !currentDashboardHasWidget);

    const onAddWidget = (type: string) => {
        store.dispatch(addWidget(currentDashboard.id, type))
        setOpened(false);
    }

    return (<div>
        <div className={classes.opener} onClick={() => setOpened(true)}>
            <FontAwesomeIcon icon="bars" />
        </div>
        <Drawer anchor="top" open={openDrawer} onClose={() => setOpened(false)}>
            <div className={classes.menubar}>
                <span className={classes.title}>Zsomapell Klod!</span>

                <DashboardSelector />

                {currentDashboard ?
                    <React.Fragment>
                        <Separator />
                        <div>{currentDashboard.name}</div>
                        <Spacer />
                        <DashboardSettingsButton />
                        <Spacer />
                        <AddWidgetMenu addWidget={onAddWidget} />
                    </React.Fragment> : null}
            </div>
        </Drawer>
    </div>)
});

function mapStateToProps(state: State): StateProps {
    const { currentDashboardId, widgets, dashboards, isIdle } = state;
    return {
        isIdle,
        currentDashboard: dashboards[currentDashboardId],
        currentDashboardHasWidget: Object.values(widgets).find(w => w.dashboardId == currentDashboardId) != undefined,
    }
}

export default connect<StateProps>(mapStateToProps)(ControlBar);
