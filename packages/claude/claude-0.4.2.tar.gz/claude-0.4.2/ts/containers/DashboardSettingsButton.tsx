import { Button } from '@material-ui/core';
import * as React from "react";
import { useState } from "react";
import { DashboardConfig, State, Dispatcher } from '../types';
import DashboardConfigDialog from '../components/DashboardConfigDialog';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { updateDashboard } from '../actions';
import { FormattedMessage } from 'react-intl';

type StateProps = {
    data: DashboardConfig,
}

type DispatchProps = {
    updateDashboard: (data: DashboardConfig) => void,
}

const DashboardSettingsButton = (props: StateProps & DispatchProps) => {

    const [isShowDialog, showDialog] = useState(false);

    const onButtonClick = () => {
        showDialog(true);
    }

    const closeDialog = () => {
        showDialog(false);
    }

    const submit = (data: DashboardConfig) => {
        props.updateDashboard(data);
        closeDialog();
    }

    return <React.Fragment>
        <Button variant="contained" size="small" color="primary" onClick={onButtonClick}>
            <FormattedMessage id="controlBar.settings" />
        </Button>
        <DashboardConfigDialog show={isShowDialog} title="Dashboard settings" onClose={closeDialog} submit={submit} data={props.data} />
    </React.Fragment>
};

function mapStateToProps(state: State): StateProps {
    const { currentDashboardId, dashboards } = state;
    return {
        data: dashboards[currentDashboardId]
    }
}

const mapDispatchToProps = (dispatch: Dispatcher): DispatchProps => {
    return {
        updateDashboard: data => dispatch(updateDashboard(data))
    }
}

export default connect<StateProps, DispatchProps>(mapStateToProps, mapDispatchToProps)(DashboardSettingsButton);
