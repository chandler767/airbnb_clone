import React from 'react';

// get constants
import {
    STATES_FETCH_ERROR,
    STATES_FETCH_INITIATED,
    STATES_FETCH_COMPLETED    
} from 'js/Constants/StateConstants';

import request from 'superagent';

export function stateFetchInitiated() {
    return {
        type: STATES_FETCH_INITIATED,
    };
}

export function stateFetchError(error) {
    return {
        type: STATES_FETCH_ERROR,
        error
    };
}

export function stateFetchCompleted(response) {
    return {
        type: STATES_FETCH_COMPLETED,
        payload: response.data // Response from API
    };
}

export function fetchStates() { // Make request to api
    return dispatch => {
        dispatch(stateFetchInitiated());
        request.get("http://localhost:3306/states/").then((data) => {
                dispatch(stateFetchCompleted(data.body));
            }).catch((error) => {
                dispatch(stateFetchError(error));
            });
    };
}
