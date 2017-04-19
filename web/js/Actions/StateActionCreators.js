import React from 'react';

// get constants
import {
    REQUEST_ERROR,
    REQUEST_INITIATED,
    REQUEST_COMPLETED    
} from 'js/Constants/StateConstants';

import request from 'superagent';

export function RequestFinished(response, error) {
        if error == null {
            return {
            type: REQUEST_COMPLETED,
            payload: response.data // Response
        };
    } else {
        return {
            type: REQUEST_ERROR, // Error
            error
        };
    }
}

export function fetchStates() { // Make request to api
    return dispatch => {
        dispatch(requestInitiated());
        request.get("http://localhost:3306/states/").then((data) => {
                dispatch(RequestFinished(data.body, null));
            }).catch((error) => {
                dispatch(RequestFinished(null, error));
            });
    };
}

export function requestInitiated() {
    return {
        type: REQUEST_INITIATED,
    };
}
