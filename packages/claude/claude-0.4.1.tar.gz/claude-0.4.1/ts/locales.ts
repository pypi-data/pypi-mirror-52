
export type LocaleType = 'en' | 'hu';

export type Translations = {[s: string]: string | Translations};

type FlatLocalMessages = {[s: string]: string};

export class LocaleData {
    public title: string;
    public moment: string;
    public messages: Translations;

    private flatCache: FlatLocalMessages = null;

    constructor(title: string, moment: string, messages: Translations) {
        this.title = title;
        this.moment = moment;
        this.messages = messages;
    }

    get flatMessages(): FlatLocalMessages {
        if (this.flatCache)
            return this.flatCache;

        this.flatCache = {};

        const iter = (data: Translations, prefix: string) => {
            for (const [key, value] of Object.entries(data)) {
                if (value instanceof Object)
                    iter(value, `${key}.`)
                else
                    this.flatCache[`${prefix}${key}`] = value;
            }
        }

        iter(this.messages, '');

        return this.flatCache;
    }
}

export const claudeLocales: {[key in LocaleType]: LocaleData} = {
    en: new LocaleData('English', 'en-gb', {
            controlBar: {
                dashboards: 'dashboards',
                newDashboard: 'Create new dashboard',
                language: 'locale',
                settings: 'settings',
                addWidget: 'add widget',
            },
        },
    ),
    hu: new LocaleData('Hungarian', 'hu', {
            // controlBar: {
            //     dashboards: 'műszerfalak',
            //     newDashboard: 'Új műszerfal',
            //     language: 'nyelv',
            //     settings: 'beállítások',
            //     addWidget: 'műszer hozzáadása',
            // },
            controlBar: {
                dashboards: 'dashboards',
                newDashboard: 'Create new dashboard',
                language: 'locale',
                settings: 'settings',
                addWidget: 'add widget',
            },
        },
    ),
}
