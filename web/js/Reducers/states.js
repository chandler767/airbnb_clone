import { Map, fromJS } from 'immutable';
import React from 'react';
import {REQUEST_COMPLETED} from 'js/Constants/StateConstants';

// Will retun state information otherwise passes to store to rerender.
export default function states(state = null, action = '') {
    switch (action.type) {
        case REQUEST_COMPLETED:
            return action.payload;
        default:
            return state;
    }
}