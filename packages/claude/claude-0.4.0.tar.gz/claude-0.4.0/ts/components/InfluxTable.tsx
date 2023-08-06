import {createStyles, withStyles, WithStyles} from '@material-ui/core';
import * as React from "react";
import {CommonWidgetProps} from "../types";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import { useInterval } from './tools';
import { WidgetStyle } from '../tools';

const styles = () => createStyles({
    body: {
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        '& table': {
            width: '100%',
            height: '100%',
            '& td': {
                padding: '0.1em 0.12em',
            },
            '& th:first-letter': {
                textTransform: 'capitalize',
            }
        },
        padding: '0.4em',
        fontSize: WidgetStyle.getRelativeSize(0.06).width,
    },
    title: {
        textAlign: 'center',
        fontSize: '1.1em',
        padding: '0.1em',
    },
    noConfig: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
    },
});


export class Settings {
    title: string = '';
    url: string = '';
    query: string = '';
    columns: string = '';
    interval: number = 60;
}

type InfluxResponse = {
    error?: string,
    results?: Array<{
        statement_id: number,
        series: Array<{
            name: string,
            tags: {[s: string]: any},
            columns: Array<string>,
            values: Array<Array<any>>,
        }>
    }>
}

export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const [data, setData] = React.useState([]);

    const { config, classes, dashboardConfig } = props;

    function fetchData(settings: Settings = config.settings) {
        if (!settings.url)
            return;

        fetch(settings.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            },
            body: `q=${encodeURIComponent(settings.query)}`,
        }).then(res => res.json()).then((data: InfluxResponse) => {
            if (data.error) {
                console.error(data.error)
                return
            }

            let res = [];
            for (let rowData of data.results[0].series) {
                let row = {...rowData.tags};
                rowData.columns.map((c, idx) => {
                    row[c] = rowData.values[0][idx]
                })
                res.push(row);
            }
            setData(res);
        })
    }

    useInterval(fetchData, config.settings.interval * 1000);

    React.useEffect(fetchData, []);

    const cols = () => {
        return config.settings.columns.split(',').map(s => s.trim());
    }

    const renderCell = (col: string, val: any) => {
        const isNum = !isNaN(val);
        return <td style={{textAlign: isNum ? 'right' : 'left'}} key={col}>{isNum ? val.toFixed(1) : val}</td>
    }

    const renderRow = (row: any, idx: number) => {
        return <tr key={idx}>{cols().map(c => renderCell(c, row[c]))}</tr>
    }

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig}>
            <div className={classes.body}>
                {config.settings.title ? <div className={classes.title}>{config.settings.title}</div> : null}
                {config.settings.url ? null : <div className={classes.noConfig}>No config.</div>}
                <div style={{flexGrow: 1}}>
                    <table>
                        <thead>
                            <tr>{cols().map(c => <th key={c}>{c}</th>)}</tr>
                        </thead>
                        <tbody>
                            {data.map(renderRow)}
                        </tbody>
                    </table>
                </div>
            </div>
            <WidgetMenu id={config.id} settings={config.settings} onBeforeSubmit={fetchData} settingsFormFields={[
                {name: 'title', label: 'Title'},
                {name: 'url', label: 'URL'},
                {name: 'query', label: 'Query'},
                {name: 'columns', label: 'Columns'},
                {name: 'interval', label: 'Interval'}
            ]} />
        </WidgetFrame>
    )
});
