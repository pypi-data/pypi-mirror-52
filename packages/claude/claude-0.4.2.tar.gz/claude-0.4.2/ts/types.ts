import { ThunkDispatch } from "redux-thunk";
import { Action } from "redux";
import { Dispatch } from "react";
import { ClaudeThemeType } from "./themes";
import { LocaleType } from './locales';

export class BaseWidgetSettings { }

export interface BaseWidgetConfig {
    x: number,
    y: number,
    width: number,
    height: number,
    settings: BaseWidgetSettings,
}

export interface WidgetConfig extends BaseWidgetConfig {
    id: string,
    type: string,
    dashboardId: string,
}

export type CommonWidgetProps<T = any> = {
    config: Omit<WidgetConfig, 'settings'> & { settings: T },
    dashboardConfig: DashboardConfig,
}

export type WidgetConfigList = Array<WidgetConfig>;
export type WidgetConfigMap = { [s: string]: WidgetConfig };

export class LocalStorageSchema {
    currentDashboardId: string = ''; // move to url?
}

export interface DashboardConfig {
    id: string,
    name: string,
    stepSize: number,
    theme: ClaudeThemeType,
    locale: LocaleType,
}

export type DashboardConfigMap = { [s: string]: DashboardConfig };

export interface State {
    currentDashboardId: string,
    dashboards: DashboardConfigMap,
    widgets: WidgetConfigMap,
    isDialogOpen: boolean,
    isIdle: boolean,
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, Action>;
export type Dispatcher = Dispatch<Action>;
export type UpdateWidgetConfigAction = (widgetId: string, config: Partial<BaseWidgetConfig>) => void;

export interface ServerStatusData {
    cpu: {
        cores: number,
    },
    hdd: Array<{
        device: string,
        free: number,
        label: string,
        mount: string,
        percent: number,
        total: number,
        used: number,
    }>,
    load: [number, number, number],
    memory: {
        available: number,
        free: number,
        percent: number,
        total: number,
        used: number,
    },
    uptime: number,
    ping: number,
}

export type IdokepCurrentResponse = {
    img: string,
    value: number,
}

export type IdokepDayData = {
    img: string,
    date: string,
    day: number,
    max: number,
    min: number
    precipitation: {
        value: number,
        probability: number,
    }
}

export type IdokepDaysResponse = Array<IdokepDayData>;

export type IdokepHourData = {
    hour: number,
    img: string,
    temp: number,
    precipitation: {
        value: number,
        probability: number,
    },
    wind: {
        img: string,
        angle: number,
    }
}

export type IdokepHoursResponse = Array<IdokepHourData>;

export namespace Chromecast {
    export namespace MediaMetaData {
        export interface YouTube {
            metadataType: number,
            title: string,
            subtitle: string,
            images: Array<{
                url: string,
            }>
        }
        export interface Spotify {
            albumName: string,
            artist: string,
            images: Array<{
                url: string,
                height: number,
                width: number,
            }>
            metadataType: number,
            songName: string,
            title: string,
        }
    }
    export interface Cast {
        appId: string,
        displayName: string,
        isActiveInput: boolean,
        isStandBy: boolean,
        namespaces: Array<string>,
        sessionId: string,
        statusText: string,
        transportId: string,
        volumeLevel: number,
        volumeMuted: boolean,
    }
    export type PlayerState = "PLAYING" | "BUFFERING" | "PAUSED" | "IDLE" | "UNKNOWN";
    export interface Media {
        contentId: string,
        contentType: string,
        currentSubtitleTracks: [], // TODO
        currentTime: number,
        duration: any,
        idleReason: any,
        lastUpdated: string,
        mediaCustomData: any,
        mediaMetadata: MediaMetaData.Spotify | MediaMetaData.YouTube,
        mediaSessionId: number,
        playbackRate: number,
        playerState: PlayerState,
        streamType: "BUFFERED" | "LIVE" | "UNKNOWN",
        subtitleTracks: {}, // TODO
        supportedMediaCommands: number, // bitflag: https://github.com/balloob/pychromecast/blob/6c71a3f3b9ae93465adf4be1a36f8260f273cc03/pychromecast/controllers/media.py#L44
        volumeLevel: number,
        volumeMuted: boolean,
    }

}

export namespace Transmission {
    export interface SessionStats {
        activeTorrentCount: number,
        cumulativeStats: {
            downloadedBytes: number,
            filesAdded: number,
            secondsActive: number,
            sessionCount: number,
            uploadedBytes: number,
        },
        currentStats: {
            downloadedBytes: number,
            filesAdded: number,
            secondsActive: number,
            sessionCount: number,
            uploadedBytes: number,
        },
        downloadSpeed: number,
        pausedTorrentCount: number,
        torrentCount: number,
        uploadSpeed: number,
    }

    export interface Torrent {
        eta: number,
        id: number,
        name: string,
        percentDone: number,
        rateDownload: number,
        sizeWhenDone: number,
        totalSize: number,
        rateUpload: number,
        peersConnected: number,
    }

    export interface ApiResponse {
        data: {
            sessionStats: SessionStats,
            torrents: Array<Torrent>,
        } | string,
        status: "success" | "error",
    }
}
