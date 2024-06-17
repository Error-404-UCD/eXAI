import React, { useState } from 'react';
import '../CSS/LNavbar.css';
import { FaGithub, FaBook, FaDatabase, FaUsers } from 'react-icons/fa';

function LNavbar() {
    const [isOpen, setIsOpen] = useState(false);
   
    const toggleNavbar = () => setIsOpen(!isOpen);


    return (
        <div className={`navbar ${isOpen ? 'open' : ''}`} onClick={toggleNavbar}>
            <ul className="nav-items">
                <li><FaBook className="icon" /><span className="nav-text">{isOpen && 'About'}</span></li>
                <li><FaGithub className="icon" /><span className="nav-text">{isOpen && 'GitHub'}</span></li>
                <li><FaDatabase className="icon" /><span className="nav-text">{isOpen && 'Libraries'}</span></li>
                <li><FaBook className="icon" /><span className="nav-text">{isOpen && 'Report'}</span></li>
                <li><FaDatabase className="icon" /><span className="nav-text">{isOpen && 'Dataset'}</span></li>
                <li><FaUsers className="icon" /><span className="nav-text">{isOpen && 'Team Details'}</span></li>
            </ul>
        </div>
    );
}

export default LNavbar;
