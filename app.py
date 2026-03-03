#!/usr/bin/env python3
"""
Simple AI Bug Reporting Tool
Checks for duplicate tickets before creating new ones in Jira.
"""

import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
JIRA_BASE_URL = os.environ.get('JIRA_BASE_URL', 'https://hellofresh.atlassian.net')
JIRA_CLOUD_ID = 'c563471e-8682-4abc-8fa9-5465b05abad5'  # HelloFresh cloud ID
JIRA_API_BASE = f'https://api.atlassian.com/ex/jira/{JIRA_CLOUD_ID}'
JIRA_EMAIL = os.environ.get('JIRA_EMAIL')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')
EPIC_KEY = os.environ.get('EPIC_KEY', 'REW-323')
PROJECT_KEY = os.environ.get('PROJECT_KEY', 'REW')

def get_jira_headers():
    """Get headers for Jira API requests."""
    return {
        'Authorization': f'Basic {get_basic_auth()}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

def get_basic_auth():
    """Get base64 encoded basic auth string."""
    import base64
    credentials = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    return base64.b64encode(credentials.encode()).decode()

def search_duplicates(title, description):
    """
    Search for potential duplicate bugs in Jira.
    Returns list of similar issues with emphasis on title matching.
    """
    import sys
    import urllib.parse
    
    print(f"\n[DEBUG] ===== SEARCHING FOR DUPLICATES =====", flush=True)
    print(f"[DEBUG] Title: '{title}'", flush=True)
    print(f"[DEBUG] Description: '{description}'", flush=True)
    sys.stdout.flush()
    
    # Simple direct search - search for individual words to catch partial matches
    title_words = [w.strip() for w in title.split() if len(w.strip()) > 2]
    
    if not title_words:
        # If title is too short or only has short words, search as-is
        simple_jql = f'project = {PROJECT_KEY} AND type = Bug AND summary ~ "{title}" ORDER BY created DESC'
    else:
        # Build JQL to search for any of the meaningful words in the title
        word_queries = ' OR '.join([f'summary ~ "{word}"' for word in title_words])
        simple_jql = f'project = {PROJECT_KEY} AND type = Bug AND ({word_queries}) ORDER BY created DESC'
    
    print(f"[DEBUG] JQL Query: {simple_jql}", flush=True)
    sys.stdout.flush()
    
    all_results = []
    
    try:
        # Use Atlassian Cloud API with proper /search/jql endpoint
        search_url = f'{JIRA_API_BASE}/rest/api/3/search/jql'
        
        print(f"[DEBUG] API URL: {search_url}", flush=True)
        sys.stdout.flush()
        
        response = requests.get(
            search_url,
            headers=get_jira_headers(),
            params={
                'jql': simple_jql,
                'maxResults': 20,
                'fields': 'summary,description,status,created,updated,parent'
            }
        )
        
        print(f"[DEBUG] Response status: {response.status_code}", flush=True)
        sys.stdout.flush()
        
        if response.status_code == 200:
            result_data = response.json()
            issues = result_data.get('issues', [])
            print(f"[DEBUG] Found {len(issues)} total issues", flush=True)
            sys.stdout.flush()
            
            for issue in issues:
                key = issue['key']
                summary = issue['fields']['summary']
                parent = issue['fields'].get('parent', {})
                parent_key = parent.get('key', 'No parent') if parent else 'No parent'
                
                print(f"[DEBUG] Issue {key}: '{summary}' (Parent: {parent_key})", flush=True)
                
                similarity = calculate_similarity(title, description, issue)
                print(f"[DEBUG] Similarity: {similarity}%", flush=True)
                
                if similarity >= 30:
                    all_results.append({
                        'key': key,
                        'summary': summary,
                        'status': issue['fields']['status']['name'],
                        'created': issue['fields']['created'],
                        'url': f"{JIRA_BASE_URL}/browse/{key}",
                        'similarity': similarity
                    })
                sys.stdout.flush()
        else:
            error_text = response.text[:500]
            print(f"[DEBUG] Error response ({response.status_code}): {error_text}", flush=True)
            sys.stdout.flush()
            
    except Exception as e:
        print(f"[ERROR] Exception during search: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
    
    # Sort by similarity score
    all_results.sort(key=lambda x: x['similarity'], reverse=True)
    
    print(f"[DEBUG] Returning {len(all_results)} results", flush=True)
    print(f"[DEBUG] ===== END SEARCH =====\n", flush=True)
    sys.stdout.flush()
    
    return all_results[:8]

def extract_key_terms(title, description):
    """Extract key terms from title and description."""
    # Simple keyword extraction (can be enhanced with NLP)
    import re
    
    # Remove common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    
    def clean_text(text):
        # Extract meaningful words
        words = re.findall(r'\w+', text.lower())
        return ' '.join([w for w in words if w not in common_words and len(w) > 2])
    
    title_keywords = clean_text(title)[:100]  # Limit length for JQL
    description_keywords = clean_text(description)[:100]
    
    # If description keywords are very similar to title, use title only
    if title_keywords in description_keywords:
        description_keywords = title_keywords
    
    return {
        'title_keywords': title_keywords,
        'description_keywords': description_keywords
    }

def calculate_similarity(title, description, issue):
    """
    Calculate similarity score between input and existing issue.
    Returns score between 0-100, with emphasis on title matching.
    """
    issue_summary = issue['fields']['summary'].lower()
    issue_description = issue['fields'].get('description', '')
    
    title_lower = title.lower()
    
    # Check for substring matches (partial matches in title)
    if title_lower in issue_summary or issue_summary in title_lower:
        return 95  # Very high similarity for substring matches
    
    # Split into words and clean
    title_words = set(title_lower.split())
    summary_words = set(issue_summary.split())
    
    # Remove common words for better matching
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'with', 'from', 'not', 'can', 'cant', 'cannot', 'does', 'doesnt', 'when', 'where', 'what', 'how', 'why'}
    title_words_filtered = {w for w in title_words if w not in common_words and len(w) > 1}
    summary_words_filtered = {w for w in summary_words if w not in common_words and len(w) > 1}
    
    # If no meaningful words after filtering, use original
    if not title_words_filtered:
        title_words_filtered = title_words
    if not summary_words_filtered:
        summary_words_filtered = summary_words
    
    # Calculate overlap
    if len(title_words_filtered) == 0 or len(summary_words_filtered) == 0:
        return 0
    
    overlap = len(title_words_filtered.intersection(summary_words_filtered))
    
    # Base similarity - more lenient calculation
    # Give higher weight to any overlap
    if overlap > 0:
        # Start with 50% base if there's any overlap
        similarity = 50.0
        
        # Add points for each matching word
        similarity += (overlap * 15)
        
        # Boost for word length (longer words are more significant)
        for word in title_words_filtered:
            if word in summary_words_filtered:
                if len(word) > 6:
                    similarity += 20  # Big boost for long words
                elif len(word) > 4:
                    similarity += 15  # Medium boost
                elif len(word) > 3:
                    similarity += 10  # Small boost
                else:
                    similarity += 5
    else:
        # No filtered overlap - check original words
        overlap_orig = len(title_words.intersection(summary_words))
        similarity = (overlap_orig / max(len(title_words), len(summary_words))) * 100
    
    # Check for matching multi-word phrases
    title_words_list = title_lower.split()
    summary_words_list = issue_summary.split()
    
    title_bigrams = set()
    summary_bigrams = set()
    
    for i in range(len(title_words_list) - 1):
        title_bigrams.add(f"{title_words_list[i]} {title_words_list[i+1]}")
    for i in range(len(summary_words_list) - 1):
        summary_bigrams.add(f"{summary_words_list[i]} {summary_words_list[i+1]}")
    
    # Big boost if phrases match
    phrase_matches = len(title_bigrams.intersection(summary_bigrams))
    if phrase_matches > 0:
        similarity += phrase_matches * 25
    
    return min(similarity, 100)

def create_bug_in_jira(title, description, steps_to_reproduce, expected_behavior, actual_behavior, environment, priority='Medium', attachments=None):
    """
    Create a new bug in Jira under the specified epic with optional attachments.
    """
    # Format description
    formatted_description = f"""h2. Issue Description
{description}

h2. Steps to Reproduce
{steps_to_reproduce}

h2. Expected Behavior
{expected_behavior}

h2. Actual Behavior
{actual_behavior}

h2. Environment
{environment}

---
_Created via AI Bug Reporter on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_
"""
    
    # Create issue payload
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "parent": {"key": EPIC_KEY},
            "summary": title,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": formatted_description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Bug"}
        }
    }
    
    # Map priority names to what Jira expects (may vary by Jira instance)
    priority_mapping = {
        'Critical': 'Urgent',  # Map Critical to Urgent if needed
        'High': 'High',
        'Medium': 'Normal',  # Map Medium to Normal if Jira uses that
        'Low': 'Low'
    }
    
    # Only add priority if it's provided and not None
    if priority and priority != 'None':
        # Use mapped priority or original if not in mapping
        jira_priority = priority_mapping.get(priority, priority)
        payload["fields"]["priority"] = {"name": jira_priority}
        print(f"[DEBUG] Setting priority to: {jira_priority}", flush=True)
    
    try:
        response = requests.post(
            f'{JIRA_API_BASE}/rest/api/3/issue',
            headers=get_jira_headers(),
            json=payload
        )
        
        if response.status_code in [200, 201]:
            issue = response.json()
            issue_key = issue['key']
            issue_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
            
            # Transition the issue to "On Hold" status
            try:
                # Get available transitions for the issue
                transitions_response = requests.get(
                    f'{JIRA_API_BASE}/rest/api/3/issue/{issue_key}/transitions',
                    headers=get_jira_headers()
                )
                
                if transitions_response.status_code == 200:
                    transitions = transitions_response.json().get('transitions', [])
                    
                    # Find the "On Hold" transition
                    on_hold_transition = None
                    for transition in transitions:
                        if transition['name'].lower() == 'on hold' or 'on hold' in transition['name'].lower():
                            on_hold_transition = transition
                            break
                    
                    if on_hold_transition:
                        # Execute the transition to On Hold
                        transition_response = requests.post(
                            f'{JIRA_API_BASE}/rest/api/3/issue/{issue_key}/transitions',
                            headers=get_jira_headers(),
                            json={
                                'transition': {
                                    'id': on_hold_transition['id']
                                }
                            }
                        )
                        
                        if transition_response.status_code in [200, 204]:
                            print(f"[DEBUG] Issue {issue_key} transitioned to On Hold", flush=True)
                        else:
                            print(f"[DEBUG] Failed to transition to On Hold: {transition_response.status_code}", flush=True)
                    else:
                        print(f"[DEBUG] 'On Hold' transition not available for {issue_key}", flush=True)
                else:
                    print(f"[DEBUG] Failed to get transitions: {transitions_response.status_code}", flush=True)
            except Exception as e:
                print(f"[DEBUG] Error transitioning to On Hold: {e}", flush=True)
            
            # Upload attachments if any
            if attachments:
                uploaded_count = 0
                for file in attachments:
                    if file and file.filename:
                        try:
                            # Jira requires multipart/form-data for attachments
                            attach_headers = {
                                'Authorization': get_jira_headers()['Authorization'],
                                'X-Atlassian-Token': 'no-check'
                            }
                            
                            files_data = {
                                'file': (file.filename, file.stream, file.content_type)
                            }
                            
                            attach_response = requests.post(
                                f'{JIRA_API_BASE}/rest/api/3/issue/{issue_key}/attachments',
                                headers=attach_headers,
                                files=files_data
                            )
                            
                            if attach_response.status_code in [200, 201]:
                                uploaded_count += 1
                                print(f"[DEBUG] Uploaded attachment: {file.filename}", flush=True)
                            else:
                                print(f"[DEBUG] Failed to upload {file.filename}: {attach_response.text}", flush=True)
                        except Exception as e:
                            print(f"[DEBUG] Error uploading {file.filename}: {e}", flush=True)
                
                print(f"[DEBUG] Uploaded {uploaded_count}/{len(attachments)} attachments", flush=True)
            
            return {
                'success': True,
                'key': issue_key,
                'url': issue_url
            }
        else:
            return {
                'success': False,
                'error': f"Failed to create issue: {response.status_code} - {response.text}"
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# API Routes
@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/epic-stats', methods=['GET'])
def get_epic_stats():
    """Get statistics for bugs under the epic."""
    import sys
    from collections import defaultdict
    from datetime import datetime, timedelta
    
    try:
        jql = f'parent = {EPIC_KEY} AND type = Bug ORDER BY created DESC'
        
        response = requests.get(
            f'{JIRA_API_BASE}/rest/api/3/search/jql',
            headers=get_jira_headers(),
            params={
                'jql': jql,
                'maxResults': 100,
                'fields': 'summary,status,priority,created,resolutiondate,labels,description'
            }
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch epic stats'}), 500
        
        issues = response.json().get('issues', [])
        
        # Initialize stats
        stats = {
            'total_count': len(issues),
            'by_status': defaultdict(int),
            'by_priority': defaultdict(int),
            'by_platform': defaultdict(int),
            'priority_status_matrix': defaultdict(lambda: defaultdict(int)),
            'creation_trend': defaultdict(int),
            'resolution_trend': defaultdict(int),
            'open_count': 0,
            'closed_count': 0,
            'avg_resolution_days': 0,
            'total_resolved_days': 0
        }
        
        for issue in issues:
            fields = issue['fields']
            
            # Status breakdown
            status = fields['status']['name']
            stats['by_status'][status] += 1
            
            # Count open vs closed
            status_category = fields['status']['statusCategory']['key']
            if status_category == 'done':
                stats['closed_count'] += 1
            else:
                stats['open_count'] += 1
            
            # Priority breakdown
            priority = fields.get('priority', {}).get('name', 'None')
            stats['by_priority'][priority] += 1
            
            # Priority x Status matrix
            stats['priority_status_matrix'][priority][status] += 1
            
            # Platform detection from title or labels
            summary = fields['summary'].lower()
            description = fields.get('description', '') or ''
            if isinstance(description, dict):
                description = ''
            else:
                description = description.lower()
            
            labels = fields.get('labels', [])
            labels_str = ' '.join(labels).lower()
            
            combined_text = f"{summary} {description} {labels_str}"
            
            platforms = []
            if 'ios' in combined_text:
                platforms.append('iOS')
            if 'android' in combined_text:
                platforms.append('Android')
            if any(word in combined_text for word in ['web', 'website', 'browser']):
                platforms.append('Web')
            
            if not platforms:
                platforms.append('Unknown')
            
            platform_key = ' + '.join(sorted(platforms))
            stats['by_platform'][platform_key] += 1
            
            # Creation trend (by day)
            created = datetime.fromisoformat(fields['created'].replace('Z', '+00:00'))
            day_key = created.strftime('%Y-%m-%d')
            stats['creation_trend'][day_key] += 1
            
            # Resolution trend
            if fields.get('resolutiondate'):
                resolved = datetime.fromisoformat(fields['resolutiondate'].replace('Z', '+00:00'))
                day_key = resolved.strftime('%Y-%m-%d')
                stats['resolution_trend'][day_key] += 1
                
                # Calculate resolution time
                resolution_days = (resolved - created).days
                if resolution_days >= 0:
                    stats['total_resolved_days'] += resolution_days
        
        # Calculate average resolution time
        if stats['closed_count'] > 0:
            stats['avg_resolution_days'] = round(stats['total_resolved_days'] / stats['closed_count'], 1)
        
        # Convert defaultdicts to regular dicts for JSON
        return jsonify({
            'total_count': stats['total_count'],
            'open_count': stats['open_count'],
            'closed_count': stats['closed_count'],
            'avg_resolution_days': stats['avg_resolution_days'],
            'by_status': dict(stats['by_status']),
            'by_priority': dict(stats['by_priority']),
            'by_platform': dict(stats['by_platform']),
            'priority_status_matrix': {k: dict(v) for k, v in stats['priority_status_matrix'].items()},
            'creation_trend': dict(stats['creation_trend']),
            'resolution_trend': dict(stats['resolution_trend'])
        })
        
    except Exception as e:
        print(f"[ERROR] Failed to get epic stats: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-duplicates', methods=['POST'])
def check_duplicates():
    """Check for duplicate bugs."""
    data = request.json
    title = data.get('title', '')
    description = data.get('description', '')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    duplicates = search_duplicates(title, description)
    
    # Categorize duplicates by similarity
    high_similarity = [d for d in duplicates if d['similarity'] >= 70]
    medium_similarity = [d for d in duplicates if 40 <= d['similarity'] < 70]
    
    return jsonify({
        'duplicates': duplicates,
        'has_duplicates': len(duplicates) > 0,
        'high_similarity_count': len(high_similarity),
        'medium_similarity_count': len(medium_similarity),
        'warning_message': get_duplicate_warning(duplicates)
    })

def get_duplicate_warning(duplicates):
    """Generate appropriate warning message based on duplicates found."""
    if not duplicates:
        return None
    
    highest_similarity = duplicates[0]['similarity']
    
    if highest_similarity >= 80:
        return "⚠️ Very similar bug found! Please review before creating a new ticket."
    elif highest_similarity >= 60:
        return "⚠️ Similar bugs found. Your issue might already be reported."
    elif highest_similarity >= 40:
        return "ℹ️ Possibly related bugs found. Consider reviewing them first."
    else:
        return None

@app.route('/api/create-bug', methods=['POST'])
def create_bug():
    """Create a new bug in Jira with optional attachments."""
    # Check if this is a multipart request (with files)
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form.to_dict()
        files = request.files.getlist('attachments')
    else:
        data = request.json
        files = []
    
    # Validate required fields
    required_fields = ['title', 'description', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    result = create_bug_in_jira(
        title=data['title'],
        description=data['description'],
        steps_to_reproduce=data['steps_to_reproduce'],
        expected_behavior=data['expected_behavior'],
        actual_behavior=data['actual_behavior'],
        environment=data.get('environment', 'Not specified'),
        priority=data.get('priority', 'Medium'),
        attachments=files
    )
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'epic': EPIC_KEY})

if __name__ == '__main__':
    # Check for required environment variables
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        print("Error: JIRA_EMAIL and JIRA_API_TOKEN environment variables are required")
        print("Please set them before running the app")
        exit(1)
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
