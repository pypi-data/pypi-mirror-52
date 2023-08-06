import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { colors, createMuiTheme, CssBaseline, MuiThemeProvider } from "@material-ui/core";
import * as React from "react";
import * as ReactDOM from "react-dom";
import { Provider } from 'react-redux';
import App from "./containers/App";
import configureStore from "./store";
import { setIdle } from './actions';

library.add(fas, fab);

const store = configureStore();

const darkTheme = createMuiTheme({
    palette: {
        type: 'dark',
        primary: colors.cyan,
        secondary: colors.pink,
    },
});

ReactDOM.render(
    <React.Fragment>
        <CssBaseline />
        <Provider store={store}>
            <MuiThemeProvider theme={darkTheme}>
                <App/>
            </MuiThemeProvider>
        </Provider>
    </React.Fragment>,
    document.getElementById("body")
);

var idleIntervalId = 0;

function resetIdleTimer() {
    clearInterval(idleIntervalId);

    if (store.getState().isIdle)
        store.dispatch(setIdle(false));

    idleIntervalId = window.setTimeout(() => {
        store.dispatch(setIdle(true));
    }, 60000);
}

window.onmousemove = resetIdleTimer;
