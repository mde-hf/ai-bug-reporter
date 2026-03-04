import { useQuery } from '@tanstack/react-query';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';
import { bugApi } from '@/services/api';
import type { Project } from '@/types/api';
import './Dashboard.css';

ChartJS.register(ArcElement, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface Props {
  project: Project;
}

export default function Dashboard({ project }: Props) {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['epic-stats', project],
    queryFn: () => bugApi.getEpicStats(),
    enabled: project === 'loyalty-2.0',
    refetchInterval: 15 * 60 * 1000, // Auto-refresh every 15 minutes
  });

  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading statistics...</p>
      </div>
    );
  }

  if (error) {
    return <div className="dashboard-error">Failed to load statistics</div>;
  }

  if (!stats) return null;

  const resolvedPercent = stats.total_count > 0
    ? Math.round((stats.resolved_count / stats.total_count) * 100)
    : 0;

  const createJiraUrl = (jql: string) => {
    return `https://hellofresh.atlassian.net/issues/?jql=${encodeURIComponent(jql)}`;
  };

  const chartData = {
    labels: stats.creation_trend.map(d => d.date),
    datasets: [
      {
        label: 'Bugs Created',
        data: stats.creation_trend.map(d => d.count),
        borderColor: 'rgb(145, 193, 30)',
        backgroundColor: 'rgba(145, 193, 30, 0.1)',
        tension: 0.3,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div
          className="stat-card clickable"
          onClick={() => window.open(createJiraUrl('parent = REW-323 AND type = Bug'), '_blank')}
        >
          <h3>Total Bugs</h3>
          <div className="stat-value">{stats.total_count}</div>
          <div className="stat-label">In Epic REW-323</div>
        </div>

        <div
          className="stat-card clickable"
          onClick={() => window.open(createJiraUrl('parent = REW-323 AND type = Bug AND statusCategory != Done'), '_blank')}
        >
          <h3>Open</h3>
          <div className="stat-value" style={{ color: '#F59E0B' }}>{stats.open_count}</div>
          <div className="stat-label">{Math.round((stats.open_count / stats.total_count) * 100)}% of total</div>
        </div>

        <div
          className="stat-card clickable"
          onClick={() => window.open(createJiraUrl('parent = REW-323 AND type = Bug AND statusCategory = Done'), '_blank')}
        >
          <h3>Resolved</h3>
          <div className="stat-value" style={{ color: '#10B981' }}>{stats.resolved_count}</div>
          <div className="stat-label">{resolvedPercent}% of total</div>
        </div>

        <div className="stat-card">
          <h3>Avg Resolution</h3>
          <div className="stat-value" style={{ color: '#8B5CF6' }}>{stats.avg_resolution_days}</div>
          <div className="stat-label">days to resolve</div>
        </div>
      </div>

      <div className="dashboard-section">
        <h3>Priority × Status Matrix</h3>
        <div className="matrix-table">
          <table>
            <thead>
              <tr>
                <th>Priority</th>
                {Object.keys(stats.by_status).map(status => (
                  <th key={status}>{status}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Object.entries(stats.priority_matrix).map(([priority, statuses]) => (
                <tr key={priority}>
                  <td><strong>{priority}</strong></td>
                  {Object.keys(stats.by_status).map(status => (
                    <td
                      key={status}
                      className="matrix-cell clickable"
                      onClick={() => window.open(createJiraUrl(`parent = REW-323 AND type = Bug AND priority = "${priority}" AND status = "${status}"`), '_blank')}
                    >
                      {statuses[status] || 0}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="dashboard-section">
        <h3>Platform Distribution</h3>
        <div className="platform-grid">
          {Object.entries(stats.by_platform).map(([platform, count]) => (
            <div key={platform} className="platform-card">
              <div className="platform-name">{platform}</div>
              <div className="platform-count">{count}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="dashboard-section">
        <h3>Bug Creation Trend (Last 10 Days)</h3>
        <div className="chart-container">
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
}
