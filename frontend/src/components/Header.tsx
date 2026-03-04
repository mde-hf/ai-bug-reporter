import { NavLink } from 'react-router-dom';
import './Header.css';

export default function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-title">
          <h1>Bug Reporter</h1>
          <p className="tribe-label">TRIBE: Loyalty & Virality</p>
        </div>
        <nav className="header-nav">
          <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Report Bug
          </NavLink>
          <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Dashboard
          </NavLink>
          <NavLink to="/test-cases" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            AI Test Cases
          </NavLink>
          <NavLink to="/qa-analysis" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            QA Analysis
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
