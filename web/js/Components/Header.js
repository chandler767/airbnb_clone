import React from 'react';

var styles = {
  header: {
    height: '60px',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingBottom: '5vh'
  },
  logo: {
    height: '60px'
  },
  div: {
    width: '200px'
  }
}

const Header = (props)=> (
  <header style={styles.header}>
    <img
      style={styles.logo}
      src="http://logok.org/wp-content/uploads/2014/07/Airbnb-new-logo-2014.png" />
     <div className={styles.div}></div>
  </header>
);

export default Header;