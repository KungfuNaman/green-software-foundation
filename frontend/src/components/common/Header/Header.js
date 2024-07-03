import React from 'react';
import GSFLogo from '../../../assets/GSFLogo.jpg';
import "./Header.css"
const Header = () => {
  return (
    <header className="App-header">
       <img class="GSFLogo" src={GSFLogo} alt="GSF Logo"/>
       Eco Doc Sense
      </header>
  );
};

export default Header;
