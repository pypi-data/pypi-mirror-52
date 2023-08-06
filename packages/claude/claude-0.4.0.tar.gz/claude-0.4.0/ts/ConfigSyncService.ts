
import * as ReconnectingWebSocket from 'reconnectingwebsocket';
import { AnyAction, Dispatch } from 'redux';
import { detailedDiff } from 'deep-object-diff';
import { Action } from './actions';

const syncableActions = [
    Action.ADD_WIDGET,
    Action.ADD_DASHBOARD,
    Action.UPDATE_DASHBOARD,
    Action.REMOVE_WIDGET,
    Action.UPDATE_WIDGET_CONFIG,
]

class ConfigSyncService {

    public url: string;
    private ws: ReconnectingWebSocket;
    private _connected: boolean = false;
    private _dispatcher: Dispatch<AnyAction>;

    constructor() {
        this.url = `ws://${window.location.host}/config-sync`;
        this.ws = new ReconnectingWebSocket(this.url);

        this.ws.onopen = this.onOpen.bind(this);
        this.ws.onmessage = this.onMessage.bind(this);
        this.ws.onclose = this.onClose.bind(this);
    }

    createReduxMiddleware() {
        return store => next => action => {
            const oldState = store.getState();
            let result = next(action);
            const newState = store.getState();

            if (syncableActions.indexOf(action.type) != -1 && !action.time) {
                this.ws.send(JSON.stringify({
                    action,
                    diff: detailedDiff(oldState, newState),
                }, (k, v) => v === undefined ? null : v)); // convert undefined to null
            }
            return result
        }
    }

    set dispatcher(val: Dispatch<AnyAction>) {
        this._dispatcher = val;
    }

    private onClose() {
        this._connected = false;
    }

    get connected(): boolean {
        return this._connected
    }

    private onOpen() {
        this._connected = true;
    }

    private onMessage(event) {
        const actionData = JSON.parse(event.data);
        this._dispatcher(actionData);
    }
}

export default new ConfigSyncService();
