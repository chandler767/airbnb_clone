import React from 'react';

const State = (props) => {
	<h3>{props.name}</h3>
};

State.propTypes = {
    name: React.PropTypes.string.isRequired
};

export default State;