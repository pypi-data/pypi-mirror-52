import {createStyles, withStyles, WithStyles} from '@material-ui/core';
import * as React from "react";
import {CommonWidgetProps, BaseWidgetSettings, IdokepHoursResponse, IdokepHourData} from "../types";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import api from '../api';
import { IfComp, useInterval } from './tools';
import { FormCheckboxListFieldDescriptor, FormSelectFieldDescriptor } from './WidgetSettingsDialog';

export type ShowableRows = 'image' | 'precipitationValue' | 'precipitationProbability' | 'temperatureChart';

type Props = CommonWidgetProps<Settings>;

const dataRowHeightRatio: {[key in ShowableRows]: number} = {
    image: 0.8,
    precipitationProbability: 0.04,
    precipitationValue: 0.04,
    temperatureChart: 0.8,
}

function getRowShownRatio(baseRatio: number, {config}: Props): number {
    let ratio = baseRatio;
    for (const [key, val] of Object.entries(dataRowHeightRatio)) {
        if (!config.settings.rowsToShow[key])
            ratio += (baseRatio * 2 * val);
    }
    return ratio;
}

const styles = () => createStyles({
    body: {
        fontSize: (p: Props) => p.config.height * getRowShownRatio(0.055, p),
        display: 'grid',
        gridTemplateColumns: (p: Props) => `repeat(${p.config.settings.hours/3}, 1fr)`,
        gridTemplateRows: 'repeat(4, min-content) auto',
        justifyItems: 'center',
        padding: '12px 0',
        height: '100%',
    },
    hour: {
        gridRowStart: 1,
    },
    image: {
        gridRowStart: 2,
        '& img': {
            width: '2.5em',
        }
    },
    precipitationProbability: {
        gridRowStart: 4,
        fontSize: '0.7em',
    },
    precipitationValue: {
        gridRowStart: 3,
        fontSize: '0.8em',
    },
    temperatureChart: {
        paddingTop: '0.4em',
        gridRowStart: 5,
        display: 'flex',
        flexDirection: 'column',
        width: '60%',
        '& .text': {
            textAlign: 'center',
        },
        '& .bar': {

            backgroundColor: 'grey',
        }
    },
});


export class Settings extends BaseWidgetSettings {
    city: string = 'Budapest';
    pollInterval: number = 60*10;
    // showCity: boolean = false;
    hours: number = 24;
    rowsToShow: {[key in ShowableRows]: boolean} = {
        image: true,
        precipitationProbability: true,
        precipitationValue: true,
        temperatureChart: true,
    };
}

export default withStyles(styles)((props: Props & WithStyles<typeof styles>) => {

    const { config, classes, dashboardConfig } = props;
    const { rowsToShow } = config.settings;

    const [data, setData] = React.useState<IdokepHoursResponse>([]);

    function fetchData(settings: Settings = config.settings) {
        api.getIdokepHours(settings.city).then(setData);
    }

    function onBeforeSettingsSubmit(settings: Settings) {
        if (settings.city != config.settings.city)
            fetchData(settings)
    }

    useInterval(fetchData, config.settings.pollInterval * 1000);

    React.useEffect(fetchData, []);

    const displayData = data.slice(0, config.settings.hours / 3);

    const temps = displayData.map(d => d.temp);

    const maxTemp = Math.max(...temps) + 1;
    const minTemp = Math.min(...temps) - 1;

    let cells = [];
    let idx = 0;

    for (const hourData of displayData) {
        const barColorLight = 100 - (30+(hourData.temp - minTemp)/(maxTemp-minTemp)*40);
        cells.push(
            <div key={idx++} className={classes.hour}>{hourData.hour}h</div>,
            <IfComp cond={rowsToShow.image}><div key={idx++} className={classes.image}><img src={hourData.img}/></div></IfComp>,

            <IfComp cond={rowsToShow.precipitationValue}>
                <div key={idx++} className={classes.precipitationValue}>
                    {hourData.precipitation.value ? `${hourData.precipitation.value} mm` : null}
                </div>
            </IfComp>,

            <IfComp cond={rowsToShow.precipitationProbability}>
                <div key={idx++} className={classes.precipitationProbability}>
                    {hourData.precipitation.probability ? `(${hourData.precipitation.probability}%)` : null}
                </div>
            </IfComp>,

            <IfComp cond={rowsToShow.temperatureChart}>
                <div key={idx++} className={classes.temperatureChart}>
                    <div style={{flexGrow: 1}} />
                    <div className="text">{hourData.temp}</div>
                    <div className="bar" style={{
                        height: `${(hourData.temp - minTemp)/(maxTemp-minTemp)*100}%`,
                        backgroundColor: `hsl(350, 62%, ${barColorLight}%)`,
                    }}/>
                </div>
            </IfComp>,
        )
    }

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig} >
            <div className={classes.body}>
                {...cells}
            </div>
            <WidgetMenu id={config.id} settings={config.settings} settingsFormFields={[{
                name: 'city',
                label: 'City',
            }, {
                name: 'hours',
                label: 'Hours to show',
                type: 'select',
                options: Array.from(Array(11).keys()).map(i => ({value: `${i*3+6}`, label: `${i*3+6}h`})),
            } as FormSelectFieldDescriptor, {
                name: 'pollInterval',
                label: 'Interval',
            // }, {
            //     name: 'showCity',
            //     label: 'Show city name',
            }, {
                type: 'checkboxList',
                name: 'rowsToShow',
                label: 'Show data rows',
                options: [
                    {value: 'image', label: 'Image'},
                    {value: 'precipitationProbability', label: 'Precipitation probability'},
                    {value: 'precipitationValue', label: 'Precipitation value'},
                    {value: 'temperatureChart', label: 'Temperature chart'},
                ]
            } as FormCheckboxListFieldDescriptor]} />
        </WidgetFrame>
    )
});
