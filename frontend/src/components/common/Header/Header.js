import React from 'react';
import GSFLogo from '../../../assets/GSFLogo.jpg';
import "./Header.css"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGithub } from '@fortawesome/free-brands-svg-icons';

const Header = () => {
  return (
    <header className="App-header">
       <img class="GSFLogo" src={GSFLogo} alt="GSF Logo"/>
       <a id='header-title' href="http://localhost:3000/">Eco Doc Sense</a>
       <a class="header-link" href="">Research</a>
       <a class="header-link" href="http://localhost:8000/docs#/">API Documentation</a>
       <a class="header-link" href="https://greensoftware.foundation/">Green Software Foundation ⭷</a>
       <a href="https://github.com/KungfuNaman/green-software-foundation" target="_blank" rel="noopener noreferrer" className='github-link'>
        <FontAwesomeIcon icon={faGithub} size="2x" className="github-icon"/>
      </a>
    </header>
  );
};

export default Header;
