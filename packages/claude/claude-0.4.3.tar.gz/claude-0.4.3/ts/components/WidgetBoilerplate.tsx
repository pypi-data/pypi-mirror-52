import {createStyles, withStyles, WithStyles} from '@material-ui/core';
import * as React from "react";
import {CommonWidgetProps, BaseWidgetSettings} from "../types";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";

const styles = () => createStyles({
    body: {

    }
});


export class Settings extends BaseWidgetSettings {

}

export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const { config, classes, dashboardConfig } = props;

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig} >
            <div className={classes.body}>
                das widget body
            </div>
            <WidgetMenu id={config.id} settings={config.settings} settingsFormFields={[]} />
        </WidgetFrame>
    )
});
