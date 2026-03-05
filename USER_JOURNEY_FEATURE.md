# User Journey Feature - Loyalty 2.0 Friends & Family

## Overview

Created a new "User Journey" page that reads test case specifications from the Excel file and displays them in a structured, interactive web interface matching the "DO NOT EDIT - Loyalty 2.0_MASTER_USECASE" tab structure.

## Implementation

### Backend (`app.py`)

**New Endpoint**: `GET /api/user-journey`

**Features**:
- Reads Excel file using pandas
- Parses the "DO NOT EDIT - Loyalty 2.0_MASTE" sheet
- Structures data into journey sections with scenarios
- Returns JSON formatted data

**Data Structure**:
```json
{
  "success": true,
  "data": {
    "title": "Loyalty 2.0 - Friends & Family",
    "subtitle": "User Journey & Test Cases",
    "sections": [
      {
        "title": "Entry Point",
        "scenarios": [
          {
            "given": "Given I am user who is not a user...",
            "when": "[Apps] I go to Profile page...",
            "then": "I should see the Loyalty 2.0 dashboard/page",
            "status": null
          }
        ]
      }
    ]
  }
}
```

### Frontend (`UserJourney.tsx`)

**Features**:
- Loads and displays journey data from backend
- Collapsible sections organized by journey steps
- BDD format display (Given/When/Then)
- Expand/Collapse all controls
- Scenario counter for each section
- Loading and error states
- Responsive design

**UI Components**:
1. **Header**:
   - Page title and subtitle
   - Expand All / Collapse All buttons

2. **Journey Sections**:
   - Numbered sections with green gradient headers
   - Click to expand/collapse
   - Test case count badge
   - Toggle arrow indicator

3. **Scenario Cards**:
   - **GIVEN** block (Blue border)
   - **WHEN** block (Orange border)
   - **THEN** block (Green border)
   - Status badge (if present)
   - Hover effects with elevation

### Styling (`UserJourney.css`)

**Color Scheme**:
- **Section Headers**: Green gradient (#57a635 → #6bc144)
- **GIVEN blocks**: Blue (#3b82f6)
- **WHEN blocks**: Orange (#f59e0b)
- **THEN blocks**: Green (#16a34a)

**Key Features**:
- Card-based layout with shadows
- Smooth animations (fadeIn, hover effects)
- Color-coded labels and borders
- Responsive grid layout
- Mobile-friendly design

## Excel Integration

**Requirements**:
- `pandas==3.0.1` - Excel file reading
- `openpyxl==3.1.5` - Excel file format support

**File Path**: `/Users/mde/Downloads/Loyalty 2.0 - Friends & Family.xlsx`

**Sheet**: "DO NOT EDIT - Loyalty 2.0_MASTE"

**Columns Mapped**:
- Journey Step → Section titles
- Customer status → GIVEN statements
- Current step of the User → WHEN statements
- Expected behaviour → THEN statements
- Status → Status badges

## Navigation

Added "User Journey" link to main navigation header.

**Route**: `/user-journey`

**Navigation Order**:
1. Report Bug
2. Dashboard
3. AI Test Cases
4. QA Analysis
5. **User Journey** ← NEW

## Data Processing

The backend processes the Excel data:
1. Reads all rows from the sheet
2. Identifies section headers (Journey Step column)
3. Groups scenarios under each section
4. Filters out empty rows
5. Converts to structured JSON

**Journey Sections Found**:
1. Entry Point
2. Points calculation
3. Redeeming rewards and redirection
4. Error and Loading states

## Features

### Section Management
- ✅ Collapsible sections
- ✅ Expand All / Collapse All controls
- ✅ First section expanded by default
- ✅ Click anywhere on header to toggle
- ✅ Visual toggle indicator (▶/▼)

### Scenario Display
- ✅ BDD format (Given/When/Then)
- ✅ Color-coded blocks
- ✅ Clean typography
- ✅ Status badges
- ✅ Hover effects

### UX Enhancements
- ✅ Loading spinner
- ✅ Error handling
- ✅ Responsive design
- ✅ Smooth animations
- ✅ Numbered sections
- ✅ Test case counts

## Testing

### Manual Testing
1. Navigate to http://localhost:5000/user-journey
2. Verify data loads correctly
3. Test expand/collapse functionality
4. Test Expand All / Collapse All buttons
5. Verify responsive layout on mobile
6. Check color coding and styling

### Expected Behavior
- Data loads from Excel file
- Sections are organized by journey steps
- Each scenario displays Given/When/Then
- Colors match BDD conventions
- Smooth animations on interactions

## Mobile Responsive

**Breakpoint**: 768px

**Mobile Optimizations**:
- Simplified grid layout
- Smaller padding and fonts
- Stacked section information
- Touch-friendly buttons
- Adjusted spacing

## Files Modified

1. **Backend**:
   - `app.py` - Added `/api/user-journey` endpoint (+90 lines)
   - `requirements.txt` - Added pandas and openpyxl

2. **Frontend**:
   - `frontend/src/pages/UserJourney.tsx` - Main component (175 lines)
   - `frontend/src/pages/UserJourney.css` - Styling (310 lines)
   - `frontend/src/App.tsx` - Added route
   - `frontend/src/components/Header.tsx` - Added navigation link

3. **Data**:
   - `loyalty_usecase_data.json` - Cached Excel data

## Benefits

### For QA Team
- ✅ View all test cases in web interface
- ✅ No need to open Excel
- ✅ Interactive browsing
- ✅ Easy navigation between sections
- ✅ Clean, readable format

### For Developers
- ✅ Understand user journeys
- ✅ See expected behaviors
- ✅ Reference test cases
- ✅ BDD format familiar

### For Team
- ✅ Single source of truth
- ✅ Always up-to-date (reads from Excel)
- ✅ Shareable URL
- ✅ Professional presentation

## Future Enhancements

Potential improvements:
1. **Search** - Find specific scenarios
2. **Filtering** - By status, section, keyword
3. **Export** - PDF or Markdown format
4. **Linking** - Link scenarios to JIRA tickets
5. **Status Updates** - Mark scenarios as tested
6. **Progress Tracking** - Overall completion percentage
7. **Comments** - Team annotations
8. **Version History** - Track changes over time
9. **Multiple Files** - Support different projects
10. **Auto-refresh** - Watch for Excel file changes

## Commit

**Commit ID**: `f21088d`

**Message**: "Add User Journey page from Excel data"

**Changes**:
- 5 files changed
- 1137 insertions(+)
- All tests passing

## Documentation

This document provides:
- Implementation details
- Data structure
- UI components
- Styling guide
- Testing instructions
- Future roadmap

## Summary

Successfully created a web-based viewer for the Loyalty 2.0 Friends & Family test case specifications. The page reads directly from the Excel file and presents the data in an interactive, color-coded, BDD-formatted interface that matches the original spreadsheet structure but with enhanced usability and visual appeal.
