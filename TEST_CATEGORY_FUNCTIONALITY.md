# Category Functionality Testing Guide

This guide outlines how to test the newly implemented category functionality for artwork uploads and filtering.

## 1. Test Category Selection During Artwork Upload

### Setup:
- Login as any user
- Navigate to "Upload Artwork" page

### Steps:
1. Fill in artwork title and description
2. Select an image file
3. Click on the "Select Categories" dropdown
4. Select multiple categories (e.g., "Digital Art", "Illustration")
5. Click "Apply" button
6. Submit the form

### Expected Result:
- Selected categories should be saved with the artwork
- Visual feedback should be shown when categories are selected
- The dropdown should close after applying selections

## 2. Test Category Filtering on Dashboard

### Setup:
- Ensure there are artworks with different categories in the database
- Login as any user

### Steps:
1. Go to the dashboard
2. Click on the "Filter by Category" dropdown
3. Select one or more categories
4. Click "Apply" button

### Expected Result:
- Only artworks matching the selected categories should be displayed
- Smooth AJAX loading without page refresh
- Visual feedback during loading
- Proper error handling if something goes wrong

## 3. Test Clear Filters Functionality

### Setup:
- Apply some category filters on the dashboard

### Steps:
1. With filters applied, click on the "Filter by Category" dropdown
2. Click the "Clear" button

### Expected Result:
- All checkboxes should be unchecked
- All categories should be cleared from the filter
- Dashboard should show all artworks again

## 4. Test Recent Uploads Scrolling

### Setup:
- Ensure there are multiple artworks in the database

### Steps:
1. Go to the dashboard
2. Observe the "Recent Uploads" section
3. Wait for auto-scroll to begin
4. Move mouse over the scroller
5. Try manually scrolling

### Expected Result:
- Auto-scroll should pause when mouse is over the scroller
- Manual scrolling should work smoothly
- Cards should snap to position when scrolling stops

## 5. Test API Endpoint for Category Filtering

### Setup:
- Use a tool like Postman or curl

### Steps:
1. Make a GET request to `/api/fetch-artworks-by-category/` with `categories` parameter
2. Try with single category: `?categories=Digital Art`
3. Try with multiple categories: `?categories=Digital Art,Illustration`

### Expected Result:
- JSON response with filtered artworks
- Correct handling of multiple categories
- Proper error response for invalid requests

## 6. Test Category Display on Artwork Cards

### Setup:
- Ensure artworks have categories assigned

### Steps:
1. View artwork cards on dashboard
2. Check recent uploads section
3. Look for category tags on each card

### Expected Result:
- Categories should be displayed as tags on each artwork card
- Limited to 3 categories with "+X more" indicator if there are more
- Proper styling matching the overall design

## Edge Cases to Test

### 1. No Categories Selected
- Filtering with no categories should show all artworks

### 2. No Matching Artworks
- Filtering with categories that don't match any artworks should show appropriate message

### 3. Special Characters in Categories
- Categories with special characters should be handled correctly

### 4. Large Number of Categories
- Dropdown should handle scrolling when there are many categories

## Performance Checks

1. **Page Load Time**
   - Dashboard should load quickly even with category filtering JavaScript

2. **AJAX Response Time**
   - Filtering should be responsive (under 1 second)

3. **Memory Usage**
   - No memory leaks from event listeners

## Mobile Responsiveness

Test all functionality on different screen sizes:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)