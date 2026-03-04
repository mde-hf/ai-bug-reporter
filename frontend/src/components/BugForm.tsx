import { useState, useEffect, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { bugApi } from '@/services/api';
import type { BugRequest, Project, Priority, Environment } from '@/types/api';
import DuplicatesList from './DuplicatesList';
import './BugForm.css';

export default function BugForm() {
  const [project, setProject] = useState<Project | ''>('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [steps, setSteps] = useState('');
  const [expected, setExpected] = useState('');
  const [actual, setActual] = useState('');
  const [priority, setPriority] = useState<Priority>('Low');
  const [environment, setEnvironment] = useState<Environment>('Staging');
  const [attachments, setAttachments] = useState<File[]>([]);
  const [duplicates, setDuplicates] = useState<any[]>([]);
  const [checkingDuplicates, setCheckingDuplicates] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [showWip, setShowWip] = useState(false);

  // Debounced duplicate check
  const checkDuplicates = useCallback(async (searchTitle: string) => {
    if (searchTitle.length < 3) {
      setDuplicates([]);
      return;
    }

    setCheckingDuplicates(true);
    try {
      const results = await bugApi.checkDuplicates(searchTitle, description);
      setDuplicates(results);
    } catch (error) {
      console.error('Failed to check duplicates:', error);
    } finally {
      setCheckingDuplicates(false);
    }
  }, [description]);

  // Auto-check duplicates when title changes
  useEffect(() => {
    const timer = setTimeout(() => {
      if (title && project === 'loyalty-2.0') {
        checkDuplicates(title);
      }
    }, 500); // 500ms debounce

    return () => clearTimeout(timer);
  }, [title, project, checkDuplicates]);

  // Handle project selection
  const handleProjectChange = (value: string) => {
    setProject(value as Project);
    if (value === 'loyalty-2.0') {
      setShowForm(true);
      setShowWip(false);
    } else if (value) {
      setShowForm(false);
      setShowWip(true);
    } else {
      setShowForm(false);
      setShowWip(false);
    }
  };

  // Handle file upload
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setAttachments(Array.from(e.target.files));
    }
  };

  // Create bug mutation
  const createBugMutation = useMutation({
    mutationFn: async () => {
      const bugData: BugRequest = {
        title,
        description,
        steps_to_reproduce: steps,
        expected_behavior: expected,
        actual_behavior: actual,
        priority,
        environment,
        project: 'loyalty-2.0',
      };
      return bugApi.createBug(bugData, attachments);
    },
    onSuccess: (data) => {
      alert(`Success! Bug created: ${data.key}\n${data.message}`);
      // Reset form
      setTitle('');
      setDescription('');
      setSteps('');
      setExpected('');
      setActual('');
      setPriority('Low');
      setEnvironment('Staging');
      setAttachments([]);
      setDuplicates([]);
    },
    onError: (error: any) => {
      alert(`Error: ${error.response?.data?.error || error.message}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!project) {
      alert('Please select a project');
      return;
    }
    createBugMutation.mutate();
  };

  return (
    <div className="bug-form-container">
      <div className="form-group">
        <label htmlFor="project">
          Project <span className="required">*</span>
        </label>
        <select
          id="project"
          value={project}
          onChange={(e) => handleProjectChange(e.target.value)}
          required
        >
          <option value="">-- Choose a project --</option>
          <option value="loyalty-mission">Loyalty Mission Squad</option>
          <option value="virality">Virality Squad</option>
          <option value="rewards">Rewards Squad</option>
          <option value="loyalty-2.0">Loyalty 2.0 Bug Reporting</option>
        </select>
        <div className="help-text">Select the project you're reporting a bug for</div>
      </div>

      {showWip && (
        <div className="wip-screen">
          <div className="wip-content">
            <h2>Work In Progress</h2>
            <p>Bug reporting for this squad is coming soon!</p>
            <p className="wip-subtitle">Please check back later or contact your squad lead for assistance.</p>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => handleProjectChange('')}
            >
              Back to Squad Selection
            </button>
          </div>
        </div>
      )}

      {showForm && (
        <form onSubmit={handleSubmit} className="bug-form">
          <div className="form-group">
            <label htmlFor="title">
              Bug Title <span className="required">*</span>
            </label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., Login button doesn't work on mobile"
              required
            />
            <div className="help-text">Brief description of the issue</div>
            {checkingDuplicates && <div className="checking-duplicates">Checking for duplicates...</div>}
          </div>

          {duplicates.length > 0 && <DuplicatesList duplicates={duplicates} />}

          <div className="form-group">
            <label htmlFor="description">
              Description <span className="required">*</span>
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              placeholder="Describe what went wrong..."
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="attachments">Attachments (Screenshots, Videos)</label>
            <input
              type="file"
              id="attachments"
              onChange={handleFileChange}
              multiple
              accept="image/*,video/*"
              className="file-input"
            />
            <div className="help-text">Upload screenshots or videos (max 50MB per file)</div>
            {attachments.length > 0 && (
              <div className="file-list">
                {attachments.map((file, idx) => (
                  <div key={idx} className="file-item">{file.name}</div>
                ))}
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="steps">
              Steps to Reproduce <span className="required">*</span>
            </label>
            <textarea
              id="steps"
              value={steps}
              onChange={(e) => setSteps(e.target.value)}
              rows={4}
              placeholder="1. Go to...&#10;2. Click on...&#10;3. See error..."
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="expected">
                Expected Behavior <span className="required">*</span>
              </label>
              <textarea
                id="expected"
                value={expected}
                onChange={(e) => setExpected(e.target.value)}
                rows={3}
                placeholder="What should happen?"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="actual">
                Actual Behavior <span className="required">*</span>
              </label>
              <textarea
                id="actual"
                value={actual}
                onChange={(e) => setActual(e.target.value)}
                rows={3}
                placeholder="What actually happens?"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="environment">Environment</label>
              <select
                id="environment"
                value={environment}
                onChange={(e) => setEnvironment(e.target.value as Environment)}
              >
                <option value="Production">Production</option>
                <option value="Staging">Staging</option>
                <option value="Local">Local</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="priority">Priority</label>
              <select
                id="priority"
                value={priority}
                onChange={(e) => setPriority(e.target.value as Priority)}
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>

          <div className="button-group">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={createBugMutation.isPending}
            >
              {createBugMutation.isPending ? (
                <>
                  <span className="spinner"></span>
                  Creating...
                </>
              ) : (
                'Create Bug Report'
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
