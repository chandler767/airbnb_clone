import React from 'react';

import {
    REQUEST_ERROR,
    REQUEST_INITIATED,
    REQUEST_COMPLETED    
} from 'js/Constants/PlaceConstants';

import request from 'superagent';

export function fetchPlacesChange(response, error) {
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

export function fetchPlaces() { // Make request to api
    return dispatch => {
        dispatch(fetchPlacesChange(null, null));
        request.get("http://localhost:3306/places/").then((data) => {
                dispatch(fetchPlacesChange(data.body, null));
            }).catch((error) => {
                dispatch(fetchPlacesChange(null, error));
            });
    };
}

