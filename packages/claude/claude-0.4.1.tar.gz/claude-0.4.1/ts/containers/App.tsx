import { createStyles, withStyles, WithStyles } from '@material-ui/core';
import * as React from "react";
import { connect } from 'react-redux';
import Dashboard from "../components/Dashboard";
import { DashboardConfig, State, WidgetConfigList } from "../types";
import ControlBar from "./ControlBar";
import {IntlProvider} from 'react-intl';

import * as moment from 'moment';
import { LocaleType, claudeLocales } from '../locales';

const styles = () => createStyles({
    root: {
        height: '100%',
    }
});

type StateProps = {
    dashboardConfig: DashboardConfig,
    widgetConfigs: WidgetConfigList,
}

const defaultDashboardConfig: DashboardConfig = {
    id: '',
    name: 'default',
    stepSize: 10,
    theme: 'grey',
    locale: 'en',
}

const App = withStyles(styles)(React.memo((props: StateProps & WithStyles<typeof styles>) => {

    const {dashboardConfig, widgetConfigs} = props;

    moment.locale(dashboardConfig.locale);

    return <div className={props.classes.root}>
        <IntlProvider locale={dashboardConfig.locale} messages={claudeLocales[dashboardConfig.locale].flatMessages}>
            <ControlBar />
            {dashboardConfig ? <Dashboard config={dashboardConfig} widgets={widgetConfigs} /> : null}
        </IntlProvider>
    </div>
}))

function mapStateToProps(state: State): StateProps {
    const { currentDashboardId, dashboards, widgets } = state;
    return {
        dashboardConfig: Object.assign({}, defaultDashboardConfig, dashboards[currentDashboardId]),
        widgetConfigs: Object.values(widgets).filter(w => w.dashboardId == currentDashboardId),
    }
}

export default connect<StateProps>(mapStateToProps)(App);
