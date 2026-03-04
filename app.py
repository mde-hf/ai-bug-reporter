#!/usr/bin/env python3
"""
AI Bug Reporting Tool for HelloFresh
Checks for duplicate tickets before creating new ones in Jira.
AI-powered test case generation using Claude (via CLI or API).
Google Drive integration via OAuth2 for org-restricted documents.
"""

import os
import json
import sys
import re
import base64
import urllib.parse
import logging
import traceback
import subprocess
import shutil
from collections import defaultdict
from datetime import datetime, timedelta

from flask import Flask, render_template, request, jsonify, redirect, session
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import anthropic

# Load environment variables first
load_dotenv()

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Google Drive OAuth imports
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    logger.warning("Google Drive libraries not installed. Run: pip install -r requirements.txt")

# Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))
CORS(app)

# Google Drive OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:5000/google/callback')
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Google credentials storage
GOOGLE_TOKEN_FILE = os.path.join(os.path.dirname(__file__), '.google_token.json')

# Configuration Constants
JIRA_BASE_URL = os.environ.get('JIRA_BASE_URL', 'https://hellofresh.atlassian.net')
JIRA_CLOUD_ID = os.environ.get('JIRA_CLOUD_ID', 'c563471e-8682-4abc-8fa9-5465b05abad5')
JIRA_API_BASE = f'https://api.atlassian.com/ex/jira/{JIRA_CLOUD_ID}'
JIRA_EMAIL = os.environ.get('JIRA_EMAIL')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')
EPIC_KEY = os.environ.get('EPIC_KEY', 'REW-323')
PROJECT_KEY = os.environ.get('PROJECT_KEY', 'REW')

# Slack Configuration
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

# Anthropic Configuration (like Agento)
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
ANTHROPIC_MODEL = os.environ.get('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')

# Claude CLI detection (like Agento - uses company AWS)
CLAUDE_CLI_PATH = shutil.which('claude')
USE_CLAUDE_CLI = CLAUDE_CLI_PATH is not None

# Application Constants
MAX_DUPLICATES_TO_RETURN = 8
SIMILARITY_THRESHOLD_MIN = 30
SUBSTRING_MATCH_SCORE = 95
HIGH_SIMILARITY_THRESHOLD = 80
MEDIUM_SIMILARITY_THRESHOLD = 60
LOW_SIMILARITY_THRESHOLD = 40

# Initialize Anthropic client (backup option)
anthropic_client = None
if ANTHROPIC_API_KEY:
    try:
        anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        logger.info(f"Anthropic client initialized with model: {ANTHROPIC_MODEL}")
    except Exception as e:
        logger.warning(f"Failed to initialize Anthropic client: {e}")
        anthropic_client = None
else:
    logger.info("ANTHROPIC_API_KEY not set")

# Log AI configuration (like Agento)
if USE_CLAUDE_CLI:
    logger.info(f"✅ Claude CLI detected at: {CLAUDE_CLI_PATH} (using company AWS)")
elif anthropic_client:
    logger.info(f"✅ Anthropic API available (personal account)")
else:
    logger.info("ℹ️  AI features will use fallback mode")

# Initialize Multi-Agent System
agent_manager = None
try:
    from agents import AgentManager
    # Pass both CLI path and API client
    agent_manager = AgentManager(
        anthropic_client=anthropic_client, 
        model_id=ANTHROPIC_MODEL,
        claude_cli_path=CLAUDE_CLI_PATH
    )
    logger.info("Multi-Agent AI System initialized successfully")
except Exception as e:
    logger.warning(f"Failed to initialize Multi-Agent System: {e}")
    agent_manager = None

def call_claude_cli(prompt, model='sonnet'):
    """
    Call Claude via CLI (like Agento does).
    Uses company's AWS Bedrock authentication.
    
    Args:
        prompt: The prompt to send to Claude
        model: Model name (sonnet, opus, haiku)
        
    Returns:
        Claude's response text or None if failed
    """
    if not CLAUDE_CLI_PATH:
        return None
    
    try:
        logger.info(f"Calling Claude CLI with model: {model}")
        
        # Claude CLI syntax: claude --print --model sonnet "prompt"
        result = subprocess.run(
            [CLAUDE_CLI_PATH, '--print', '--model', model, prompt],
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
            check=True
        )
        
        logger.info("Claude CLI completed successfully")
        return result.stdout.strip()
        
    except subprocess.TimeoutExpired:
        logger.error("Claude CLI timeout after 120s")
        return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Claude CLI error: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Claude CLI unexpected error: {e}")
        return None

def call_ai(prompt, system_prompt=None):
    """
    Call AI with fallback priority (like Agento):
    1. Claude CLI (company AWS)
    2. Anthropic API (personal)
    3. None (caller handles fallback)
    
    Args:
        prompt: User prompt
        system_prompt: Optional system prompt (only used with API)
        
    Returns:
        AI response text or None
    """
    # Priority 1: Claude CLI (company AWS)
    if USE_CLAUDE_CLI:
        logger.debug("Trying Claude CLI (company AWS)...")
        result = call_claude_cli(prompt)
        if result:
            return result
        logger.warning("Claude CLI failed, trying Anthropic API...")
    
    # Priority 2: Anthropic API (personal)
    if anthropic_client:
        logger.debug("Trying Anthropic API...")
        try:
            message = anthropic_client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=4096,
                system=system_prompt if system_prompt else "You are a helpful AI assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            if message.content:
                return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
    
    # Priority 3: None (caller must handle fallback)
    return None

