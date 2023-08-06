import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { createStyles, withStyles, WithStyles } from '@material-ui/core';
import * as moment from 'moment';
import * as React from "react";
import { useEffect, useState } from "react";
import api from "../api";
import { CommonWidgetProps, ServerStatusData } from "../types";
import FlagIcon, { countries } from "./FlagIcon";
import {IfComp, useInterval} from "./tools";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import { FormListFieldDescriptor, FormNumberFieldDescriptor, FormSelectFieldDescriptor, FormCheckboxListFieldDescriptor } from "./WidgetSettingsDialog";

export type Column = 'name' | 'ping' | 'load' | 'memory' | 'uptime';

const colRatioRef: {[key in Column]: (props: CommonWidgetProps<Settings>) => number} = {
    name: p => 0.85 - (Math.max(...Object.values(p.config.settings.servers).map(s => s.name.length)) - 7) / 70,
    ping: p => 0.95,
    load: p => 0.75,
    memory: p => 0.95,
    uptime: p => 0.90,
}

const styles = () => createStyles({
    body: {
        fontSize: (props: CommonWidgetProps<Settings>) => {
            let baseSize = props.config.width * 0.062;
            for (let [col, enabled] of Object.entries(props.config.settings.columns)) {
                if (enabled)
                    baseSize *= colRatioRef[col](props)
            }

            return baseSize > 100 ? 16 : (baseSize < 5 ? 10 : baseSize);
        },
        padding: '0.5em',
        '& table': {
            borderSpacing: 0,
            width: '100%',
            '& td, & th': {
                padding: '0.2em 0.4em',
            },
            '& tr': {
                transition: 'opacity 1s',
            },
            '& th': {
                borderBottom: '1px solid rgba(255,255,255,0.5)'
            }
        },
    },
    nodata: {
        opacity: 0.3,
    },
    loadCol: {
        textAlign: 'right',
    }
});

export type ServerConfig = {
    id: string,
    ip: string,
    name: string,
    location: string,
    systemStatusServerPort?: number,
    rank: number,
}

type ServerConfigMap = {[s: string]: ServerConfig};

export class Settings {
    servers: ServerConfigMap = {};
    columns: {[key in Column]: boolean} = {load: true, memory: true, name: true, ping: true, uptime: true};
    pollInterval: number = 60;
}

export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const { config, classes, dashboardConfig } = props;
    const { settings } = config;
    const [serverInfo, setServerInfo] = useState({} as {[s: string]: ServerStatusData});


    const fetchServerInfo = (servers: ServerConfigMap = settings.servers) => {
        for (let desc of Object.values(servers)) {
            api.getServerStatus(desc.ip, desc.systemStatusServerPort).then(d => {
                setServerInfo(info => Object.assign({}, info, {[desc.ip]: d}))
            });
        }
    }

    useEffect(fetchServerInfo, [])

    useInterval(() => {
        fetchServerInfo()
    }, settings.pollInterval * 1000);

    const onBeforeSettingsSubmit = (data: Settings) => {
        // TODO: check if was a new server added (search for new ips)
        fetchServerInfo(data.servers)
    }

    const Status = (props: {ip: string}) => {
        const info = serverInfo[props.ip];

        let icon: IconProp = 'question-circle';
        let color = 'unset';

        if (info) {
            if (info.ping == null) {
                icon = 'times-circle';
                color = '#d40303';
            } else {
                icon = info.load ? 'check-circle' : 'exclamation-circle';
                color = info.load ? '#37a702' : '#d46703';
            }
        }

        return <FontAwesomeIcon icon={icon} style={{color: color}} />
    }

    const cols = settings.columns;

    const renderRow = (cfg: ServerConfig) => {

        const info = serverInfo[cfg.ip];

        const baseCols = <IfComp cond={cols.name}>
            <td><Status ip={cfg.ip} /></td>
            <td>{cfg.name}</td>
            <td style={{maxWidth: 30}}><FlagIcon name={cfg.location} /></td>
        </IfComp>

        if (!info)
            return <tr className={classes.nodata} key={cfg.name}>{baseCols}</tr>;

        return <tr key={cfg.name}>
            {baseCols}
            <IfComp cond={cols.ping}><td style={{textAlign: 'right'}}>{info.ping != null ? `${info.ping} ms` : null}</td></IfComp>
            <IfComp cond={cols.load}>
                <td className={classes.loadCol}>{info.load ? info.load[0].toFixed(2): null}</td>
                <td className={classes.loadCol}>{info.load ? info.load[1].toFixed(2): null}</td>
                <td className={classes.loadCol}>{info.load ? info.load[2].toFixed(2): null}</td>
            </IfComp>
            <IfComp cond={cols.memory}><td style={{textAlign: 'right'}}>{info.memory ? `${info.memory.percent.toFixed(1)}%` : null}</td></IfComp>
            <IfComp cond={cols.uptime}><td>{info.uptime ? moment.duration(info.uptime * 1000).humanize() : null}</td></IfComp>
        </tr>
    }

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig}>
            <div className={classes.body}>
                <table>
                    <thead>
                        <tr>
                            <IfComp cond={cols.name}><th colSpan={3}>Name</th></IfComp>
                            <IfComp cond={cols.ping}><th>Ping</th></IfComp>
                            <IfComp cond={cols.load}><th colSpan={3}>Load</th></IfComp>
                            <IfComp cond={cols.memory}><th>Mem</th></IfComp>
                            <IfComp cond={cols.uptime}><th>Uptime</th></IfComp>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.values(settings.servers).sort((s1, s2) => s1.rank - s2.rank).map(renderRow)}
                    </tbody>
                </table>
            </div>
            <WidgetMenu id={config.id} onBeforeSubmit={onBeforeSettingsSubmit} settings={config.settings} settingsFormFields={[{
                name: 'pollInterval',
                label: 'Polling interval',
                min: 0,
                max: 65565,
            } as FormNumberFieldDescriptor ,{
                type: 'list',
                label: 'Servers',
                name: 'servers',
                addButtonLabel: 'Add server',
                fields: [{
                    name: 'name',
                    label: 'Name',
                    default: '',
                },{
                    name: 'ip',
                    label: 'IP',
                    default: '',
                },{
                    name: 'location',
                    label: 'Location',
                    default: 'hu',
                    type: 'select',
                    options: Object.keys(countries).map(code => ({value: code, label: countries[code]}))
                } as FormSelectFieldDescriptor ,{
                    name: 'systemStatusServerPort',
                    label: 'Status port',
                    default: 35280,
                }]
            } as FormListFieldDescriptor, {
                type: 'checkboxList',
                name: 'columns',
                label: 'Columns',
                options: [
                    {value: 'name', label: 'Name'},
                    {value: 'ping', label: 'Ping'},
                    {value: 'load', label: 'Load'},
                    {value: 'memory', label: 'Memory'},
                    {value: 'uptime', label: 'Uptime'},
                ]
            } as FormCheckboxListFieldDescriptor ]} />
        </WidgetFrame>
    )
});
