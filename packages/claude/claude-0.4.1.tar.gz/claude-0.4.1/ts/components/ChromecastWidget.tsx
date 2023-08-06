import { IconName } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { createStyles, withStyles, WithStyles } from '@material-ui/core';
import * as React from "react";
import * as moment from 'moment';
import WidgetFrame from "../containers/WidgetFrame";
import { WidgetStyle, convertKeysToCamelCase } from '../tools';
import { BaseWidgetSettings, Chromecast, CommonWidgetProps } from "../types";
import { useInterval } from './tools';
import WidgetMenu from "./WidgetMenu";
import classNames = require('classnames');
import useWebSocket from 'react-use-websocket';

const styles = () => createStyles({
    root: {
        overflow: 'initial',
        '& .body': {
            height: '100%',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
        },
        '& .center': {
            height: '100%',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
        },
        '& .panel': {
            margin: WidgetStyle.getRelativeSize(0.026).width,
            backdropFilter: 'blur(4px)',
            backgroundColor: 'rgba(0,0,0,0.6)',
            padding: WidgetStyle.getRelativeSize(0.02).width,
            borderRadius: 5,
            flexGrow: 1,
            display: 'flex',
            alignItems: 'center',
            '&:not(:last-child)': {
                marginBottom: 0,
            },
        },
        '& .title': {
            fontSize: WidgetStyle.getRelativeSize(0.05).width,
        },
        '& .time': {
            justifyContent: 'center',
        },
        '& .icon': {
            marginRight: WidgetStyle.getRelativeSize(0.05).width,
            fontSize: WidgetStyle.getRelativeSize(0.09).width,
        },
        '& .current': {
            fontSize: WidgetStyle.getRelativeSize(0.11).width,
            marginRight: WidgetStyle.getRelativeSize(0.04).width,
        },
        '& .duration': {
            fontSize: WidgetStyle.getRelativeSize(0.06).width,
        },
        '& .initializing': {
            width: WidgetStyle.getRelativeSize(0.3).width,
        },
        '& .backdrop': {
            width: '100%',
            height: '100%',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            borderRadius: '0.4em',
            '& .time': {
                backdropFilter: 'blur(4px)',
                backgroundColor: 'rgba(0,0,0,0.3)',
                fontSize: WidgetStyle.getRelativeSize(0.2).width,
                padding: '0.2em 0.4em',
                borderRadius: '0.1em',
            }
        }
    }
});

export class Settings extends BaseWidgetSettings {
    name: string = 'Olaf';
}

type ChromecastStatus = {
    media: Chromecast.Media,
    cast: Chromecast.Cast,
}

type AppProps = {
    status: ChromecastStatus,
}

function BackdropApp(props: AppProps) {

    const getNow = () => moment(new Date()).format('HH:mm');

    const [img, setImg] = React.useState('');
    const [time, setTime] = React.useState(getNow());

    function rollTheImageDice() {
        fetch('https://www.reddit.com/r/EarthPorn.json').then(r => r.json()).then(d => {
            const entries = d.data.children.filter(i => i.data['post_hint'] == 'image');
            const imgurl = entries[Math.floor(Math.random() * entries.length)].data.url;
            setImg(imgurl);
        })
    }

    React.useEffect(rollTheImageDice, []);

    useInterval(rollTheImageDice, 10*60*1000);
    useInterval(() => setTime(getNow()), 1000);

    return (
        <div className="backdrop center" style={{backgroundImage: `url(${img})`}}>
            <span className="time">{time}</span>
        </div>
    );
}

type PanelProps = {
    children: React.ReactNode,
    className?: string,
    style?: React.CSSProperties,
}

const Panel = (props: PanelProps) => {
    return (
        <div className={classNames('panel', props.className)} style={props.style}>
            {props.children}
        </div>
    )
}

const playerIcon: {[key in Chromecast.PlayerState]: IconName} = {
    PLAYING: 'play',
    BUFFERING: 'sync-alt',
    PAUSED: 'pause',
    IDLE: 'dot-circle',
    UNKNOWN: 'question',
}

