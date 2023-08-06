
import { connect } from 'react-redux';
import { State } from '../types';
import { bindActionCreators } from "redux";

import {updateWidgetConfig} from '../actions';

import WidgetFrame, {StateProps, DispatchProps, OwnProps} from '../components/WidgetFrame';

function mapStateToProps(state: State): StateProps {
    const {isDialogOpen, isIdle} = state;

    return {
        isDialogOpen,
        isIdle,
    }
}

const mapDispatchToProps = dispatch => bindActionCreators({updateWidgetConfig}, dispatch)

export default connect<StateProps, DispatchProps, OwnProps>(mapStateToProps, mapDispatchToProps)(WidgetFrame)
