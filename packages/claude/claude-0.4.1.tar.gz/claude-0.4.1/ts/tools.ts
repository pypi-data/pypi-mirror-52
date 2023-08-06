
import {CommonWidgetProps, LocalStorageSchema} from "./types";

const localStorageHandler = {
    get: (target: LocalStorageSchema, name: string) => {
        const res = window.localStorage.getItem(name);
        return res == undefined ? target[name] : JSON.parse(res);
    },
    set: (target: LocalStorageSchema, name: string, value: any, receiver: any) => {
        window.localStorage.setItem(name, JSON.stringify(value));
        return true;
    },
};

export const claudeLocalStorage = new Proxy<LocalStorageSchema>(new LocalStorageSchema(), localStorageHandler);

export function copy<T>(data: T): T {
    return JSON.parse(JSON.stringify(data))
}

type WidgetStyleCallback<T = any> = (props: CommonWidgetProps<{}>) => T;

export namespace WidgetStyle {
    export function getRelativeSize(ratio: number): {width: WidgetStyleCallback<number>, height: WidgetStyleCallback<number>} {
        return {
            width: (props: CommonWidgetProps<{}>) => props.config.width * ratio,
            height: (props: CommonWidgetProps<{}>) => props.config.height * ratio,
        }
    }
}

export function capitalizeFirstLetter(string: string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

export const isObject = function(a: any) {
    return (!!a) && (a.constructor === Object);
};

export function convertKeysToCamelCase<T>(data: T): T {
    let res = {} as T
    for (const key in data) {
        let newKey = key.split(/-|_/).map(s => capitalizeFirstLetter(s)).join('');
        let value = data[key];
        res[newKey.charAt(0).toLowerCase() + newKey.slice(1)] = isObject(value) ? convertKeysToCamelCase(value) : value;
    }
    return res
}

export function humanFileSize(bytes: number, si: boolean = false): string {
    var thresh = si ? 1000 : 1024;
    if(Math.abs(bytes) < thresh) {
        return bytes + ' B';
    }
    var units = si
        ? ['kB','MB','GB','TB','PB','EB','ZB','YB']
        : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while(Math.abs(bytes) >= thresh && u < units.length - 1);
    return bytes.toFixed(1)+' '+units[u];
}
