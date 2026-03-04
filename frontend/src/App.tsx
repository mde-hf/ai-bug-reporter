import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import ReportBugPage from './pages/ReportBugPage';
import DashboardPage from './pages/DashboardPage';
import TestCasesPage from './pages/TestCasesPage';

function App() {
  return (
    <div className="app">
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<ReportBugPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/test-cases" element={<TestCasesPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
