import {createStyles, withStyles, WithStyles} from '@material-ui/core';
import * as React from "react";
import {CommonWidgetProps, BaseWidgetSettings, IdokepCurrentResponse} from "../types";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import { useInterval } from './tools';
import api from '../api';
import { WidgetStyle } from '../tools';

const styles = () => createStyles({
    body: {
        fontSize: WidgetStyle.getRelativeSize(0.3).width,
    },
    value: {
        textAlign: 'center',
    },
    img: {
        textAlign: 'center',
        margin: '-0.25em 0',
        '& img': {
            width: WidgetStyle.getRelativeSize(0.9).width
        },
    },
    city: {
        fontSize: WidgetStyle.getRelativeSize(0.1).width,
        textAlign: 'center',
    },
});


export class Settings extends BaseWidgetSettings {
    city: string = 'Budapest';
    pollInterval: number = 60*10;
    showCity: boolean = false;
}

export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const { config, classes, dashboardConfig } = props;

    const [data, setData] = React.useState<IdokepCurrentResponse>();

    function fetchData(settings: Settings = config.settings) {
        api.getIdokepCurrent(settings.city).then(setData);
    }

    function onBeforeSettingsSubmit(settings: Settings) {
        if (settings.city != config.settings.city)
            fetchData(settings)
    }

    useInterval(fetchData, config.settings.pollInterval * 1000);

    React.useEffect(fetchData, []);

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig} >
            <div className={classes.body}>
                {data ? (<React.Fragment>
                    {config.settings.showCity ? <div className={classes.city}>{config.settings.city}</div> : null}
                    <div className={classes.value}>{data.value}°C</div>
                    <div className={classes.img}><img src={data.img} /></div>

                    </React.Fragment>) : null}
            </div>
            <WidgetMenu id={config.id} onBeforeSubmit={onBeforeSettingsSubmit} settings={config.settings} settingsFormFields={[{
                name: 'city',
                label: 'City',
            }, {
                name: 'pollInterval',
                label: 'Interval',
            }, {
                name: 'showCity',
                label: 'Show city name',
            }]} />
        </WidgetFrame>
    )
});
