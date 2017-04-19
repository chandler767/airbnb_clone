import React from 'react';

const styles = {
  footer: {
      height: '40px',
      borderStyle: 'solid',
      textAlign: 'center'
    }
}

const Footer = (props)=> (
  <footer style={styles.footer}>
    <p>&copy; 2017 Chandler and Josh</p>
  </footer>
);

export default Footer;