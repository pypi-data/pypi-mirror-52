import {createStyles, withStyles, WithStyles} from '@material-ui/core';
import * as React from "react";
import {CommonWidgetProps, BaseWidgetSettings, Transmission} from "../types";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import api from '../api';
import { useInterval } from './tools';
import { humanFileSize, WidgetStyle } from '../tools';
import moment = require('moment');
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';


const styles = () => createStyles({
    body: {
        fontSize: WidgetStyle.getRelativeSize(0.025).width,
        '& .torrentList': {
            padding: '0.5em',
            display: 'grid',
            gridTemplateColumns: 'auto repeat(3, 1fr)',
            gridColumnGap: '0.6em',
            gridRowGap: '0.3em',
            '& .name': {
                overflow: 'hidden',
                textOverflow: 'ellipsis',
            },
            '& div': {
                whiteSpace: 'nowrap',
            },
            '& .percent, & .rate': {
                textAlign: 'right',
            }
        },
        '& .stats': {
            padding: '0.5em',
            '& > span': {
                padding: '0.5em',
            }
        }
    }
});


export class Settings extends BaseWidgetSettings {
    host: string = '';
    ssl: boolean = false;
    port: number = 9091;
    path: string = '/transmission/rpc';
    username: string = '';
    password: string = '';

    get url(): string {
        return `http${this.ssl ? 's' : ''}://${this.host}:${this.port}${this.path}`;
    }
}

function TorrentList(props: {torrents: Array<Transmission.Torrent>}) {

    function Torrent(props: {data: Transmission.Torrent}) {
        const {id, name, percentDone, rateDownload, eta} = props.data;
        return (
            <React.Fragment>
                <div className="name">{name}</div>
                <div className="percent">{Math.round(percentDone*100)}%</div>
                <div className="rate">{humanFileSize(rateDownload)}/s</div>
                <div className="eta">{moment.duration(eta * 1000).humanize()}</div>
            </React.Fragment>
        );
    }

    const torrents = props.torrents.filter(t => t.rateDownload != 0);

    return (
        <div className="torrentList">
            {torrents.map(t => <Torrent key={t.id} data={t} />)}
        </div>
    );
}

function Error(props: {msg: string}) {
    return <div>{props.msg}</div>
}

function SessionStats(props: {sessionStats: Transmission.SessionStats, torrents: Array<Transmission.Torrent>}) {
    const {sessionStats: {torrentCount, uploadSpeed, downloadSpeed}, torrents} = props;
    return (
        <div className="stats">
            <span style={{paddingRight: 0}}>Active:</span><span>{torrents.filter(t => t.peersConnected).length} / {torrentCount}</span>
            <span>Speed:</span>
            <FontAwesomeIcon icon="chevron-circle-down" style={{color: '#08D'}} /><span>{humanFileSize(downloadSpeed)}/s</span>
            <FontAwesomeIcon icon="chevron-circle-up" style={{color: '#090'}} /><span>{humanFileSize(uploadSpeed)}/s</span>
        </div>
    );
}


export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const { config, config: {id, settings}, classes, dashboardConfig } = props;

    const [data, setData] = React.useState<Transmission.ApiResponse>();

    function fetchData(cfg: Settings = settings) {
        if (cfg.host)
            api.transmission(cfg.url, cfg.username, cfg.password).then(setData);
    }

    useInterval(fetchData, 5*1000);

    React.useEffect(fetchData, []);

    return (
        <WidgetFrame config={config} dashboardConfig={dashboardConfig} >
            <div className={classes.body}>
                {data ? (typeof data.data == 'string' ? <Error msg={data.data} /> : (
                    <React.Fragment>
                        <SessionStats {...data.data} />
                        <TorrentList torrents={data.data.torrents} />
                    </React.Fragment>
                )) : ''}
            </div>
            <WidgetMenu id={id} settings={settings} settingsFormFields={[
                {name: 'host',label: 'Host'},
                {name: 'ssl', label: 'SSL'},
                {name: 'port', label: 'Port'},
                {name: 'path', label: 'Path'},
                {name: 'username', label: 'Username'},
                {name: 'password', label: 'Password'}
            ]} />
        </WidgetFrame>
    )
});

