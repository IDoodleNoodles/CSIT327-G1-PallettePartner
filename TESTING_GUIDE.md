# Testing Guide for New Features

## Prerequisites
- Virtual environment activated
- Database migrated (`python manage.py migrate`)
- Server running (`python manage.py runserver`)

## Test Scenarios

### 1. Test Profile Interests Field

**Steps:**
1. Login to the application
2. Navigate to Profile → Edit Profile
3. Add interests: "Digital Art, Fantasy, Character Design"
4. Save profile
5. Verify interests are saved and displayed

**Expected Result:**
- Interests field appears in edit form
- Data persists after save
- Displayed in profile view

---

### 2. Test Find Collaborators (Matching Algorithm)

**Setup:**
Create 3 test users with different profiles:
- User A: Art Type="Digital Artist", Interests="Fantasy, Sci-Fi"
- User B: Art Type="Digital Artist", Interests="Fantasy, Portraits"
- User C: Art Type="Traditional Artist", Interests="Landscapes"

**Steps (as User A):**
1. Login as User A
2. Click "Find Collaborators" in dashboard menu
3. Review suggested matches

**Expected Result:**
- User B shows high match score (art type + Fantasy match)
- User C shows lower match score (no art type match)
- Match reasons displayed correctly
- "Fantasy" listed as common interest

---

### 3. Test Collaboration Feedback System

**Steps:**
1. Create a collaboration post
2. Navigate to collaboration detail page
3. Click "Rate Collaboration" button
4. Select rating (1-5 stars)
5. Add comment (optional)
6. Submit feedback

**Expected Result:**
- Rating form displays with emoji icons
- Feedback saves successfully
- Average rating calculated and displayed
- Notification sent to collaboration owner
- Cannot submit duplicate feedback (unique constraint)

---

### 4. Test Collaboration Matches

**Setup:**
- Login as User A (collaboration owner)
- Create collaboration with profile containing interests

**Steps:**
1. Go to collaboration detail page
2. Click "Find Suggested Matches" button
3. View generated matches

**Expected Result:**
- Matches generated based on owner's profile
- Match scores calculated correctly
- Users sorted by match score
- Display art type and interests for each match

---

### 5. Test Featured Artists

**Admin Setup:**
1. Go to Django Admin (`/admin`)
2. Navigate to Profiles
3. Mark 2-3 profiles as "is_featured=True"
4. Save changes

**User Steps:**
1. Login as any user
2. Click "Featured Artists" in dashboard menu
3. Browse featured artists

**Expected Result:**
- Only featured artists displayed
- Featured badge shown
- Recent artworks preview displayed
- Link to full profile works

---

## Database Verification

### Check Profile Model
```python
python manage.py shell
```

```python
from pallattepartner.pallate.models import Profile
# Check interests field exists
profile = Profile.objects.first()
print(profile.interests)
print(profile.is_featured)
print(profile.get_interests_list())
```

### Check CollaborationFeedback Model
```python
from pallattepartner.pallate.models import CollaborationFeedback
feedbacks = CollaborationFeedback.objects.all()
for f in feedbacks:
    print(f"{f.reviewer.username} rated {f.rating}/5")
```

### Check CollaborationMatch Model
```python
from pallattepartner.pallate.models import CollaborationMatch
matches = CollaborationMatch.objects.all()
for m in matches:
    print(f"Score: {m.match_score} - {m.suggested_user.username}")
```

---

## API Endpoints Test

Test all new URLs are accessible:

1. `/find-collaborators/` - Find Collaborators page
2. `/collaboration/<id>/feedback/` - Feedback form
3. `/collaboration/<id>/matches/` - Suggested matches
4. `/featured-artists/` - Featured artists gallery

---

## Edge Cases to Test

### 1. Empty Interests
- Profile with no interests still displays correctly
- Matching algorithm handles empty interests gracefully

### 2. Duplicate Feedback Prevention
- Try submitting feedback twice for same collaboration
- Should see update form instead of create

### 3. No Matches Found
- Profile with unique interests/art type
- Should display "No matches found" message

### 4. Featured Artists - Empty State
- No featured artists marked
- Should display empty state message

### 5. Match Score Calculation
- User with only art type match = 50 points
- User with only 1 interest match = 20 points
- User with both = 70+ points

---

## Performance Checks

1. **Query Optimization**
   - Check N+1 queries with Django Debug Toolbar
   - Verify `select_related()` and `prefetch_related()` usage

2. **Page Load Times**
   - Find Collaborators with 50+ users
   - Featured Artists with multiple artworks

---

## Admin Panel Verification

1. Login to `/admin`
2. Verify new models appear:
   - Collaboration Feedbacks
   - Collaboration Matches
3. Test CRUD operations on new models
4. Verify list_display and filters work

---

## Mobile Responsiveness

Test all new pages on different screen sizes:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

Pages to test:
- Find Collaborators
- Collaboration Feedback
- Featured Artists
- Collaboration Matches

---

## Integration Tests

### Workflow 1: Complete Collaboration Cycle
1. User A creates collaboration
2. System suggests User B (matching profile)
3. User B contacts User A
4. Both users complete collaboration
5. Both submit feedback/ratings

### Workflow 2: Profile Matching
1. User updates profile with interests
2. Finds collaborators
3. Views matched user profile
4. Navigates to their artworks
5. Favorites artwork

---

## Rollback Plan

If issues occur:
```bash
# Rollback migration
python manage.py migrate pallate 0011

# Revert code changes
git checkout HEAD~1
```

---

## Success Criteria

✅ All new pages load without errors
✅ Forms submit successfully
✅ Data persists in database
✅ Matching algorithm returns relevant results
✅ Admin panel shows new models
✅ No Python/Django errors in console
✅ UI displays correctly on all devices
✅ Navigation links work correctly

---

## Known Issues

- URL namespace warning (pre-existing, does not affect functionality)

---

## Support

For issues or questions, check:
1. Server logs in terminal
2. Browser console for JS errors
3. Database via Django admin
4. Migration status: `python manage.py showmigrations`
