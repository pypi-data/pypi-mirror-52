import * as React from "react";
import { createStyles, withStyles, WithStyles, Typography } from '@material-ui/core';
import { WidgetConfig, DashboardConfig, WidgetConfigList, UpdateWidgetConfigAction, BaseWidgetSettings } from "../types";
import widgetRegistry from '../widgetRegistry'
import { claudeThemes } from "../themes";

const styles = () => createStyles({
    body: {
        height: '100%',
    }
});

export interface Props {
    config: DashboardConfig,
    widgets: WidgetConfigList,
}

function createSettingsClass(data: BaseWidgetSettings, settingsType: typeof BaseWidgetSettings) {
    let res = new settingsType();
    for (const key in data) {
        res[key] = data[key];
    }
    return res;
}

export default withStyles(styles)(React.memo((props: Props & WithStyles<typeof styles>) => {

    function factory(wconf: WidgetConfig) {
        const settingsType = widgetRegistry[wconf.type].settingsType;
        return React.createElement(widgetRegistry[wconf.type].factory, { // TODO: factory type is 'any'
            config: {...wconf, settings: createSettingsClass(wconf.settings, settingsType)},
            dashboardConfig: props.config,
            key: wconf.id,
        });
    }

    return (
        <div className={props.classes.body} style={{...claudeThemes[props.config.theme].dashboard}} >
            {props.widgets.map(factory)}
        </div>
    )
}))
