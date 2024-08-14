import React from 'react';
import GSFLogo from '../../../assets/GSFLogo.jpg';
import "./Header.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGithub } from '@fortawesome/free-brands-svg-icons';

const Header = () => {
  return (
    <header className="App-header">
       <img class="GSFLogo" src={GSFLogo} alt="GSF Logo"/>
       Eco Doc Sense
       <href class="header-link" href="">Research Documentation</href>
       <a href="https://github.com/KungfuNaman/green-software-foundation" target="_blank" rel="noopener noreferrer" className='github-link'>
        <FontAwesomeIcon icon={faGithub} size="2x" className="github-icon"/>
      </a>
    </header>
  );
};

export default Header;
