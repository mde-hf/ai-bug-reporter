#!/usr/bin/env python3
"""
Test script for Multi-Agent AI System

Tests each agent individually and the complete workflow.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import AgentManager

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")

def print_result(agent_name, result):
    """Print agent result"""
    if result.get('success'):
        print(f"✅ {agent_name} - SUCCESS")
        print(f"   Model: {result.get('model')}")
        if 'usage' in result:
            print(f"   Tokens: {result['usage'].get('input_tokens', 0)} in, {result['usage'].get('output_tokens', 0)} out")
        print(f"\n   Response Preview:")
        response = result.get('response', '')
        preview = response[:300] + "..." if len(response) > 300 else response
        print(f"   {preview}\n")
    else:
        print(f"❌ {agent_name} - FAILED")
        print(f"   Error: {result.get('error')}\n")

def test_bug_analyzer(agent_manager):
    """Test Bug Analyzer Agent"""
    print_section("TEST 1: Bug Analyzer Agent")
    
    bug_data = {
        'title': 'Login fails on iOS app',
        'description': 'Users are unable to login on the iOS app. The app shows a timeout error.',
        'steps': '1. Open iOS app\n2. Enter valid credentials\n3. Tap login button',
        'expected': 'User should be logged in successfully',
        'actual': 'Error message: "Connection timeout"',
        'environment': 'Production',
        'priority': 'High'
    }
    
    print("Testing with bug data:")
    print(json.dumps(bug_data, indent=2))
    print("\nAnalyzing...")
    
    result = agent_manager.analyze_bug(bug_data)
    print_result("Bug Analyzer", result)
    
    return result.get('success', False)

def test_bug_triage(agent_manager):
    """Test Bug Triage Agent"""
    print_section("TEST 2: Bug Triage Agent")
    
    bug_data = {
        'title': 'Rewards redemption fails at checkout',
        'description': 'Production issue: users cannot redeem loyalty points during checkout on iOS',
        'steps': '1. Add items to cart\n2. Go to checkout\n3. Select "Use Points"\n4. Complete payment',
        'expected': 'Points should be deducted and order completed',
        'actual': 'Error: Points not applied, checkout fails'
    }
    
    print("Testing with bug data:")
    print(json.dumps(bug_data, indent=2))
    print("\nTriaging...")
    
    result = agent_manager.triage_bug(bug_data)
    print_result("Bug Triage", result)
    
    return result.get('success', False)

def test_duplicate_detective(agent_manager):
    """Test Duplicate Detective Agent"""
    print_section("TEST 3: Duplicate Detective Agent")
    
    bug_data = {
        'title': 'App crashes when opening profile',
        'description': 'The application force closes whenever I try to view my profile',
        'steps': 'Open app, tap profile icon',
        'environment': 'Production'
    }
    
    # Simulate some candidate duplicates
    candidates = [
        {
            'key': 'REW-123',
            'title': 'Profile page causes crash',
            'description': 'App shuts down when viewing profile',
            'status': 'Open'
        },
        {
            'key': 'REW-456',
            'title': 'Login screen not responsive',
            'description': 'Cannot tap login button',
            'status': 'Resolved'
        }
    ]
    
    print("Testing with bug data:")
    print(json.dumps(bug_data, indent=2))
    print("\nCandidate duplicates:")
    print(json.dumps(candidates, indent=2))
    print("\nChecking semantic duplicates...")
    
    result = agent_manager.check_duplicates_semantic(bug_data, candidates)
    print_result("Duplicate Detective", result)
    
    return result.get('success', False)

def test_test_enhancer(agent_manager):
    """Test Test Case Enhancer Agent"""
    print_section("TEST 4: Test Case Enhancer Agent")
    
    test_cases = """Feature: User Login
  
  @smoke @happy_path
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid email and password
    And I click the login button
    Then I should be logged in
    And I should see the home page
