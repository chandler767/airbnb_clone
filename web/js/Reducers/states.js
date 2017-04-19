// LEARN MORE ABOUT IMMUTABLE
import { Map, fromJS } from 'immutable';
import React from 'react';
import {STATES_FETCH_COMPLETED} from 'js/Constants/StateConstants';

// this is the reducer, which, after hearing the PRODUCT_FETCH_COMPLETED action type,
// will update the store. merge is perhaps another immutable thing?? if there is a 
// different action, then the reducer will just pass on the current, unadjusted state to store.
// component re/rendering follows.
export default function states(state = null, action = '') {
    switch (action.type) {
        case STATES_FETCH_COMPLETED:
            //console.log("HERE: ", action.payload);
            return action.payload;
        default:
            return state;
    }
}

// This reducer is really only listening for one action, the completion of an api call to get
// data on 'states', and then it returns a new updated data model.

