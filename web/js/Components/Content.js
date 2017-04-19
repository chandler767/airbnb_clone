import React from 'react';

var styles = {
  content: {
  	position: "absolute"
    width: "100%",
    left: "300px",
    top: "60px",
    bottom: "40px"
  }
}

export default class Content extends React.Component {
    render () {
        return (
            <main className={styles.content}>
            </main>
        );
    }
