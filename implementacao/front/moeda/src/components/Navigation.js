import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/aluno">Aluno</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navigation;
