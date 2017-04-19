import React from 'react';

var styles = {
  header: {
    height: '60px',
    display: 'flex',
    flexDirection: 'row'
  },
  airbnb_logo: {
    height: '60px'
  },
  div: {
    width: '200px'
  }
}

const Header = (props)=> (
  <header style={styles.header}>
    <img
      style={styles.airbnb_logo}
      src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/2000px-Airbnb_Logo_B%C3%A9lo.svg.png" />
     <div className={styles.div}></div>
  </header>
);

export default Header;