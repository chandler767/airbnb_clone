import { bindActionCreators } from 'redux';
import component from 'js/Components/StatesSelector';
import { connect } from 'react-redux';
import { fetchStates } from 'js/Actions/StateActionCreators';
import { Map } from 'immutable';
import React from 'react';


export function mapToProp(dispatch) {
  return bindActionCreators({
    fetchStates,
  }, dispatch);
}

export function StateToProp(state) {
  return {
    states: state.StateReducer, // see Reducers/states.js
  };
}

export default connect(StateToProp, mapToProp)(component);