function formatTimeDuration(s: number): string {
    s = Math.round(s);
    return (s-(s%=60))/60+(9<s?':':':0')+s
}

function LoadingApp(props: AppProps) {
    return <div className="center"><img className="initializing" src="/static/pics/rings.svg" /></div>;
}

function InitializingApp(props: AppProps) {
    return <div className="center"><img className="initializing" src="/static/pics/rings.svg" /></div>;
}

type MediaAppProps = {
    title: string,
    subTitle: string,
    image: string,
    currentTime: number,
    duration: number,
    playerState: Chromecast.PlayerState,
}

type MediaLoadingScreenProps = {
    icon: IconName,
    color: string,
}

function MediaLoadingScreen(props: MediaLoadingScreenProps) {
    return <div className="center">
        <FontAwesomeIcon icon={{prefix: 'fab', iconName: props.icon}} style={{
            color: props.color,
            filter: 'drop-shadow(0px 0px 14px white)',
            fontSize: '9em',
        }} />
    </div>;
}

function MediaApp(props: MediaAppProps) {

    const {title, subTitle, image, currentTime, duration, playerState} = props;

    const [time, setTime] = React.useState(currentTime);

    useInterval(() => {
        if (playerState == 'PLAYING') {
            setTime(t => t + 1);
        }
    }, 1000);

    React.useEffect(() => {
        setTime(currentTime);
    }, [currentTime])

    return (
        <div className="body" style={{backgroundImage: `url(${image})`}}>
            <Panel className="title">{title}</Panel>
            <Panel style={{fontSize: 20}}>{subTitle}</Panel>
            <Panel className="time">
                <FontAwesomeIcon icon={playerIcon[playerState]} className="icon" />
                <span className="current">{formatTimeDuration(time)}</span>
                <span className="duration"> / {formatTimeDuration(duration)}</span>
            </Panel>
        </div>
    );
}

const mediaApps: {[s: string]: {loading: MediaLoadingScreenProps, data: (p: ChromecastStatus) => MediaAppProps}} = {
    YouTube: {
        loading: {
            icon: 'youtube',
            color: 'rgb(252, 42, 23)',
        },
        data: p => {
            const mediaMetadata = p.media.mediaMetadata as Chromecast.MediaMetaData.YouTube;
            return {
                title: mediaMetadata.title,
                subTitle: mediaMetadata.subtitle,
                image: mediaMetadata.images[0].url,
                currentTime: p.media.currentTime,
                duration: p.media.duration,
                playerState: p.media.playerState,
            }
        },
    },
    Spotify: {
        loading: {
            icon: 'spotify',
            color: '#1DB954',
        },
        data: p => {
            const mediaMetadata = p.media.mediaMetadata as Chromecast.MediaMetaData.Spotify;
            return {
                title: mediaMetadata.title,
                subTitle: `${mediaMetadata.artist} - ${mediaMetadata.albumName}`,
                image: mediaMetadata.images[0].url,
                currentTime: p.media.currentTime,
                duration: p.media.duration,
                playerState: p.media.playerState,
            }
        },
    },
}

