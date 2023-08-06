import { CSSProperties } from "react";

export type ClaudeTheme = {
    title: string,
    controlBar: {
        openerColor: string,
    },
    dashboard: CSSProperties,
    widget: CSSProperties,
    calendar: {
        today: CSSProperties,
    },
}

export type ClaudeThemeType = 'blue' | 'grey';

export const claudeThemes: {[key in ClaudeThemeType]: ClaudeTheme} = {
    blue: {
        title: 'Blue',
        controlBar: {
            openerColor: 'white',
        },
        dashboard: {
            backgroundImage: 'url(/static/pics/canvas_blue_texture_surface_shadow_44965_1920x1200.jpg)'
        },
        widget: {
            color: '#eee',
            backgroundColor: 'rgba(0,0,0,0.4)',
        },
        calendar: {
            today: {
                borderRadius: 100,
                border: '3px solid #eee',
            },
        },
    },
    grey: {
        title: 'Grey',
        controlBar: {
            openerColor: 'white',
        },
        dashboard: {
            backgroundColor: '#333',
        },
        widget: {
            color: '#eee',
            backgroundColor: 'rgba(0,0,0,0.3)',
        },
        calendar: {
            today: {
                backgroundColor: 'rgba(255,255,255,0.2)',
            },
        },
    },
};