def get_jira_headers():
    """Get headers for Jira API requests."""
    return {
        'Authorization': f'Basic {get_basic_auth()}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

def get_basic_auth():
    """Get base64 encoded basic auth string."""
    credentials = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    return base64.b64encode(credentials.encode()).decode()

def search_duplicates(title, description):
    """
    Search for potential duplicate bugs in Jira.
    Returns list of similar issues with emphasis on title matching.
    """
    logger.debug("===== SEARCHING FOR DUPLICATES =====")
    logger.debug(f"Title: '{title}'")
    logger.debug(f"Description: '{description}'")
    
    # Simple direct search - search for individual words to catch partial matches
    title_words = [w.strip() for w in title.split() if len(w.strip()) > 2]
    
    if not title_words:
        # If title is too short or only has short words, search as-is
        simple_jql = f'project = {PROJECT_KEY} AND type = Bug AND summary ~ "{title}" ORDER BY created DESC'
    else:
        # Build JQL to search for any of the meaningful words in the title
        word_queries = ' OR '.join([f'summary ~ "{word}"' for word in title_words])
        simple_jql = f'project = {PROJECT_KEY} AND type = Bug AND ({word_queries}) ORDER BY created DESC'
    
    logger.debug(f"JQL Query: {simple_jql}")
    sys.stdout.flush()
    
    all_results = []
    
    try:
        # Use Atlassian Cloud API with proper /search/jql endpoint
        search_url = f'{JIRA_API_BASE}/rest/api/3/search/jql'
        
        logger.debug(f"API URL: {search_url}")
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
        
        logger.debug(f"Response status: {response.status_code}")
        sys.stdout.flush()
        
        if response.status_code == 200:
            result_data = response.json()
            issues = result_data.get('issues', [])
            logger.debug(f"Found {len(issues)} total issues")
            sys.stdout.flush()
            
            for issue in issues:
                key = issue['key']
                summary = issue['fields']['summary']
                parent = issue['fields'].get('parent', {})
                parent_key = parent.get('key', 'No parent') if parent else 'No parent'
                
                logger.debug(f"Issue {key}: '{summary}' (Parent: {parent_key})")
                
                similarity = calculate_similarity(title, description, issue)
                logger.debug(f"Similarity: {similarity}%")
                
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
            logger.debug(f"Error response ({response.status_code}): {error_text}")
            sys.stdout.flush()
            
    except Exception as e:
        logger.error(f"Exception during search: {e}")
        traceback.print_exc()
    
    # Sort by similarity score
    all_results.sort(key=lambda x: x['similarity'], reverse=True)
    
    logger.debug(f"Returning {len(all_results)} results")
    logger.debug("===== END SEARCH =====")
    sys.stdout.flush()
    
    return all_results[:8]

def extract_key_terms(title, description):
    """
    Extract meaningful keywords from title and description for search.
    
    Filters out common stop words and returns up to 100 chars of keywords
    from both title and description for use in JQL queries.
    
    Args:
        title: Bug title string
        description: Bug description string
        
    Returns:
        dict: Contains 'title_keywords' and 'description_keywords' strings
    """
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
    Calculate similarity score between input bug and existing Jira issue.
    
    Uses multiple strategies:
    - Substring matching (95% if title is contained in summary)
    - Word overlap with length-based weighting (longer words = higher score)
    - Bigram/phrase matching for multi-word sequences
    
    Args:
        title: Input bug title
        description: Input bug description  
        issue: Existing Jira issue dict with 'fields'
        
    Returns:
        int: Similarity score 0-100, where 70+ indicates high similarity
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
    Uses Atlassian Document Format (ADF) for proper rendering.
    """
    
    # Build ADF description with proper structure
    adf_content = [
        # Issue Description heading
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": "Issue Description"}]
        },
        {
            "type": "paragraph",
            "content": [{"type": "text", "text": description}]
        },
        # Steps to Reproduce heading
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": "Steps to Reproduce"}]
        },
        {
            "type": "paragraph",
            "content": [{"type": "text", "text": steps_to_reproduce}]
        },
        # Expected Behavior heading
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": "Expected Behavior"}]
        },
        {
            "type": "paragraph",
            "content": [{"type": "text", "text": expected_behavior}]
        },
        # Actual Behavior heading
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": "Actual Behavior"}]
        },
        {
            "type": "paragraph",
            "content": [{"type": "text", "text": actual_behavior}]
        },
        # Environment heading
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": "Environment"}]
        },
        {
            "type": "paragraph",
            "content": [{"type": "text", "text": environment}]
        },
        # Divider
        {
            "type": "rule"
        },
        # Footer
        {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "text": f"Created via AI Bug Reporter on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "marks": [{"type": "em"}]
                }
            ]
        }
    ]
    
    # Create issue payload
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "parent": {"key": EPIC_KEY},
            "summary": title,
            "description": {
                "type": "doc",
                "version": 1,
                "content": adf_content
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
        logger.debug(f"Setting priority to: {jira_priority}")
    
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
                            logger.debug(f"Issue {issue_key} transitioned to On Hold")
                        else:
                            logger.debug(f"Failed to transition to On Hold: {transition_response.status_code}")
                    else:
                        logger.debug(f"'On Hold' transition not available for {issue_key}")
                else:
                    logger.debug(f"Failed to get transitions: {transitions_response.status_code}")
            except Exception as e:
                logger.debug(f"Error transitioning to On Hold: {e}")
            
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
                                logger.debug(f"Uploaded attachment: {file.filename}")
                            else:
                                logger.debug(f"Failed to upload {file.filename}: {attach_response.text}")
                        except Exception as e:
                            logger.debug(f"Error uploading {file.filename}: {e}")
                    
                logger.debug(f"Uploaded {uploaded_count}/{len(attachments)} attachments")
            
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
        
        # Convert creation_trend from dict to array sorted by date
        creation_trend_array = [
            {'date': date, 'count': count}
            for date, count in sorted(stats['creation_trend'].items())
        ]
        
        # Convert defaultdicts to regular dicts for JSON
        return jsonify({
            'total_count': stats['total_count'],
            'open_count': stats['open_count'],
            'resolved_count': stats['closed_count'],  # Frontend expects 'resolved_count'
            'closed_count': stats['closed_count'],
            'avg_resolution_days': stats['avg_resolution_days'],
            'by_status': dict(stats['by_status']),
            'by_priority': dict(stats['by_priority']),
            'by_platform': dict(stats['by_platform']),
            'priority_matrix': {k: dict(v) for k, v in stats['priority_status_matrix'].items()},  # Frontend expects 'priority_matrix'
            'creation_trend': creation_trend_array,  # Array format for frontend
            'resolution_trend': dict(stats['resolution_trend'])
        })
        
    except Exception as e:
        logger.error(f"Failed to get epic stats: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-duplicates', methods=['POST'])
def check_duplicates():
    """
    Check for duplicate bugs with AI-powered semantic analysis.
    Falls back to rule-based matching if AI unavailable.
    """
    data = request.json
    title = data.get('title', '')
    description = data.get('description', '')
    steps = data.get('steps_to_reproduce', '')
    environment = data.get('environment', '')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    # Step 1: Get candidate duplicates using rule-based search
    logger.info(f"Checking duplicates for: '{title}'")
    candidates = search_duplicates(title, description)
    
    if not candidates:
        return jsonify({
            'duplicates': [],
            'has_duplicates': False,
            'ai_enhanced': False,
            'method': 'rule-based',
            'warning_message': None
        })
    
    # Step 2: Try AI semantic analysis if available
    if agent_manager and USE_CLAUDE_CLI:
        try:
            logger.info("Using AI semantic duplicate detection...")
            
            # Prepare bug data for AI analysis
            bug_data = {
                'title': title,
                'description': description,
                'steps': steps,
                'environment': environment
            }
            
            # Prepare candidates for AI (limit to top 5 for performance)
            ai_candidates = []
            for candidate in candidates[:5]:
                ai_candidates.append({
                    'key': candidate['key'],
                    'title': candidate['title'],
                    'description': candidate['description'][:500],  # Limit length
                    'status': candidate['status']
                })
            
            # Get AI analysis
            agent = agent_manager.get_agent('duplicate_detective')
            if agent:
                ai_result = agent.find_semantic_duplicates(bug_data, ai_candidates)
                
                if ai_result.get('success'):
                    # Parse AI response to update similarity scores
                    ai_response = ai_result.get('response', '')
                    
                    # Try to extract JSON from AI response
                    import re
                    json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
                    if json_match:
                        try:
                            ai_scores = json.loads(json_match.group(1))
                            
                            # Update candidates with AI scores
                            for candidate in candidates[:5]:
                                for ai_score in ai_scores:
                                    if ai_score.get('candidate_key') == candidate['key']:
                                        # Use AI score if higher than rule-based
                                        ai_similarity = ai_score.get('similarity_score', candidate['similarity'])
                                        candidate['similarity'] = max(candidate['similarity'], ai_similarity)
                                        candidate['ai_reasoning'] = ai_score.get('reasoning', '')
                                        candidate['ai_enhanced'] = True
                            
                            # Re-sort by updated scores
                            candidates.sort(key=lambda x: x['similarity'], reverse=True)
                            
                            logger.info(f"AI enhanced {len(ai_scores)} candidates")
                        except json.JSONDecodeError:
                            logger.warning("Could not parse AI response as JSON")
                    
                    # Mark as AI-enhanced
                    for candidate in candidates[:5]:
                        if 'ai_enhanced' not in candidate:
                            candidate['ai_enhanced'] = False
                    
                    method = 'ai-semantic'
                else:
                    logger.warning("AI analysis failed, using rule-based scores")
                    method = 'rule-based-fallback'
            else:
                logger.warning("Duplicate Detective agent not available")
                method = 'rule-based'
        except Exception as e:
            logger.error(f"Error in AI duplicate detection: {e}")
            method = 'rule-based-fallback'
    else:
        method = 'rule-based'
        if not agent_manager:
            logger.debug("Agent manager not initialized")
        if not USE_CLAUDE_CLI:
            logger.debug("Claude CLI not available")
    
    # Categorize duplicates by similarity
    high_similarity = [d for d in candidates if d['similarity'] >= 70]
    medium_similarity = [d for d in candidates if 40 <= d['similarity'] < 70]
    
    return jsonify({
        'duplicates': candidates,
        'has_duplicates': len(candidates) > 0,
        'high_similarity_count': len(high_similarity),
        'medium_similarity_count': len(medium_similarity),
        'ai_enhanced': method.startswith('ai'),
        'method': method,
        'warning_message': get_duplicate_warning(candidates)
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

# ═══════════════════════════════════════════════════════════════
# GOOGLE DRIVE OAUTH & AUTHENTICATION
# ═══════════════════════════════════════════════════════════════

def get_google_credentials():
    """Load Google OAuth credentials from token file."""
    if not os.path.exists(GOOGLE_TOKEN_FILE):
        return None
    
    try:
        with open(GOOGLE_TOKEN_FILE, 'r') as f:
            token_data = json.load(f)
        
        creds = Credentials.from_authorized_user_info(token_data, GOOGLE_SCOPES)
        
        # Check if credentials are valid
        if creds and creds.valid:
            return creds
        
        # Try to refresh if expired
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
            save_google_credentials(creds)
            return creds
            
        return None
    except Exception as e:
        logger.error(f"Error loading Google credentials: {e}")
        return None

def save_google_credentials(creds):
    """Save Google OAuth credentials to token file."""
    try:
        token_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        with open(GOOGLE_TOKEN_FILE, 'w') as f:
            json.dump(token_data, f)
        logger.info("Google credentials saved successfully")
    except Exception as e:
        logger.error(f"Error saving Google credentials: {e}")

@app.route('/google/auth')
def google_auth():
    """Initiate Google OAuth flow."""
    if not GOOGLE_DRIVE_AVAILABLE:
        return jsonify({
            'error': 'Google Drive integration not available. Install dependencies: pip install -r requirements.txt'
        }), 500
    
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return jsonify({
            'error': 'Google OAuth not configured. See GOOGLE_DRIVE_SETUP.md for instructions.'
        }), 500
    
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [GOOGLE_REDIRECT_URI]
                }
            },
            scopes=GOOGLE_SCOPES
        )
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        session['state'] = state
        return redirect(authorization_url)
    except Exception as e:
        logger.error(f"Error initiating Google OAuth: {e}")
        return jsonify({'error': f'Failed to start Google authentication: {str(e)}'}), 500

@app.route('/google/callback')
def google_callback():
    """Handle Google OAuth callback."""
    if not GOOGLE_DRIVE_AVAILABLE:
        return "Google Drive integration not available", 500
    
    try:
        state = session.get('state')
        
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [GOOGLE_REDIRECT_URI]
                }
            },
            scopes=GOOGLE_SCOPES,
            state=state
        )
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        
        # Get authorization code from callback
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)
        
        # Save credentials
        creds = flow.credentials
        save_google_credentials(creds)
        
        return """
        <html>
            <body>
                <h2>✅ Google Drive Connected!</h2>
                <p>You can now access org-restricted Google Docs.</p>
                <p><a href="/">Go back to Bug Reporter</a></p>
            </body>
        </html>
        """
    except Exception as e:
        logger.error(f"Error in Google OAuth callback: {e}")
        return f"<h2>❌ Authentication Failed</h2><p>{str(e)}</p><p><a href='/google/auth'>Try again</a></p>", 500

def fetch_google_doc_authenticated(doc_id):
    """
    Fetch Google Doc content using authenticated API.
    Works with org-restricted documents.
    """
    creds = get_google_credentials()
    
    if not creds:
        return None, "Not authenticated. Visit /google/auth to connect your Google account."
    
    try:
        service = build('drive', 'v3', credentials=creds)
        
        # Export as plain text
        request_obj = service.files().export(fileId=doc_id, mimeType='text/plain')
        content = request_obj.execute().decode('utf-8')
        
        # Get document metadata
        metadata = service.files().get(fileId=doc_id, fields='name').execute()
        title = metadata.get('name', 'Untitled Document')
        
        return {'content': content, 'title': title}, None
        
    except HttpError as e:
        if e.resp.status == 404:
            return None, "Document not found. Check the link and your access permissions."
        elif e.resp.status == 403:
            return None, "Access denied. You may not have permission to view this document."
        else:
            return None, f"Google Drive API error: {e.resp.status} - {str(e)}"
    except Exception as e:
        return None, f"Error fetching document: {str(e)}"

@app.route('/api/generate-test-cases', methods=['POST'])
def generate_test_cases():
    """
    Generate test cases from JIRA ticket or Google Drive link.
    Supports:
    - JIRA ticket URL (e.g., https://company.atlassian.net/browse/KEY-123)
    - JIRA ticket key (e.g., KEY-123)
    - Google Drive/Docs URL (for acceptance criteria documents)
    """
    try:
        data = request.get_json()
        source_input = data.get('ticket')
        
        if not source_input:
            return jsonify({'error': 'JIRA ticket or Google Drive link is required'}), 400
        
        source_input = source_input.strip()
        
        # Check if it's a Google Drive link
        if 'drive.google.com' in source_input or 'docs.google.com' in source_input:
            return handle_google_drive_test_cases(source_input)
        
        # Otherwise, treat as JIRA ticket
        return handle_jira_test_cases(source_input)
        
    except Exception as e:
        logger.error(f"Test case generation failed: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def handle_jira_test_cases(ticket_input):
    """Handle test case generation from JIRA ticket."""
    # Extract ticket key from URL or use as-is
    ticket_key = ticket_input
    if 'atlassian.net/browse/' in ticket_key:
        ticket_key = ticket_key.split('/browse/')[-1].split('?')[0]
    
    # Fetch ticket from JIRA
    logger.info(f"Fetching JIRA ticket: {ticket_key}")
    
    response = requests.get(
        f'{JIRA_API_BASE}/rest/api/3/issue/{ticket_key}',
        headers=get_jira_headers()
    )
    
    if not response.ok:
        return jsonify({'error': f'Failed to fetch ticket: {response.status_code}'}), 400
    
    issue = response.json()
    
    # Extract ticket information
    summary = issue['fields']['summary']
    description = issue['fields'].get('description', {})
    issue_type = issue['fields']['issuetype']['name']
    status = issue['fields']['status']['name']
    priority = issue['fields'].get('priority', {}).get('name', 'None')
    
    # Extract description text
    desc_text = extract_description_text(description)
    
    # Parse ticket content for structured information
    parsed_content = parse_ticket_content(desc_text)
    
    # Generate test cases using AI (with fallback to rule-based)
    test_cases = generate_critical_path_tests_with_ai(ticket_key, summary, desc_text, issue_type, parsed_content)
    
    return jsonify({
        'success': True,
        'source_type': 'jira',
        'ticket_key': ticket_key,
        'ticket_url': f'{JIRA_BASE_URL}/browse/{ticket_key}',
        'summary': summary,
        'description': desc_text,
        'issue_type': issue_type,
        'status': status,
        'priority': priority,
        'test_cases': test_cases
    })

def handle_google_drive_test_cases(drive_url):
    """
    Handle test case generation from Google Drive link.
    Uses OAuth for org-restricted documents, falls back to public access.
    """
    logger.info(f"Processing Google Drive link: {drive_url}")
    
    # Extract document ID from various Google Drive URL formats
    doc_id = None
    if '/d/' in drive_url:
        doc_id = drive_url.split('/d/')[-1].split('/')[0]
    elif 'id=' in drive_url:
        doc_id = drive_url.split('id=')[-1].split('&')[0]
    
    if not doc_id:
        return jsonify({'error': 'Could not extract document ID from Google Drive URL'}), 400
    
    # Try authenticated access first (for org-restricted docs)
    if GOOGLE_DRIVE_AVAILABLE:
        result, error = fetch_google_doc_authenticated(doc_id)
        if result:
            content = result['content']
            title = result['title']
            
            lines = content.split('\n')
            description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else content
            
            # Parse content for structured information
            parsed_content = parse_ticket_content(description)
            
            # Generate test cases using AI (with fallback)
            test_cases = generate_critical_path_tests_with_ai(
                f"GDOC-{doc_id[:8]}", 
                title, 
                description, 
                "Documentation",
                parsed_content
            )
            
            return jsonify({
                'success': True,
                'source_type': 'google_drive',
                'auth_method': 'oauth',
                'document_id': doc_id,
                'document_url': drive_url,
                'summary': title,
                'description': description[:500] + ('...' if len(description) > 500 else ''),
                'issue_type': 'Documentation',
                'status': 'N/A',
                'priority': 'N/A',
                'test_cases': test_cases
            })
        elif "Not authenticated" in error:
            # Need to authenticate
            return jsonify({
                'error': 'Google Drive authentication required for org-restricted documents.\n\n'
                        'Steps:\n'
                        '1. Visit http://localhost:5000/google/auth\n'
                        '2. Sign in with your HelloFresh Google account\n'
                        '3. Grant permissions\n'
                        '4. Try again\n\n'
                        'Or make the document "Anyone with the link"',
                'auth_url': '/google/auth'
            }), 401
    
    # Fallback: Try public access (works if document is "Anyone with the link")
    try:
        export_url = f'https://docs.google.com/document/d/{doc_id}/export?format=txt'
        response = requests.get(export_url, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            lines = content.split('\n')
            title = lines[0].strip() if lines else "Google Drive Document"
            description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else content
            
            parsed_content = parse_ticket_content(description)
            
            test_cases = generate_critical_path_tests_with_ai(
                f"GDOC-{doc_id[:8]}", 
                title, 
                description, 
                "Documentation",
                parsed_content
            )
            
            return jsonify({
                'success': True,
                'source_type': 'google_drive',
                'auth_method': 'public',
                'document_id': doc_id,
                'document_url': drive_url,
                'summary': title,
                'description': description[:500] + ('...' if len(description) > 500 else ''),
                'issue_type': 'Documentation',
                'status': 'N/A',
                'priority': 'N/A',
                'test_cases': test_cases
            })
        else:
            # Document not accessible
            return jsonify({
                'error': 'Could not access Google Drive document.\n\n'
                        'Options:\n'
                        '1. Authenticate with Google: Visit /google/auth\n'
                        '2. Or change sharing to "Anyone with the link"\n\n'
                        f'Status code: {response.status_code}',
                'auth_url': '/google/auth'
            }), 401
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': f'Failed to fetch Google Drive document: {str(e)}\n\n'
                    'Try authenticating: Visit /google/auth',
            'auth_url': '/google/auth'
        }), 500

def extract_description_text(description):
    """
    Extract plain text from JIRA description object (ADF format).
    Preserves structure with section headings for better AI analysis.
    """
    if not description:
        return "No description provided"
    
    if isinstance(description, str):
        return description
    
    # Handle Atlassian Document Format (ADF)
    text_parts = []
    current_heading = None
    
    def extract_text(node):
        nonlocal current_heading
        
        if isinstance(node, dict):
            node_type = node.get('type')
            
            # Handle headings
            if node_type == 'heading':
                heading_text = ''
                if 'content' in node:
                    for child in node['content']:
                        if isinstance(child, dict) and child.get('type') == 'text':
                            heading_text = child.get('text', '')
                current_heading = heading_text
                text_parts.append(f"\n## {heading_text}\n")
            
            # Handle text nodes
            elif node_type == 'text':
                text_parts.append(node.get('text', ''))
            
            # Handle paragraphs
            elif node_type == 'paragraph':
                if 'content' in node:
                    for child in node['content']:
                        extract_text(child)
                    text_parts.append('\n')
            
            # Handle rules (horizontal lines)
            elif node_type == 'rule':
                text_parts.append('\n---\n')
            
            # Recursively process content
            elif 'content' in node:
                for child in node['content']:
                    extract_text(child)
                    
        elif isinstance(node, list):
            for item in node:
                extract_text(item)
    
    extract_text(description)
    
    # Clean up the text
    result = ''.join(text_parts).strip()
    return result if result else "No description provided"

def parse_ticket_content(description):
    """
    Parse ticket description to extract:
    - Acceptance Criteria
    - User Stories  
    - Business Rules
    - Google Drive links
    
    Optimized to recognize explicit Acceptance Criteria sections.
    """
    desc_lower = description.lower()
    
    result = {
        'acceptance_criteria': [],
        'user_stories': [],
        'business_rules': [],
        'google_drive_links': [],
        'raw_description': description
    }
    
    # Split description into lines for parsing
    lines = description.split('\n')
    
    # Track what section we're in
    in_acceptance_criteria_section = False
    in_user_story_section = False
    in_business_rules_section = False
    current_section = None
    section_content = []
    
    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()
        
        # Skip empty lines and separators
        if not line_stripped or line_stripped in ['---', '___']:
            continue
        
        # Check for Acceptance Criteria header
        if any(keyword in line_lower for keyword in [
            'acceptance criteria', 
            'acceptance criterion',
            'acceptance criteria:',
            '## acceptance criteria',
            'ac:',
            'a.c.'
        ]):
            in_acceptance_criteria_section = True
            in_user_story_section = False
            in_business_rules_section = False
            current_section = 'acceptance_criteria'
            continue
        
        # Check for User Story header
        if any(keyword in line_lower for keyword in [
            'user story',
            'user stories',
            '## user story',
            'user stories:'
        ]):
            in_user_story_section = True
            in_acceptance_criteria_section = False
            in_business_rules_section = False
            current_section = 'user_story'
            continue
        
        # Check for Business Rules header
        if any(keyword in line_lower for keyword in [
            'business rule',
            'business rules',
            '## business rule',
            'rules:'
        ]):
            in_business_rules_section = True
            in_acceptance_criteria_section = False
            in_user_story_section = False
            current_section = 'business_rules'
            continue
        
        # Check if we're entering a new section (any ## heading that's not AC/US/BR)
        if line_stripped.startswith('##'):
            # End current section
            in_acceptance_criteria_section = False
            in_user_story_section = False
            in_business_rules_section = False
            
            # Track the section type
            if 'step' in line_lower and 'reproduce' in line_lower:
                current_section = 'steps_to_reproduce'
            elif 'expected' in line_lower and 'behavior' in line_lower:
                current_section = 'expected_behavior'
            elif 'actual' in line_lower and 'behavior' in line_lower:
                current_section = 'actual_behavior'
            elif 'environment' in line_lower:
                current_section = 'environment'
            else:
                current_section = 'other'
            
            section_content = []
            continue
        
        # Extract content based on current section
        if in_acceptance_criteria_section:
            # In AC section - capture criteria
            clean_line = line_stripped.lstrip('*-•0123456789.) ').strip()
            if clean_line and len(clean_line) > 5:
                result['acceptance_criteria'].append(clean_line)
        
        elif in_user_story_section:
            # In user story section
            if 'as a' in line_lower or 'as an' in line_lower:
                result['user_stories'].append(line_stripped)
            elif line_stripped:
                # Might be continuation of user story
                if result['user_stories']:
                    result['user_stories'][-1] += ' ' + line_stripped
        
        elif in_business_rules_section:
            # In business rules section
            clean_line = line_stripped.lstrip('*-•0123456789.) ').strip()
            if clean_line and len(clean_line) > 5:
                result['business_rules'].append(clean_line)
        
        else:
            # Not in a specific section - check for patterns
            
            # Check for user story pattern anywhere
            if 'as a' in line_lower or 'as an' in line_lower:
                result['user_stories'].append(line_stripped)
            
            # Check for bullet points in Steps/Expected/Actual sections
            if current_section in ['steps_to_reproduce', 'expected_behavior']:
                if line_stripped and (line_stripped.startswith('*') or 
                                     line_stripped.startswith('-') or 
                                     line_stripped.startswith('•') or
                                     (len(line_stripped) > 2 and line_stripped[0].isdigit() and line_stripped[1] in '.)')):
                    clean_line = line_stripped.lstrip('*-•0123456789.) ').strip()
                    if clean_line and len(clean_line) > 10:
                        # Add as acceptance criteria if not already added
                        result['acceptance_criteria'].append(clean_line)
                elif line_stripped:
                    # Regular content in these sections
                    section_content.append(line_stripped)
        
        # Check for Google Drive links anywhere
        if 'drive.google.com' in line or 'docs.google.com' in line:
            urls = re.findall(r'https?://(?:drive|docs)\.google\.com[^\s]+', line)
            result['google_drive_links'].extend(urls)
    
    return result

def generate_critical_path_tests_with_ai(ticket_key, summary, description, issue_type, parsed_content):
    """
    Generate test cases using AI (Claude CLI or API).
    Falls back to rule-based generation if AI is unavailable.
    """
    try:
        # Build the AI prompt
        prompt = build_test_case_prompt(ticket_key, summary, description, issue_type, parsed_content)
        
        # Call Claude via Anthropic API
        logger.info("Calling Claude AI for test case generation...")
        
        # Try AI (CLI > API > fallback)
        ai_response = call_ai(
            prompt=prompt,
            system_prompt="You are an expert QA engineer specializing in test case design. Generate precise, actionable test cases in Gherkin format."
        )
        
        # Extract test cases from response
        if ai_response:
            logger.info("Successfully generated AI test cases")
            return ai_response
        else:
            logger.warning("AI unavailable, using fallback generation")
            return generate_critical_path_tests_fallback(ticket_key, summary, description, issue_type, parsed_content)
        
    except Exception as e:
        logger.error(f"AI error: {e}")
        return generate_critical_path_tests_fallback(ticket_key, summary, description, issue_type, parsed_content)

def build_test_case_prompt(ticket_key, summary, description, issue_type, parsed_content):
    """
    Build an intelligent prompt for Claude AI to generate test cases.
    Uses the structured description text extracted from JIRA.
    """
    has_ac = len(parsed_content['acceptance_criteria']) > 0
    has_user_stories = len(parsed_content['user_stories']) > 0
    has_business_rules = len(parsed_content['business_rules']) > 0
    has_google_drive = len(parsed_content['google_drive_links']) > 0
    
    prompt = f"""You are an expert QA engineer at HelloFresh. Generate comprehensive test cases in Cucumber/Gherkin format based on the JIRA ticket details below.

# Ticket Information

**Ticket ID:** {ticket_key}
**Type:** {issue_type}
**Summary:** {summary}

# Full Ticket Description

{description}

"""
    
    # Only add parsed sections if they provide additional info beyond the description
    if has_ac:
        prompt += f"\n# 🎯 IMPORTANT: Acceptance Criteria (Must Test)\n\n"
        prompt += f"The ticket explicitly defines {len(parsed_content['acceptance_criteria'])} acceptance criteria.\n"
        prompt += f"**YOU MUST create dedicated test scenarios for EACH criterion below:**\n\n"
        for idx, ac in enumerate(parsed_content['acceptance_criteria'][:10], 1):
            prompt += f"{idx}. {ac}\n"
        prompt += f"\nTag these scenarios with @acceptance_criteria @AC{idx} @priority_critical\n"
    
    if has_user_stories:
        prompt += f"\n# User Stories Identified\n\n"
        for idx, story in enumerate(parsed_content['user_stories'][:5], 1):
            prompt += f"{idx}. {story}\n"
    
    if has_business_rules:
        prompt += f"\n# Business Rules Identified\n\n"
        for idx, rule in enumerate(parsed_content['business_rules'][:5], 1):
            prompt += f"{idx}. {rule}\n"
    
    if has_google_drive:
        prompt += f"\n# Referenced Documents\n\n"
        for link in parsed_content['google_drive_links']:
            prompt += f"- {link}\n"
    
    prompt += """

# Your Task

Generate production-ready test cases in Cucumber/Gherkin format based ONLY on the specific requirements in this ticket. 

**CRITICAL RULES:**
- DO NOT generate generic placeholder tests
- Every scenario must be directly related to the ticket content
- Be specific to the actual feature/bug described
- Use real values and contexts from the ticket

Analyze the ticket description carefully:
- **Issue Description**: What specific problem/feature is this?
- **Acceptance Criteria** (if present): Test EXACTLY what each criterion states
- **Steps to Reproduce**: Use the actual steps from the ticket
- **Expected vs Actual Behavior**: Test the specific behaviors mentioned
- **Environment**: Consider the actual platform mentioned

# Test Case Requirements

1. **Feature description** 
   - Describe the SPECIFIC feature/bug from this ticket
   - Reference the ticket ID and summary

2. **Background** (only if needed)
   - Include ONLY if there are common preconditions mentioned in the ticket
   - Be specific to this feature/bug

3. **PRIORITY: Acceptance Criteria Tests (if provided)**
   - Create ONE detailed scenario for EACH acceptance criterion
   - Use the EXACT wording from the criterion
   - Tag: @acceptance_criteria @AC1, @AC2, etc. @priority_critical
   - Steps must directly test what the criterion states
   - NO generic placeholders

4. **Additional relevant scenarios** (only if they relate to the ticket):
   - **Happy Path** (@happy_path @smoke) - The ideal flow for THIS specific feature
   - **Steps to Reproduce** (@bug_reproduction) - For bugs, reproduce the exact issue
   - **Specific Edge Cases** (@edge_case) - ONLY edge cases relevant to THIS feature
   - **Relevant Error Handling** (@sad_path) - ONLY errors specific to THIS feature

5. **What NOT to include:**
   - ❌ Generic "Scenario Outline: Verify handling of edge cases" with placeholder data
   - ❌ Tests for "empty values", "special characters" unless the ticket mentions them
   - ❌ Regression tests unless the ticket specifically requires them
   - ❌ Platform-specific tests unless the ticket mentions specific platforms
   - ❌ Any test that doesn't directly relate to the ticket requirements

6. **Gherkin Quality:**
   - Clear Given/When/Then with SPECIFIC steps from the ticket context
   - Real values, not placeholders like "<edge_case_data>"
   - Scenario names that describe WHAT is being tested in this specific case
   - Only use Scenario Outline if the ticket suggests multiple similar test cases

7. **Be specific and contextual:**
   - Reference actual features mentioned (e.g., "login page", "welcome screen")
   - Use real user actions from the ticket
   - Test actual expected outcomes described
   - Include only details relevant to this ticket

# Output Format

Generate ONLY the Gherkin feature file content for THIS SPECIFIC ticket. 
No generic tests. No placeholder scenarios. Only what this ticket requires.
Do not include any explanatory text before or after the Gherkin."""
    
    return prompt

def generate_critical_path_tests_fallback(ticket_key, summary, description, issue_type, parsed_content):
    """
    Fallback rule-based test case generation.
    Used when AI is unavailable. Generates focused tests only on found criteria.
    """
    
    has_ac = len(parsed_content['acceptance_criteria']) > 0
    has_user_stories = len(parsed_content['user_stories']) > 0
    
    # Extract key words for feature name
    feature_name = summary[:80] if len(summary) <= 80 else summary[:77] + "..."
    
    gherkin_output = f"""# NOTE: These tests were generated using fallback mode (AI unavailable)
# For better, context-aware test cases, configure Claude CLI or Anthropic API.

Feature: {feature_name}
  
  Ticket: {ticket_key}
  Type: {issue_type}

"""
    
    # ACCEPTANCE CRITERIA BASED TESTS (if available)
    if has_ac:
        gherkin_output += """  # ═══════════════════════════════════════════════════════════════
  # ACCEPTANCE CRITERIA TESTS
  # ═══════════════════════════════════════════════════════════════

"""
        for idx, ac in enumerate(parsed_content['acceptance_criteria'], 1):
            ac_clean = ac.replace('\n', ' ').strip()
            if len(ac_clean) > 80:
                ac_clean = ac_clean[:77] + "..."
            
            gherkin_output += f"""  @acceptance_criteria @AC{idx} @priority_critical
  Scenario: {ac_clean}
    Given the system is ready
    When the acceptance criterion is evaluated
    Then the requirement should be met
    # TODO: Add specific steps based on: {ac[:100]}

"""
    
    # USER STORY BASED TESTS (if available)
    if has_user_stories:
        gherkin_output += """  # ═══════════════════════════════════════════════════════════════
  # USER STORY TESTS
  # ═══════════════════════════════════════════════════════════════

"""
        for idx, story in enumerate(parsed_content['user_stories'], 1):
            story_clean = story.replace('\n', ' ').strip()[:80]
            gherkin_output += f"""  @user_story @US{idx} @priority_high
  Scenario: Verify user story - {story_clean}
    Given I am a user
    When I follow the user story flow
    Then I should achieve the desired outcome
    # User Story: {story[:150]}

"""
    
    # If no structured criteria, add basic happy path
    if not has_ac and not has_user_stories:
        gherkin_output += f"""  @happy_path @smoke
  Scenario: Basic functionality test for {ticket_key}
    Given the feature/fix from {ticket_key} is implemented
    When I use the feature as intended
    Then it should work as expected
    
    # TODO: Add specific test steps based on ticket description:
    # {description[:200]}

"""
    
    gherkin_output += """
# ═══════════════════════════════════════════════════════════════
# Configure Claude CLI or Anthropic API for AI-generated, context-aware tests
# ═══════════════════════════════════════════════════════════════
"""
    
    return gherkin_output

# ═══════════════════════════════════════════════════════════════
# MULTI-AGENT AI SYSTEM ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List all available AI agents."""
    if not agent_manager:
        return jsonify({
            'success': False,
            'error': 'Multi-Agent system not initialized'
        }), 503
    
    agents = agent_manager.list_agents()
    return jsonify({
        'success': True,
        'agents': agents,
        'count': len(agents)
    })

@app.route('/api/agents/analyze-bug', methods=['POST'])
def analyze_bug_with_ai():
    """
    Analyze a bug report using AI.
    
    Request body:
    {
        "title": "Bug title",
        "description": "Bug description",
        "steps": "Steps to reproduce",
        "expected": "Expected behavior",
        "actual": "Actual behavior",
        "environment": "Environment",
        "priority": "Current priority"
    }
    """
    if not agent_manager:
        return jsonify({
            'success': False,
            'error': 'Multi-Agent system not initialized'
        }), 503
    
    try:
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Bug title is required'}), 400
        
        logger.info(f"Analyzing bug: {data.get('title')}")
        
        # Analyze bug using Bug Analyzer agent
        result = agent_manager.analyze_bug(data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Bug analysis failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agents/triage-bug', methods=['POST'])
def triage_bug_with_ai():
    """
    Auto-triage a bug using AI.
    
    Returns priority, squad assignment, and label recommendations.
    """
    if not agent_manager:
        return jsonify({
            'success': False,
            'error': 'Multi-Agent system not initialized'
        }), 503
    
    try:
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Bug title is required'}), 400
        
        logger.info(f"Triaging bug: {data.get('title')}")
        
        # Triage bug using Bug Triage agent
        result = agent_manager.triage_bug(data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Bug triage failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agents/check-semantic-duplicates', methods=['POST'])
def check_semantic_duplicates():
    """
    Check for semantic duplicates using AI.
    
    Goes beyond keyword matching to understand meaning.
    """
    if not agent_manager:
        return jsonify({
            'success': False,
            'error': 'Multi-Agent system not initialized'
        }), 503
    
    try:
        data = request.get_json()
        title = data.get('title', '')
        description = data.get('description', '')
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        logger.info(f"Semantic duplicate check: {title}")
        
        # First, get potential candidates using existing keyword search
        keyword_matches = search_duplicates(title, description)
        
        if not keyword_matches:
            return jsonify({
                'success': True,
                'duplicates_found': [],
                'message': 'No potential duplicates found'
            })
        
        # Then use AI to do semantic analysis
        bug_data = {
            'title': title,
            'description': description,
            'steps': data.get('steps', ''),
            'environment': data.get('environment', '')
        }
        
        # Prepare candidates for AI analysis
        candidates = [
            {
                'key': dup['key'],
                'title': dup['title'],
                'description': dup.get('description', '')[:500],  # Limit length
                'status': dup.get('status', 'Unknown')
            }
            for dup in keyword_matches[:5]  # Top 5 candidates
        ]
        
        result = agent_manager.check_duplicates_semantic(bug_data, candidates)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Semantic duplicate check failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agents/enhance-test-cases', methods=['POST'])
def enhance_test_cases_with_ai():
    """
    Enhance test cases using AI.
    
    Request body:
    {
        "test_cases": "Current Gherkin test cases",
        "enhancement_request": "What to improve (e.g., add edge cases)",
        "ticket_context": {
            "acceptance_criteria": [...],
            "user_stories": [...]
        }
    }
    """
    if not agent_manager:
        return jsonify({
            'success': False,
            'error': 'Multi-Agent system not initialized'
        }), 503
    
    try:
        data = request.get_json()
        test_cases = data.get('test_cases', '')
        enhancement_request = data.get('enhancement_request', '')
        ticket_context = data.get('ticket_context')
        
        if not test_cases:
            return jsonify({'error': 'Test cases are required'}), 400
        
        if not enhancement_request:
            return jsonify({'error': 'Enhancement request is required'}), 400
        
        logger.info(f"Enhancing test cases: {enhancement_request}")
        
        # Enhance test cases using Test Enhancer agent
        result = agent_manager.enhance_test_cases(
            test_cases, 
            enhancement_request,
            ticket_context
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Test case enhancement failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agents/smart-workflow', methods=['POST'])
def smart_bug_workflow():
    """
    Run complete AI-powered bug workflow.
    
    Orchestrates multiple agents:
    1. Analyze bug quality
    2. Auto-triage (priority, squad)
    3. Check semantic duplicates
    
    Returns comprehensive recommendations.
    """
    if not agent_manager:
        return jsonify({
            'success': False,
            'error': 'Multi-Agent system not initialized'
        }), 503
    
    try:
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Bug title is required'}), 400
        
        logger.info(f"Running smart workflow for: {data.get('title')}")
        
        # Run complete workflow
        result = agent_manager.smart_bug_workflow(data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Smart workflow failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Check for required environment variables
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        logger.error("Error: JIRA_EMAIL and JIRA_API_TOKEN environment variables are required")
        logger.error("Please set them before running the app")
        exit(1)
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