const exampleData = {
    yt: '{"cast":{"isActiveInput":false,"isStandBy":true,"volumeLevel":1,"volumeMuted":false,"appId":"233637DE","displayName":"YouTube","namespaces":["urn:x-cast:com.google.cast.debugoverlay","urn:x-cast:com.google.cast.cac","urn:x-cast:com.google.cast.media","urn:x-cast:com.google.youtube.mdx"],"sessionId":"2d8a8880-5b00-4037-acc1-f9a79c69db3f","transportId":"2d8a8880-5b00-4037-acc1-f9a79c69db3f","statusText":"YouTube"},"media":{"currentTime":901.567,"contentId":"OSTZ4XHJE34","contentType":"x-youtube/video","duration":1303.961,"streamType":"BUFFERED","idleReason":null,"mediaSessionId":1454740611,"playbackRate":1,"playerState":"PLAYING","supportedMediaCommands":262147,"volumeLevel":1,"volumeMuted":false,"mediaCustomData":{},"mediaMetadata":{"metadataType":0,"title":"Worcester - Final Version","subtitle":"Flamu","images":[{"url":"https://i.ytimg.com/vi/OSTZ4XHJE34/hqdefault.jpg"}]},"subtitleTracks":{},"currentSubtitleTracks":[],"lastUpdated":"2019-08-27T19:21:36.901680"}}',
    bd: '{"cast":{"isActiveInput":false,"isStandBy":true,"volumeLevel":1,"volumeMuted":false,"appId":"E8C28D3C","displayName":"Backdrop","namespaces":["urn:x-cast:com.google.cast.debugoverlay","urn:x-cast:com.google.cast.cac","urn:x-cast:com.google.cast.sse","urn:x-cast:com.google.cast.remotecontrol"],"sessionId":"fa0fae95-dab2-4b63-9286-862e3e9cad9b","transportId":"fa0fae95-dab2-4b63-9286-862e3e9cad9b","statusText":""},"media":null}',
    sp: '{"cast":{"isActiveInput":false,"isStandBy":true,"volumeLevel":1,"volumeMuted":false,"appId":"CC32E753","displayName":"Spotify","namespaces":["urn:x-cast:com.google.cast.debugoverlay","urn:x-cast:com.google.cast.cac","urn:x-cast:com.spotify.chromecast.secure.v1","urn:x-cast:com.google.cast.test","urn:x-cast:com.google.cast.broadcast","urn:x-cast:com.google.cast.media"],"sessionId":"b0b7b5ef-7d22-497f-907c-faed8dbc6082","transportId":"b0b7b5ef-7d22-497f-907c-faed8dbc6082","statusText":"Spotify"},"media":{"currentTime":217.796,"contentId":"spotify:track:6dgFhHtleZmYABhqiX8MKV","contentType":"application/x-spotify.track","duration":316.224,"streamType":"BUFFERED","idleReason":null,"mediaSessionId":1,"playbackRate":1,"playerState":"PLAYING","supportedMediaCommands":514511,"volumeLevel":1,"volumeMuted":false,"mediaCustomData":{},"mediaMetadata":{"metadataType":3,"title":"Alive Alone","songName":"Alive Alone","artist":"The Chemical Brothers","albumName":"Exit Planet Dust","images":[{"url":"https://i.scdn.co/image/ba20cec1e90348cb8a2ca00679acc98331eadd78","height":300,"width":300},{"url":"https://i.scdn.co/image/0f1a5fed171dcb0023c33f8d2064329b48314d5b","height":64,"width":64},{"url":"https://i.scdn.co/image/eb286311364f330a69ff3997bd342379d16b2ab0","height":640,"width":640}]},"subtitleTracks":{},"currentSubtitleTracks":[],"lastUpdated":"2019-09-15T06:59:46.700654"}}',
}

export default withStyles(styles)((props: CommonWidgetProps<Settings> & WithStyles<typeof styles>) => {

    const { config, classes, dashboardConfig } = props;

    const [sendMessage, lastMessage, readyState] = useWebSocket(`ws://${window.location.host}/chromecast-proxy/${config.settings.name}`);
    const data: ChromecastStatus = (readyState && lastMessage) ? convertKeysToCamelCase(JSON.parse(lastMessage.data)) : null;

    // const data: ChromecastStatus = JSON.parse(exampleData.bd);
    // console.log(data);

    // console.log(JSON.stringify(data))

    function renderApp() {
        if (data == null)
            return <InitializingApp status={data} />

        if (data.cast.appId == null)
            return <LoadingApp status={data} />

        const mediaApp = mediaApps[data.cast.displayName];

        if (mediaApp) {
            if (data.media == null || data.media.contentId == null)
                return <MediaLoadingScreen {...mediaApp.loading} />
            return <MediaApp {...mediaApp.data(data)} />
        }

        return <BackdropApp status={data} />
    }

    return (
        <WidgetFrame className={classes.root} config={config} dashboardConfig={dashboardConfig}>
            {renderApp()}
            <WidgetMenu id={config.id} settings={config.settings} settingsFormFields={[]} />
        </WidgetFrame>
    )
});
