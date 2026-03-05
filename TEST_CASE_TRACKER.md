# Test Case Tracker Feature

## Overview

The Test Case Tracker transforms the User Journey page into a comprehensive test execution management tool. It reads test case data from an Excel file and provides real-time tracking of test execution status across multiple platforms.

## Features

### 1. Statistics Dashboard
A visual dashboard displaying key metrics:
- **Total Test Cases**: Complete count of all test cases
- **Passed**: Number and percentage of passed tests (green)
- **Failed**: Number and percentage of failed tests (red)
- **In Progress**: Number and percentage of tests currently being executed (orange)
- **Blocked**: Number and percentage of blocked tests (purple)
- **Not Started**: Number and percentage of tests not yet started (gray)

All statistics are calculated in real-time based on the current status of test cases.

### 2. Platform Status Tracking
Each test case displays status for three platforms:
- **WEB**: Web platform execution status
- **iOS**: iOS app execution status
- **Android**: Android app execution status

Platform badges are color-coded:
- 🟢 **Green**: Passed
- 🔴 **Red**: Failed
- 🟣 **Purple**: Blocked
- 🟡 **Orange**: In Progress / Testing
- ⚪ **Gray**: Not tested

### 3. Test Execution Status
Each test case has a dropdown to track execution progress:
- **Not Started**: Test has not been executed yet
- **In Progress**: Test is currently being executed
- **Passed**: Test completed successfully
- **Failed**: Test found defects
- **Blocked**: Test cannot be executed due to blockers

Status changes update the statistics dashboard in real-time.

### 4. Test Case Information
Each test case card displays:
- **Test Case ID**: Unique identifier (e.g., TC-001)
- **Platform Status Badges**: Status for WEB, iOS, Android
- **Test Status Dropdown**: Current execution status
- **BDD Format**: Given/When/Then structure
  - **GIVEN** (Blue): Initial conditions/context
  - **WHEN** (Orange): Actions taken
  - **THEN** (Green): Expected outcomes
- **JIRA Link**: Link to associated defect (if any)

### 5. Section Organization
Test cases are organized into collapsible sections:
- Each section represents a Journey Step
- Section headers show step number and test case count
- Click to expand/collapse individual sections
- "Expand All" / "Collapse All" controls for quick navigation

## Data Source

The tracker reads data from an Excel file:
```
/Users/mde/Downloads/Loyalty 2.0 - Friends & Family.xlsx
Sheet: DO NOT EDIT - Loyalty 2.0_MASTE
```

### Excel Column Mapping
- **Journey Step**: Section/journey step name
- **Customer status**: GIVEN block (initial state)
- **Current step of the User**: WHEN block (action)
- **Expected behaviour**: THEN block (expected result)
- **Status (renamed to WEB)**: Web platform status
- **Functionality (renamed to iOS)**: iOS platform status
- **Unnamed: 6 (renamed to Android)**: Android platform status
- **Jira links for defects**: Link to JIRA defect ticket

## API Endpoint

### GET `/api/user-journey`

Returns structured test case data with statistics.

**Response Structure:**
```json
{
  "success": true,
  "data": {
    "title": "Loyalty 2.0 - Friends & Family",
    "subtitle": "Test Case Tracker",
    "sections": [
      {
        "title": "Journey Step Name",
        "scenarios": [
          {
            "id": "TC-001",
            "given": "Initial condition",
            "when": "Action taken",
            "then": "Expected result",
            "platforms": {
              "web": "Passed",
              "ios": "Not tested",
              "android": "Failed"
            },
            "jira_link": "https://...",
            "test_status": "Not Started"
          }
        ]
      }
    ],
    "statistics": {
      "total": 150,
      "not_started": 100,
      "in_progress": 20,
      "passed": 25,
      "failed": 3,
      "blocked": 2
    }
  }
}
```

## UI Components

### Statistics Dashboard
Located at the top of the page, provides a quick overview:
- Color-coded stat cards with gradients
- Large numbers for easy reading
- Percentage calculations
- Hover effects for interactivity

