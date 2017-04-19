import React from 'react';

const styles = {
  leftcol: {
    width: '300px',
    borderStyle: 'solid',
    position: 'absolute',
    top: '60px',
    backgroundColor: '#F6F6F6',
    bottom: '40px'
  }
}

var LeftColumn = React.createClass({
  propTypes: {

  },
  getDefaultProps() {
    return {
      
    };
  },
  render: function () {
    return (
      <aside style={styles.leftcol}>
      </aside>
    )
  }
});

export default LeftColumn;