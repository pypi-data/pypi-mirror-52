import {createStyles, withStyles, WithStyles} from '@material-ui/core';
import {ResizeDirection} from "re-resizable";
import * as React from "react";
import {DraggableEvent} from "react-draggable";
import {DraggableData, Position, ResizableDelta, Rnd, RndResizeCallback} from "react-rnd";
import {DashboardConfig, UpdateWidgetConfigAction, WidgetConfig} from "../types";
import { claudeThemes } from "../themes";
import * as classNames from 'classnames';


const styles = () => createStyles({
    body: {
        borderRadius: 5,
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        backdropFilter: 'blur(3px)',
        '&:hover .widget-menu': {
            opacity: 1,
        },
    },
    hiddenMenuIcon: {
        '& .widget-menu': {
            opacity: 0,
        },
    }
});

export interface OwnProps {
    config: WidgetConfig,
    children: React.ReactNode,
    removeButton?: boolean,
    onResize?: RndResizeCallback,
    dashboardConfig: DashboardConfig,
    style?: React.CSSProperties,
    className?: string,
}

export type StateProps = {
    isDialogOpen: boolean,
    isIdle: boolean,
}

export type DispatchProps = {
    updateWidgetConfig: UpdateWidgetConfigAction,
}

function isEquals(o1: Object, o2: Object): boolean {
    for (const k of Object.keys(o1)) {
        if (o1[k] !== o2[k])
            return false
    }
    return true
}

function WidgetFrame(props: OwnProps & StateProps & DispatchProps & WithStyles<typeof styles>) {
    const {config, dashboardConfig, updateWidgetConfig, classes, isDialogOpen, isIdle} = props;
    const [position, setPosition] = React.useState({
        x: config.x,
        y: config.y,
    });
    const [size, setSize] = React.useState({
        width: config.width,
        height: config.height,
    });

    const updatePosition = (newData: typeof position) => {
        if (isEquals(newData, position))
            return;
        setPosition(newData);
        updateWidgetConfig(config.id, newData)
    };

    const onDragStop = (e: DraggableEvent, data: DraggableData) => {
        updatePosition({
            x: data.lastX,
            y: data.lastY,
        })
    };

    const onDrag = (e: DraggableEvent, data: DraggableData) => {
        updatePosition( {
            x: data.x,
            y: data.y,
        })
    };

    const onResizeStop = (e: MouseEvent, dir: ResizeDirection, elementRef: HTMLDivElement, delta: ResizableDelta, newPosition: Position) => {
        onResize(e, dir, elementRef, delta, newPosition);
    };

    const onResize = (e: MouseEvent, dir: ResizeDirection, elementRef: HTMLDivElement, delta: ResizableDelta, newPosition: Position) => {
        const newData = {
            x: newPosition.x,
            y: newPosition.y,
            width: elementRef.offsetWidth,
            height: elementRef.offsetHeight,
        };
        if (isEquals(newData, {...position, ...size}))
            return;

        updateWidgetConfig(config.id, newData);

        setPosition({...newData});
        setSize({...newData});
    };

    return <Rnd
        position={{
            x: config.x,
            y: config.y
        }}
        size={{
            width: config.width,
            height: config.height,
        }}
        dragGrid={[dashboardConfig.stepSize, dashboardConfig.stepSize]}
        resizeGrid={[dashboardConfig.stepSize, dashboardConfig.stepSize]}
        onDragStop={onDragStop}
        onResizeStop={onResizeStop}
        onDrag={onDrag}
        onResize={onResize}
        disableDragging={isDialogOpen}
        style={{userSelect: 'none'}}
        enableUserSelectHack={false}
    >
        <div
            className={classNames(classes.body, props.className, {[classes.hiddenMenuIcon]: isIdle})}
            style={{...claudeThemes[dashboardConfig.theme].widget, ...props.style}}
        >
            { props.children }
        </div>
    </Rnd>
}

export default withStyles(styles)(WidgetFrame)
