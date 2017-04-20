import React from 'react';

import {
    REQUEST_ERROR,
    REQUEST_INITIATED,
    REQUEST_COMPLETED    
} from 'js/Constants/CityConstants';

import request from 'superagent';

export function fetchCityChange(response, error) {
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

export function fetchCities() { // Make request to api
}
