import React from 'react';

import {
    REQUEST_ERROR,
    REQUEST_INITIATED,
    REQUEST_COMPLETED    
} from 'js/Constants/StateConstants';

import request from 'superagent';

export function fetchStateChange(response, error) {
    if error == null {
        if response == null { 
            return { // If nothing was passed the the request was started.
                type: REQUEST_INITIATED,
            };
        } else {
            return {
                type: REQUEST_COMPLETED,
                payload: response.data // Response
            };
        }
    } else {
        return {
            type: REQUEST_ERROR, // Error
            error
        };   
    }    
}