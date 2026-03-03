# AWS Bedrock Setup Guide for AI Test Case Generation

This guide will help you enable AI-powered test case generation using AWS Bedrock with Claude.

## Overview

The Bug Reporter now includes an **AI Test Case Generator** powered by Claude 3.5 Sonnet via AWS Bedrock. This feature analyzes JIRA tickets and Google Drive documents to generate comprehensive, production-ready Cucumber/Gherkin test scenarios.

---

## Prerequisites

- AWS Account with Bedrock access
- IAM permissions for Bedrock
- Bug Reporter application set up

---

## Step 1: Request AWS Bedrock Access at HelloFresh

**Recommended: Use HelloFresh Enterprise AWS Account**

1. Contact your **DevOps** or **Platform Engineering** team
2. Request access to **AWS Bedrock** for your project
3. Ask for:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Confirmation that **Anthropic Claude** models are enabled
   - Preferred AWS Region (usually `us-east-1` or `eu-west-1`)

**Why Enterprise?**
- ✅ Centralized billing and cost tracking
- ✅ Compliance and security policies already configured
- ✅ No personal AWS charges
- ✅ Shared model access approvals

---

## Step 2: Enable Claude Models in AWS Bedrock

If your team hasn't enabled Claude models yet:

1. Log into **AWS Console** → **Amazon Bedrock**
2. Navigate to **Model access** (left sidebar under "Foundation models")
3. Click **Manage model access** or **Modify model access**
4. Find **Anthropic** section
5. Enable these models:
   - ✅ **Claude 3.5 Sonnet v2** (Recommended - ID: `anthropic.claude-3-5-sonnet-20241022-v2:0`)
   - ✅ **Claude 3 Sonnet** (Alternative - ID: `anthropic.claude-3-sonnet-20240229-v1:0`)
6. Click **Request model access** or **Save changes**
7. Wait for approval (usually instant for Claude models)

### Verify Model Access

Run this AWS CLI command to confirm:

```bash
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[?contains(modelId, `anthropic`)]'
```

---

## Step 3: Configure Your Application

### Add AWS Credentials to `.env`

Edit your `.env` file and add:

```bash
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1

# Claude Model (use one of these)
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0  # Latest Sonnet (recommended)
# BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0  # Claude 3 Sonnet (alternative)
```

### Security Best Practices

⚠️ **Never commit your `.env` file to Git**

- `.env` is already in `.gitignore`
- Use environment variables in production (Vercel, Railway, etc.)
- Rotate keys if accidentally exposed

---

## Step 4: Test the Integration

### 1. Restart the Application

```bash
./start.sh
```

Check the console output for:

```
[INFO] AWS Bedrock client initialized with model: anthropic.claude-3-5-sonnet-20241022-v2:0
```

### 2. Test AI Generation

1. Open the app: **http://localhost:5000**
2. Click **🧪 AI Test Cases** tab
3. Enter a JIRA ticket (e.g., `REW-323`)
4. Click **✨ Generate AI Test Cases**
5. Wait 5-15 seconds for AI generation
6. Review the comprehensive Gherkin scenarios!

---

## What the AI Generates

Claude AI creates:

- **Feature** description with context
- **Acceptance Criteria Tests** - One scenario per criterion found (tagged `@AC1`, `@AC2`, etc.)
- **User Story Tests** - Validates "As a/I want/So that" fulfillment
- **Business Rule Tests** - Ensures rules are enforced
- **Happy Path** - Ideal user journey (`@happy_path` `@smoke`)
- **Critical Path** - Essential business flows (`@critical_path`)
- **Edge Cases** - Boundary conditions (`@edge_case`)
- **Sad Path** - Error handling (`@sad_path` `@validation`)
- **Regression** - Side effect prevention (`@regression`)
- **Scenario Outlines** - Data-driven examples with tables
- **Platform-specific scenarios** - iOS, Android, Web considerations

### Example Output

