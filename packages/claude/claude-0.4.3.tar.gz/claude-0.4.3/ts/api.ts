import {ServerStatusData, IdokepCurrentResponse, IdokepDaysResponse, IdokepHoursResponse, Transmission} from "./types";
import { convertKeysToCamelCase } from "./tools";

class ApiFetcher {

    public url: string;

    private async fetch(endpoint: string, data: any, method: 'POST' | 'GET' = 'POST') {
        const resp = await fetch(`/api/${endpoint}`, {
            method: method,
            headers: {
                'Content-type': 'application/json'
            },
            body: data ? JSON.stringify(data) : undefined,
        })

        return await resp.json();
    }

    async getServerStatus(ip: string, statusServerPort: number): Promise<ServerStatusData> {
        return this.fetch('server-status', {ip, statusServerPort})
    }

    async getIdokepCurrent(city: string): Promise<IdokepCurrentResponse> {
        return this.fetch(`idokep/current/${city}`, null, 'GET')
    }

    async getIdokepDays(city: string): Promise<IdokepDaysResponse> {
        return this.fetch(`idokep/days/${city}`, null, 'GET')
    }

    async getIdokepHours(city: string): Promise<IdokepHoursResponse> {
        return this.fetch(`idokep/hours/${city}`, null, 'GET')
    }

    async transmission(url: string, username?: string, password?: string): Promise<Transmission.ApiResponse> {
        return convertKeysToCamelCase(await this.fetch('transmission', {url, username, password}));
    }
}

export default new ApiFetcher();
