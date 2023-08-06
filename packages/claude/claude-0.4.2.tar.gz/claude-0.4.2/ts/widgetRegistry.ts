
import { BaseWidgetSettings } from './types';

import ClockWidget, { Settings as ClockWidgetSettings } from './components/ClockWidget';
import ServerStatusWidget, { Settings as ServerStatusWidgetSettings } from './components/ServerStatusWidget';
import CalendarWidget, { Settings as CalendarWidgetSettings } from "./components/CalendarWidget";
import StorageStatusWidget, { Settings as StorageStatusWidgetSettings } from './components/StorageStatusWidget';
import InfluxTable, { Settings as InfluxTableSettings } from './components/InfluxTable';
import IdokepCurrent, { Settings as IdokepCurrentSetting } from './components/IdokepCurrent';
import IdokepDays, {Settings as IdokepDaysSettings} from "./components/IdokepDays";
import IdokepHours, {Settings as IdokepHoursSettings} from "./components/IdokepHours";
import ChromecastWidget, {Settings as ChromecastWidgetSettings} from './components/ChromecastWidget';
import TransmissionWidget, {Settings as TransmissionWidgetSettings} from './components/TransmissionWidget';

export type WidgetRegistryType = {
    [s: string]: {
        factory: any,
        title: string,
        settingsType: typeof BaseWidgetSettings,
        defaultSize: {w: number, h: number},
    }
}


let reg: WidgetRegistryType = {
    storages: {
        factory: StorageStatusWidget,
        title: 'Storage status',
        settingsType: StorageStatusWidgetSettings,
        defaultSize: {w: 400, h: 200},
    },
    clock: {
        factory: ClockWidget,
        title: 'Clock',
        settingsType: ClockWidgetSettings,
        defaultSize: {w: 450, h: 200},
    },
    serverStatus: {
        factory: ServerStatusWidget,
        title: 'Server status',
        settingsType: ServerStatusWidgetSettings,
        defaultSize: {w: 400, h: 200},
    },
    calendar: {
        factory: CalendarWidget,
        title: 'Calendar',
        settingsType: CalendarWidgetSettings,
        defaultSize: {w: 250, h: 250},
    },
    influxTable: {
        factory: InfluxTable,
        title: 'Influx table',
        settingsType: InfluxTableSettings,
        defaultSize: {w: 300, h: 150},
    },
    idokepCurrent: {
        factory: IdokepCurrent,
        title: 'Idokep / Current',
        settingsType: IdokepCurrentSetting,
        defaultSize: {w: 220, h: 280},
    },
    idokepDays: {
        factory: IdokepDays,
        title: 'Idokep / Days',
        settingsType: IdokepDaysSettings,
        defaultSize: {w: 400, h: 200},
    },
    idokepHours: {
        factory: IdokepHours,
        title: 'Idokep / Hours',
        settingsType: IdokepHoursSettings,
        defaultSize: {w: 400, h: 200},
    },
    chromecast: {
        factory: ChromecastWidget,
        title: 'Chromecast',
        settingsType: ChromecastWidgetSettings,
        defaultSize: {w: 600, h: 300},
    },
    transmission: {
        factory: TransmissionWidget,
        title: 'Transmission',
        settingsType: TransmissionWidgetSettings,
        defaultSize: {w: 600, h: 300},
    },
};

export default reg;
