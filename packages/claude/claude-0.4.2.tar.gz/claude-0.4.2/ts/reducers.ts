import * as objectAssignDeep from 'object-assign-deep';
import { combineReducers } from 'redux';
import { Action, addDashboard, addWidget, removeWidget, selectDashboard, updateWidgetConfig, updateDashboard, setIsDalogOpen, setIdle } from './actions';
import { claudeLocalStorage } from './tools';
import { DashboardConfigMap, State, WidgetConfigMap } from './types';

import widgetRegistry from './widgetRegistry';

type ConfigAction = ReturnType<typeof addWidget> | ReturnType<typeof updateWidgetConfig>;

// [key in Action] is a mapped object type
type HandlerMap<T> = {[key in Action]?: (state: T, action: any) => T}

function mergeResource<T>(old: T, new_: T): T {
    return Object.assign<{}, T, T>({}, old, new_);
}

const dashboardHandlers: HandlerMap<DashboardConfigMap> = {
    [Action.ADD_DASHBOARD]: (state: DashboardConfigMap, action: ReturnType<typeof addDashboard>): DashboardConfigMap => {
        return mergeResource<DashboardConfigMap>(state, {
            [action.id]: {
                id: action.id,
                name: action.name,
                stepSize: action.stepSize,
                theme: 'blue',
                locale: 'en',
            }
        });
    },
    [Action.UPDATE_DASHBOARD]: (state: DashboardConfigMap, action: ReturnType<typeof updateDashboard>): DashboardConfigMap => {
        return mergeResource<DashboardConfigMap>(state, {[action.data.id]: action.data})
    },
}

const widgetHandlers: HandlerMap<WidgetConfigMap> = {
    [Action.ADD_WIDGET]: (state: WidgetConfigMap, action: ReturnType<typeof addWidget>): WidgetConfigMap => {
        return mergeResource<WidgetConfigMap>(state, {
            [action.id]: {
                id: action.id,
                type: action.widgetType,
                x: 10,
                y: 10,
                width: widgetRegistry[action.widgetType].defaultSize.w,
                height: widgetRegistry[action.widgetType].defaultSize.h,
                settings: {},
                dashboardId: action.dashboardId,
            }
        });
    },
    [Action.UPDATE_WIDGET_CONFIG]: (state: WidgetConfigMap, action: ReturnType<typeof updateWidgetConfig>): WidgetConfigMap => {
        let newState:WidgetConfigMap = objectAssignDeep({}, state, {[action.widgetId]: action.config});
        if (action.config.settings)
            newState[action.widgetId].settings = action.config.settings;
        return newState;
    },
    [Action.REMOVE_WIDGET]: (state: WidgetConfigMap, action: ReturnType<typeof removeWidget>): WidgetConfigMap => {
        let newState = Object.assign({}, state);
        delete newState[action.widgetId];
        return newState;
    },
}

function currentDashboardId(state = claudeLocalStorage.currentDashboardId, action: ReturnType<typeof selectDashboard>) {
    if (action.type == Action.SELECT_DASHBOARD) {
        return action.id;
    }
    return state;
}

function dashboards(state = {}, action: {type: Action}): DashboardConfigMap {
    if (action.type in dashboardHandlers)
        return dashboardHandlers[action.type](state, action);

    return state;
}

function widgets(state = {}, action: {type: Action}): WidgetConfigMap {
    if (action.type in widgetHandlers)
        return widgetHandlers[action.type](state, action);

    return state;
}

function isDialogOpen(state = false, action: ReturnType<typeof setIsDalogOpen>): boolean {
    if (action.type == Action.IS_DALOG_OPEN)
        return action.isOpen;
    return state;
}

function isIdle(state = false, action: ReturnType<typeof setIdle>): boolean {
    if (action.type == Action.SET_IDLE)
        return action.isIdle;
    return state;
}

const rootReducer = combineReducers<State>({
    currentDashboardId,
    dashboards,
    widgets,
    isDialogOpen,
    isIdle,
});

export default rootReducer;