"""
    
    enhancement_request = "Add edge cases for error handling and invalid credentials"
    
    print("Original test cases:")
    print(test_cases)
    print(f"\nEnhancement request: {enhancement_request}")
    print("\nEnhancing...")
    
    result = agent_manager.enhance_test_cases(test_cases, enhancement_request)
    print_result("Test Enhancer", result)
    
    return result.get('success', False)

def test_smart_workflow(agent_manager):
    """Test complete smart workflow"""
    print_section("TEST 5: Smart Workflow (Orchestration)")
    
    bug_data = {
        'title': 'Referral link sharing fails on Android',
        'description': 'Users cannot share referral links via WhatsApp on Android devices',
        'steps': '1. Go to Referrals tab\n2. Tap Share button\n3. Select WhatsApp',
        'expected': 'WhatsApp opens with pre-filled referral message',
        'actual': 'Nothing happens, no WhatsApp intent triggered'
    }
    
    print("Testing complete workflow with bug data:")
    print(json.dumps(bug_data, indent=2))
    print("\nRunning smart workflow (multiple agents)...")
    
    result = agent_manager.smart_bug_workflow(bug_data)
    
    if result.get('workflow'):
        print(f"✅ Smart Workflow - SUCCESS")
        print(f"   Workflow: {result['workflow']}")
        print(f"   Steps completed: {len(result.get('steps', []))}")
        
        for step in result.get('steps', []):
            step_result = step.get('result', {})
            status = "✅" if step_result.get('success') else "❌"
            print(f"   {status} {step['step']} ({step['agent']})")
        
        if 'recommendations' in result:
            print("\n   Recommendations:")
            recs = result['recommendations']
            print(f"   - Priority: {recs.get('priority')}")
            print(f"   - Squad: {recs.get('squad')}")
            print(f"   - Labels: {', '.join(recs.get('labels', []))}")
            print(f"   - Quality Score: {recs.get('quality_score')}/10")
        print()
        return True
    else:
        print(f"❌ Smart Workflow - FAILED")
        print(f"   Error: {result.get('error')}\n")
        return False

def run_all_tests():
    """Run all agent tests"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "MULTI-AGENT AI SYSTEM TESTS" + " " * 31 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Check environment
    print("\n🔧 Checking environment...")
    aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    
    if not aws_key or not aws_secret:
        print("❌ AWS credentials not found in environment")
        print("   Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        sys.exit(1)
    
    print(f"✅ AWS credentials configured")
    print(f"   Region: {aws_region}")
    
    # Initialize Agent Manager
    print("\n🚀 Initializing Agent Manager...")
    try:
        agent_manager = AgentManager(aws_region=aws_region)
        print("✅ Agent Manager initialized")
        
        # List agents
        agents = agent_manager.list_agents()
        print(f"\n📋 Available agents: {len(agents)}")
        for agent in agents:
            print(f"   - {agent['name']}: {agent['description'][:60]}...")
    except Exception as e:
        print(f"❌ Failed to initialize Agent Manager: {e}")
        sys.exit(1)
    
    # Run tests
    results = {
        'Bug Analyzer': False,
        'Bug Triage': False,
        'Duplicate Detective': False,
        'Test Enhancer': False,
        'Smart Workflow': False
    }
    
    try:
        results['Bug Analyzer'] = test_bug_analyzer(agent_manager)
    except Exception as e:
        print(f"❌ Bug Analyzer test crashed: {e}\n")
    
    try:
        results['Bug Triage'] = test_bug_triage(agent_manager)
    except Exception as e:
        print(f"❌ Bug Triage test crashed: {e}\n")
    
    try:
        results['Duplicate Detective'] = test_duplicate_detective(agent_manager)
    except Exception as e:
        print(f"❌ Duplicate Detective test crashed: {e}\n")
    
    try:
        results['Test Enhancer'] = test_test_enhancer(agent_manager)
    except Exception as e:
        print(f"❌ Test Enhancer test crashed: {e}\n")
    
    try:
        results['Smart Workflow'] = test_smart_workflow(agent_manager)
    except Exception as e:
        print(f"❌ Smart Workflow test crashed: {e}\n")
    
    # Print summary
    print_section("TEST SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n   🎉 ALL TESTS PASSED! 🎉\n")
        sys.exit(0)
    else:
        print("\n   ⚠️  Some tests failed\n")
        sys.exit(1)

if __name__ == '__main__':
    run_all_tests()
