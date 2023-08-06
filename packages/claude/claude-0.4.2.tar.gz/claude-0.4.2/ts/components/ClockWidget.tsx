import { createStyles, Link, withStyles, WithStyles } from '@material-ui/core';
import * as moment from 'moment';
import * as React from "react";
import { CommonWidgetProps } from "../types";
import WidgetFrame from "../containers/WidgetFrame";
import WidgetMenu from "./WidgetMenu";
import {WidgetStyle} from "../tools";

// some weird rendering shit in Raspberry
const isRasbperry: boolean = !!navigator.userAgent.match('Raspbian');

const styles = () => createStyles({
    body: {
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        overflow: 'hidden',
    },
    clock: {
        textAlign: 'center',
        lineHeight: isRasbperry ? '120%' : '90%',
        fontFamily: 'Digital7',
        marginTop: isRasbperry ? '-0.3em' : 0,
        fontSize: WidgetStyle.getRelativeSize(0.8).height,
    },
    date: {
        textAlign: 'center',
        lineHeight: '95%',
        fontWeight: 'bold',
        fontSize: WidgetStyle.getRelativeSize(0.17).height,
    },
});

export class Settings {
    showDate: boolean = true;
    timeFormat: string = 'HH:mm';
    dateFormat: string = 'YYYY. MMMM D. dddd';
}

type State = {
    time: string,
}

class ClockWidget extends React.Component<CommonWidgetProps<Settings> & WithStyles<typeof styles>, State> {

    private timerId: number;

    constructor(props) {
        super(props);
        this.timerId = 0;
        this.state = {
            time: this.now,
        }
    }

    private get now(): string {
        return moment(new Date().getTime()).format(this.props.config.settings.timeFormat);
    }

    componentDidMount() {
        this.timerId = window.setInterval(() => {
            const now = this.now;
            if (now != this.state.time)
                this.setState({time: this.now})
        }, 1000);
    }

    componentWillUnmount() {
        window.clearInterval(this.timerId);
    }

    render() {
        const {config, classes, dashboardConfig} = this.props;

        const dateComp = () => {
            return (
                <div className={classes.date}>
                    {moment(new Date().getTime()).format(config.settings.dateFormat)}
                </div>
            )
        }

        const settingsDialogText = <span>
            For more info about date & time formats<br/>see the <Link href="https://momentjs.com/docs/#/displaying/format/"
            target="blank">Moment.js</Link> documentation.
        </span>

        return (
            <WidgetFrame
                config={config}
                dashboardConfig={dashboardConfig}
            >
                <div className={classes.body}>
                    <div className={classes.clock}>
                        {this.state.time}
                    </div>
                    {config.settings.showDate ? dateComp() : null}
                </div>
                <WidgetMenu id={config.id} settings={config.settings} dialogText={settingsDialogText} settingsFormFields={[{
                    name: "timeFormat",
                    label: "Time format",
                }, {
                    name: "dateFormat",
                    label: "Date format",
                }, {
                    name: "showDate",
                    label: "Show date",
                }]} />
            </WidgetFrame>
        )
    }
}

export default withStyles(styles)(ClockWidget);
