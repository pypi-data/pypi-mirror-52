import { createStyles, withStyles, WithStyles } from '@material-ui/core';
import * as moment from 'moment';
import * as React from "react";
import { Line, LineChart, YAxis } from 'recharts';
import api from '../api';
import WidgetFrame from "../containers/WidgetFrame";
import { BaseWidgetSettings, CommonWidgetProps, IdokepDayData, IdokepDaysResponse } from "../types";
import { IfComp, useInterval } from './tools';
import WidgetMenu from "./WidgetMenu";
import { FormCheckboxListFieldDescriptor } from './WidgetSettingsDialog';


export type ShowableRows = 'dayNumber' | 'dayText' | 'dayImage' | 'precipitationValue' | 'precipitationProbability' | 'temperatureChart';

const dataRowHeightRatio: {[key in ShowableRows]: number} = {
    dayNumber: 0.06,
    dayText: 0.06,
    dayImage: 0.9,
    precipitationValue: 0.035,
    precipitationProbability: 0.035,
    temperatureChart: 0.8,
}

function getRowShownRatio(baseRatio: number, {config}: CommonWidgetProps<Settings>): number {
    let ratio = baseRatio;
    for (const [key, val] of Object.entries(dataRowHeightRatio)) {
        if (!config.settings.rowsToShow[key])
            ratio += (baseRatio * 2 * val);
    }
    return ratio;
}

const styles = () => createStyles<string, CommonWidgetProps<Settings>>({
    body: {
        fontSize: p => p.config.height * getRowShownRatio(0.05, p),
    },
    header: {
        paddingTop: '0.6em',
        display: 'flex',
        justifyContent: 'space-around',
        '& > div': {
            display: 'flex',
            alignItems: 'center',
            flexDirection: 'column',
        },
    },
    weatherImage: {
        width: '2.5em',
    },
    precipitation: {
        fontSize: '0.7em',
        textAlign: 'center',
    }
});

export class Settings extends BaseWidgetSettings {
    city: string = 'Budapest';
    pollInterval: number = 60*10;
    // showCity: boolean = false;
    days: number = 7;
    rowsToShow: {[key in ShowableRows]: boolean} = {
        dayNumber: true,
        dayText: true,
        dayImage: true,
        precipitationValue: true,
        precipitationProbability: true,
        temperatureChart: true,
    };
}

function CustomizedLabel(props) {
    const {x, y, stroke, value} = props;
    // TODO fill color! (use theme)
    return <text x={x} y={y} dy={'-0.5em'} fill={"white"} textAnchor="middle">{value}</text>
}

export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const { config, classes, dashboardConfig } = props;
    const { rowsToShow } = config.settings;

    const [data, setData] = React.useState<IdokepDaysResponse>([]);

    function fetchData(settings: Settings = config.settings) {
        api.getIdokepDays(settings.city).then(setData);
    }

    function onBeforeSettingsSubmit(settings: Settings) {
        if (settings.city != config.settings.city)
            fetchData(settings)
    }

    useInterval(fetchData, config.settings.pollInterval * 1000);

    React.useEffect(fetchData, []);

    const displayData = data.slice(0, config.settings.days);

    function DayInfoCell(props: {day: IdokepDayData}) {
        return (
            <div>
                <IfComp cond={rowsToShow.dayNumber}><div>{props.day.day}</div></IfComp>
                <IfComp cond={rowsToShow.dayText}><div>{moment(props.day.date).format('dd')}</div></IfComp>
                <IfComp cond={rowsToShow.dayImage}><div><img className={classes.weatherImage} src={props.day.img} /></div></IfComp>
                {props.day.precipitation.probability ? <div className={classes.precipitation}>
                        <IfComp cond={rowsToShow.precipitationValue}><div>{`${props.day.precipitation.value}mm`}</div></IfComp>
                        <IfComp cond={rowsToShow.precipitationProbability}><div>{`(${props.day.precipitation.probability}%)`}</div></IfComp>
                    </div> : null}
            </div>
        )
    }

    const baseForMargin = config.height * getRowShownRatio(0.06, props);
    const vertMargin = config.width / config.settings.days / 2;

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig} >
            <div className={classes.body}>
                <div className={classes.header}>
                    {displayData.map(day => <DayInfoCell key={day.date} day={day} />)}
                </div>
                <IfComp cond={rowsToShow.temperatureChart}>
                    <LineChart
                        data={displayData}
                        width={config.width}
                        height={config.height * getRowShownRatio(0.54, props)}
                        margin={{
                            top: baseForMargin * 1.3,
                            right: vertMargin,
                            bottom: baseForMargin * 0.2,
                            left: vertMargin,
                        }}
                    >
                        <YAxis type="number" domain={['dataMin', 'dataMax']} hide />
                        <Line type="monotone" dataKey="max" stroke="red" strokeWidth={3} label={CustomizedLabel} />
                        <Line type="monotone" dataKey="min" stroke="blue" strokeWidth={3} label={CustomizedLabel} />
                    </LineChart>
                </IfComp>
            </div>
            <WidgetMenu id={config.id} onBeforeSubmit={onBeforeSettingsSubmit} settings={config.settings} settingsFormFields={[{
                name: 'city',
                label: 'City',
            }, {
                name: 'days',
                label: 'Days to show',
            }, {
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
                    {value: 'dayNumber', label: 'Day number'},
                    {value: 'dayText', label: 'Day text'},
                    {value: 'dayImage', label: 'Day image'},
                    {value: 'precipitationValue', label: 'Precipitation value'},
                    {value: 'precipitationProbability', label: 'Precipitation probability'},
                    {value: 'temperatureChart', label: 'Temperature chart'},
                ]
            } as FormCheckboxListFieldDescriptor ]} />
        </WidgetFrame>
    )
});
