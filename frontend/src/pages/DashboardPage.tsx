import { useState } from 'react';
import Dashboard from '@/components/Dashboard';
import type { Project } from '@/types/api';
import './DashboardPage.css';

export default function DashboardPage() {
  const [project, setProject] = useState<Project | ''>('');
  const [showDashboard, setShowDashboard] = useState(false);
  const [showWip, setShowWip] = useState(false);

  const handleProjectChange = (value: string) => {
    setProject(value as Project);
    if (value === 'loyalty-2.0') {
      setShowDashboard(true);
      setShowWip(false);
    } else if (value) {
      setShowDashboard(false);
      setShowWip(true);
    } else {
      setShowDashboard(false);
      setShowWip(false);
    }
  };

  return (
    <div className="page dashboard-page">
      <div className="dashboard-header">
        <div className="form-group">
          <label htmlFor="dashboardProject">
            Project <span className="required">*</span>
          </label>
          <select
            id="dashboardProject"
            value={project}
            onChange={(e) => handleProjectChange(e.target.value)}
            required
          >
            <option value="">-- Select a project --</option>
            <option value="loyalty-mission">Loyalty Mission Squad</option>
            <option value="virality">Virality Squad</option>
            <option value="rewards">Rewards Squad</option>
            <option value="loyalty-2.0">Loyalty 2.0 Bug Reporting</option>
          </select>
          <div className="help-text">Select a project to view dashboard metrics</div>
        </div>
      </div>

      {showWip && (
        <div className="wip-screen">
          <div className="wip-content">
            <h2>Work In Progress</h2>
            <p>Dashboard for this project is coming soon!</p>
            <p className="wip-subtitle">
              Please check back later or select Loyalty 2.0 Bug Reporting to view active dashboard.
            </p>
          </div>
        </div>
      )}

      {showDashboard && <Dashboard project={project as Project} />}
    </div>
  );
}
