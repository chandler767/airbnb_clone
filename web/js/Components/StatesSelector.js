import React, {Component} from 'react';
import StateItemSelector from 'js/Components/StateItemSelector';

export default class StatesSelector extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        this.props.fetchStates();
    }

    createStateList() {
        if (!this.props.states) {
            return <div></div>;
        }
        return (this.props.states.map((each) => {
            <li key={each.id}>
                {each.name} // List each
            </li>
        }));
    }

    render () {  
        return (
            <div>
                <h1>States:</h1>
                <ul>
                    {this.createStateList()} // Show list
                </ul>
            </div>
        );
    }
}

StatesSelector.propTypes = {
  fetchStates: React.PropTypes.func,
  states: React.PropTypes.array,
};