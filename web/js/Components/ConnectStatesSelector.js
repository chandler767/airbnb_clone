import React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Map } from 'immutable';

import {fetchStates} from 'js/Actions/StateActionCreators';

import component from 'js/Components/StatesSelector';

export function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    fetchStates,
  }, dispatch);
}

export function mapStateToProps(state) {
  return {
    states: state.StateReducer,
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(component);