```gherkin
Feature: Implement loyalty points redemption

  # ═══════════════════════════════════════════════
  # Test cases generated from:
  #   ✓ 3 Acceptance Criteria found
  #   ✓ 1 User Stories found
  # ═══════════════════════════════════════════════

  Background:
    Given the system is in a stable state
    And all prerequisites are met
    And test data is prepared

  @acceptance_criteria @priority_critical @AC1
  Scenario: User can redeem points for discount
    Given a user has 500 loyalty points
    When the user attempts to redeem 100 points
    Then 100 points should be deducted from balance
    And a €10 discount code should be generated
    And the user receives a confirmation email

  @happy_path @smoke @priority_high
  Scenario: Successful points redemption flow
    Given I am a logged-in user with sufficient points
    When I navigate to the rewards page
    And I select a reward to redeem
    And I confirm the redemption
    Then I should see a success message
    And my points balance should be updated
    And I should receive my reward

  # ... more scenarios ...
```

---

## Troubleshooting

### "AWS Bedrock not available, falling back to rule-based generation"

**Causes:**
- Missing AWS credentials in `.env`
- Invalid credentials
- Incorrect region
- Model not enabled

**Solutions:**
1. Check `.env` has all AWS variables
2. Verify credentials with: `aws sts get-caller-identity`
3. Confirm model access in AWS Console → Bedrock → Model access
4. Check region matches where models are enabled

### "AccessDeniedException: User is not authorized"

**Fix:** Update IAM permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.*"
    }
  ]
}
```

### "ThrottlingException: Rate exceeded"

**Fix:** Bedrock has usage limits per region:
- Implement retry logic
- Request quota increase in AWS Console
- Use exponential backoff

### Fallback Mode Works Fine

The application **automatically falls back** to rule-based test generation if AWS Bedrock is unavailable. This ensures the tool always works, even without AI.

---

## Cost Optimization

### AWS Bedrock Pricing (as of 2024)

**Claude 3.5 Sonnet:**
- Input: $0.003 per 1K tokens
- Output: $0.015 per 1K tokens

**Typical test case generation:**
- Input: ~1,500 tokens (ticket description)
- Output: ~2,000 tokens (test scenarios)
- **Cost per generation: $0.034** (~3-4 cents)

### Monthly Cost Estimates

- **10 test cases/day**: ~$10/month
- **50 test cases/day**: ~$50/month
- **100 test cases/day**: ~$100/month

**Much cheaper than manual test writing!** (Saves hours of QA time per test case)

### Cost Saving Tips

1. **Cache common patterns** - Reuse test scenarios for similar tickets
2. **Use for complex tickets only** - Simple bugs may not need AI
3. **Set AWS Budget Alerts** - Get notified at $50, $100, etc.
4. **Monitor usage** - Check AWS Cost Explorer regularly

---

## Alternative: Use Without AWS (Fallback Mode)

If AWS Bedrock is not available:

The application will **automatically use rule-based test generation**:
- ✅ Still extracts acceptance criteria
- ✅ Still generates Gherkin scenarios
- ✅ Less intelligent, but functional
- ✅ No AI costs

Simply leave AWS variables **empty** in `.env`:

```bash
# AWS Bedrock (optional - leave empty for fallback)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

---

## Support

**HelloFresh Internal:**
- Contact: DevOps / Platform Engineering
- Slack: #platform-engineering, #devops

**AWS Bedrock Issues:**
- AWS Support Console
- AWS Bedrock Documentation: https://docs.aws.amazon.com/bedrock/

**Bug Reporter Issues:**
- GitHub: https://github.com/mde-hf/ai-bug-reporter/issues
- Contact: @mde

---

## Next Steps

1. ✅ Complete AWS Bedrock setup
2. ✅ Test with a sample JIRA ticket
3. ✅ Share with your team
4. ✅ Monitor usage and costs
5. ✅ Provide feedback for improvements

**Happy testing!** 🚀