### Section Headers
- Green gradient background (HelloFresh brand colors)
- Section number badge
- Expandable/collapsible toggle
- Test case count badge
- Hover effects

### Test Case Cards
- White background with shadow
- Header row with:
  - Test Case ID badge (green)
  - Platform status badges (color-coded)
  - Status dropdown (color-coded)
- BDD blocks with left-border color coding
- JIRA link (if available)
- Hover lift effect

## User Interactions

### Viewing Statistics
- Statistics automatically update when test statuses change
- Percentages calculated in real-time
- All metrics visible at a glance

### Managing Test Execution
1. Navigate to the User Journey page
2. Expand a section to see test cases
3. Select execution status from dropdown
4. Watch statistics update in real-time
5. Click JIRA link to view related defects

### Navigation
- **Expand All**: Open all sections at once
- **Collapse All**: Close all sections
- **Click Section Header**: Toggle individual section
- Sections remember state during session

## Styling

### Color Scheme
- **Passed**: Green (#16a34a)
- **Failed**: Red (#dc2626)
- **Blocked**: Purple (#9333ea)
- **In Progress**: Orange (#f59e0b)
- **Not Started**: Gray (#6b7280)
- **Brand Green**: #57a635 (HelloFresh)

### Responsive Design
- Grid layout adapts to screen size
- Mobile-optimized statistics (2 columns)
- Stack elements vertically on small screens
- Touch-friendly controls

## Benefits

### For QA Teams
- **Centralized Tracking**: All test cases in one place
- **Real-Time Updates**: Instant status visibility
- **Platform Coverage**: Track testing across all platforms
- **Progress Monitoring**: Clear statistics and metrics
- **BDD Format**: Consistent test case structure

### For Project Managers
- **Quick Overview**: Statistics dashboard at a glance
- **Progress Tracking**: See execution progress in real-time
- **Risk Identification**: Failed/blocked tests clearly visible
- **Coverage Analysis**: Platform-specific test coverage

### For Developers
- **JIRA Integration**: Quick access to defect details
- **Test Context**: BDD format provides clear requirements
- **Platform-Specific Issues**: See which platform has issues

## Technical Details

### Frontend State Management
- React state for test status updates
- Real-time statistics calculation
- Persistent section expansion state
- Color-coded status classes

### Backend Processing
- Pandas for Excel parsing
- Dynamic column renaming
- Null value handling
- Test case ID generation (TC-001, TC-002, etc.)

### Performance
- Efficient data parsing
- Minimal re-renders
- Smooth animations
- Lazy loading (sections collapsed by default)

## Future Enhancements (Ideas)

1. **Persistent Storage**: Save test status to database
2. **Export Reports**: Generate execution reports
3. **Filtering**: Filter by status, platform, section
4. **Sorting**: Sort by ID, status, platform
5. **Search**: Search test cases by content
6. **History**: Track status changes over time
7. **Assignments**: Assign test cases to testers
8. **Comments**: Add notes to test cases
9. **Attachments**: Add screenshots/evidence
10. **Bulk Updates**: Update multiple tests at once

## Maintenance

### Updating Test Cases
1. Update the Excel file with new test cases
2. Refresh the page (no code changes needed)
3. New test cases automatically appear

### Adding Platforms
To add a new platform (e.g., Desktop):
1. Add column to Excel file
2. Update backend column mapping in `app.py`
3. Update frontend `PlatformStatus` interface
4. Add badge rendering in JSX
5. Update CSS for platform badge styling

## Troubleshooting

### Excel File Not Found
- Ensure file exists at specified path
- Check file permissions
- Verify sheet name matches exactly

### Incorrect Data Parsing
- Check column names match expected format
- Verify first row contains platform headers
- Ensure Excel file is not open/locked

### Statistics Not Updating
- Check browser console for errors
- Verify state management in React
- Clear browser cache and reload

## Related Files

- `app.py`: Backend endpoint at line 2189
- `frontend/src/pages/UserJourney.tsx`: Frontend component
- `frontend/src/pages/UserJourney.css`: Styling
- Excel file: `/Users/mde/Downloads/Loyalty 2.0 - Friends & Family.xlsx`
