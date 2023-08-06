import { createStyles, withStyles, WithStyles } from '@material-ui/core';
import * as React from "react";
import { useEffect, useState } from "react";
import { CommonWidgetProps } from "../types";
import { useInterval } from "./tools";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import { FormSelectFieldDescriptor } from './WidgetSettingsDialog';
import { WidgetStyle } from '../tools';
// import * as prettyBytes from 'pretty-bytes';

const styles = () => createStyles({
    body: {
        fontSize: WidgetStyle.getRelativeSize(0.05).width,
        padding: '0.4em',
        '& table': {
            width: '100%',
            '& td': {
                padding: '0.15em 0.3em',
            }
        }
    },
    empty: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        fontSize: WidgetStyle.getRelativeSize(0.07).width,
    },
    title: {
        textAlign: 'center',
        fontSize: '1.1em',
        padding: '0.2em',
    },
});

type StorageInfo = {
    device: string,
    label: string,
    mount: string,
    free: number,
    percent: number,
    total: number,
    used: number,
}

export class Settings {
    host: string = '';
    pollInterval: number = 600;
    title: string = '';
    sortBy: keyof StorageInfo = 'device';
}

export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const { config, classes, dashboardConfig } = props;
    const { settings } = config;
    const [storageInfo, setStorageInfo] = useState([] as Array<StorageInfo>);

    const fetchStorageInfo = (host: string = null) => {
        if (host || settings.host) {
            fetch(`http://${host || settings.host}:35280/`).then(rd => rd.json()).then(d => {
                setStorageInfo(d.hdd)
            })
        }
    }

    useEffect(fetchStorageInfo, [])

    useInterval(fetchStorageInfo, settings.pollInterval * 1000);

    const onBeforeSettingsSubmit = (data: Settings) => {
        fetchStorageInfo(data.host);
    }

    const gigabytize = (val: number) => {
        const gb = val / 1024 / 1024 / 1024
        return gb.toFixed(1) + ' GiB'
    }

    const comparator = (a: any, b: any) => {
        if (a < b) return -1;
        if (b < a) return 1;
        return 0;
    }

    const renderBody = () => {
        if (!settings.host)
            return <div className={classes.empty}>No host defined!</div>

        return (
            <div className={classes.body}>
                {settings.title ? <div className={classes.title}>{settings.title}</div> : null}
                <table>
                    <tbody>
                    {storageInfo.sort((a, b) => comparator(a[settings.sortBy], b[settings.sortBy])).map(s => <tr key={s.mount}>
                        <td>{s.label}</td>
                        <td style={{textAlign: 'right'}}>{s.percent.toFixed(1)} %</td>
                        <td style={{textAlign: 'right'}}>{gigabytize(s.free)}</td>
                    </tr>)}
                    </tbody>
                </table>
            </div>
        )
    }

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig}>
            {renderBody()}
            <WidgetMenu id={config.id} onBeforeSubmit={onBeforeSettingsSubmit} settings={config.settings} settingsFormFields={[{
                name: 'host',
                label: 'Host',
            }, {
                name: 'title',
                label: 'Title',
            }, {
                name: 'pollInterval',
                label: 'Poll interval',
            }, {
                name: 'sortBy',
                label: 'Sort',
                type: 'select',
                options: [
                    {value: 'device', label: 'Device name'},
                    {value: 'free', label: 'Free bytes'},
                    {value: 'label', label: 'Label'},
                    {value: 'mount', label: 'Mount point'},
                    {value: 'percent', label: 'Used percent'},
                    {value: 'total', label: 'Total bytes'},
                    {value: 'used', label: 'Used bytes'},
                ],
            } as FormSelectFieldDescriptor ]} />
        </WidgetFrame>
    )
});
