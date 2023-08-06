import { BaseWidgetConfig, DashboardConfig } from "./types";
import { claudeLocalStorage } from "./tools";
import { LocaleType } from "./locales";
const uuid = require('uuid/v4');

export enum Action {
    ADD_WIDGET = 'ADD_WIDGET',
    ADD_DASHBOARD = 'ADD_DASHBOARD',
    UPDATE_DASHBOARD = 'UPDATE_DASHBOARD',
    REMOVE_WIDGET = 'REMOVE_WIDGET',
    UPDATE_WIDGET_CONFIG = 'UPDATE_WIDGET_CONFIG',
    SELECT_DASHBOARD = 'SELECT_DASHBOARD',
    IS_DALOG_OPEN = 'IS_DALOG_OPEN',
    SET_IDLE = 'SET_IDLE',
}

export const addDashboard = (name: string, stepSize: number) => ({
    type: Action.ADD_DASHBOARD,
    name,
    stepSize,
    id: uuid(),
})

export const updateDashboard = (data: DashboardConfig) => ({
    type: Action.UPDATE_DASHBOARD,
    data,
})

export const addWidget = (dashboardId: string, widgetType: string) => ({
    type: Action.ADD_WIDGET,
    dashboardId,
    widgetType,
    id: uuid(),
})

export const updateWidgetConfig = (widgetId: string, config: Partial<BaseWidgetConfig>) => ({
    type: Action.UPDATE_WIDGET_CONFIG,
    widgetId,
    config,
})

export const removeWidget = (widgetId: string) => ({
    type: Action.REMOVE_WIDGET,
    widgetId,
})

export const selectDashboard = (id: string) => {
    claudeLocalStorage.currentDashboardId = id;
    return {
        type: Action.SELECT_DASHBOARD,
        id,
    }
}

export const setIsDalogOpen = (isOpen: boolean) => {
    return {
        type: Action.IS_DALOG_OPEN,
        isOpen,
    }
}

export const setIdle = (isIdle: boolean) => ({
    type: Action.SET_IDLE,
    isIdle,
})
