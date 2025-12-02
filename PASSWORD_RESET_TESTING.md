# Security Question Password Reset - Testing Guide

## Overview
This document provides instructions for testing the security question-based password reset feature, which allows users to reset their passwords without requiring email verification.

## Feature Components

### 1. Database Fields (Profile Model)
- `security_question`: CharField(max_length=255) - Stores the user's security question
- `security_answer`: CharField(max_length=255) - Stores the hashed answer

### 2. Forms (forms.py)
- `PasswordResetRequestForm`: Step 1 - Username/email input
- `SecurityQuestionAnswerForm`: Step 2 - Answer verification
- `NewPasswordForm`: Step 3 - New password setting
- `ProfileForm`: Updated to include security_question and security_answer fields

### 3. Views (views.py)
- `password_reset_no_email`: Validates username/email and displays security question
- `password_reset_security_question`: Verifies answer and proceeds to password reset
- `password_reset_new_password`: Sets new password and completes reset
- `edit_profile`: Updated to hash security_answer before saving

### 4. Templates
- `password_reset_no_email.html`: Step 1 UI
- `password_reset_security_question.html`: Step 2 UI
- `password_reset_new_password.html`: Step 3 UI
- `edit_profile.html`: Updated with security question section
- `login.html`: Updated "Forgot Password?" link

### 5. URLs (urls.py)
- `/reset-password/` - Step 1
- `/reset-password/security-question/` - Step 2
- `/reset-password/new-password/` - Step 3

## Testing Procedure

### Pre-Test Setup

1. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**: http://127.0.0.1:8000/

### Test Case 1: Setting Up Security Question (First-Time Setup)

**Objective**: Verify users can set security questions during profile editing

**Steps**:
1. Log in with an existing account
2. Navigate to Profile → Edit Profile
3. Scroll to "Security Question (Optional)" section
4. Fill in:
   - **Security Question**: "What was your first pet's name?"
   - **Security Answer**: "Fluffy"
5. Click "Save Changes"

**Expected Results**:
- ✅ Form saves successfully
- ✅ Redirects to profile page
- ✅ Security answer is hashed in database (not plain text)
- ✅ No errors displayed

**Database Verification**:
```sql
-- Check if answer is hashed (should start with pbkdf2_sha256$)
SELECT security_question, security_answer FROM pallate_profile WHERE user_id = <your_user_id>;
```

### Test Case 2: Complete Password Reset Flow (Happy Path)

**Objective**: Test full password reset workflow with correct information

**Steps**:

**Step 1: Request Password Reset**
1. Log out of the account
2. Go to login page: http://127.0.0.1:8000/login/
3. Click "Forgot Password?" link
4. Enter username or email of account with security question set
5. Click "Continue"

**Expected Results**:
- ✅ Redirects to security question page
- ✅ Displays the security question set by user
- ✅ Shows username for verification
- ✅ Session stores `reset_user_id`

**Step 2: Answer Security Question**
1. Enter the correct answer (case-insensitive): "fluffy" or "Fluffy"
2. Click "Verify Answer"

**Expected Results**:
- ✅ Answer is verified successfully
- ✅ Redirects to new password page
- ✅ Session maintains `reset_user_id`

**Step 3: Set New Password**
1. Enter new password in both fields (e.g., "NewSecurePass123!")
2. Passwords must match
3. Click "Reset Password"

**Expected Results**:
- ✅ Password is updated successfully
- ✅ Success message with green checkmark displayed
- ✅ "Login with new password" link appears
- ✅ Session data is cleared (`reset_user_id` removed)
- ✅ Password is hashed in database

**Step 4: Login with New Password**
1. Click "Login with new password" or go to login page
2. Enter username and new password
3. Click "Login"

**Expected Results**:
- ✅ Login successful
- ✅ Redirects to dashboard
- ✅ User can access all features

### Test Case 3: Error Handling - Invalid Username/Email

**Objective**: Verify system handles non-existent users gracefully

**Steps**:
1. Go to `/reset-password/`
2. Enter non-existent username: "nonexistentuser123"
3. Click "Continue"

**Expected Results**:
- ✅ Error message: "No account found with that username or email"
- ✅ Stays on step 1 page
- ✅ Form data is preserved
- ✅ No session data created

### Test Case 4: Error Handling - No Security Question Set

**Objective**: Verify system handles users without security questions

**Steps**:
1. Create a new account without setting security question
2. Log out
3. Go to `/reset-password/`
4. Enter the new account's username
5. Click "Continue"

**Expected Results**:
- ✅ Error message: "No security question set for this account. Please contact support."
- ✅ Stays on step 1 page
- ✅ Suggests contacting admin
- ✅ No session data created

### Test Case 5: Error Handling - Wrong Security Answer

**Objective**: Verify incorrect answers are rejected

**Steps**:
1. Complete Step 1 successfully
2. On security question page, enter wrong answer: "WrongAnswer"
3. Click "Verify Answer"

**Expected Results**:
- ✅ Error message: "Incorrect answer. Please try again."
- ✅ Stays on step 2 page
- ✅ Security question still displayed
- ✅ Session data maintained
- ✅ Form is cleared for retry

### Test Case 6: Error Handling - Password Mismatch

**Objective**: Verify password validation works

**Steps**:
1. Complete Steps 1 and 2 successfully
2. On new password page:
   - **New Password**: "Password123!"
   - **Confirm Password**: "DifferentPass123!"
3. Click "Reset Password"

**Expected Results**:
- ✅ Error message: "Passwords do not match"
- ✅ Stays on step 3 page
- ✅ Form fields are cleared
- ✅ Session data maintained
- ✅ Password is NOT changed

### Test Case 7: Session Security - Direct URL Access

**Objective**: Verify unauthorized access to reset steps is blocked

**Steps**:
1. **Without starting reset flow**, directly access:
   - http://127.0.0.1:8000/reset-password/security-question/
   - http://127.0.0.1:8000/reset-password/new-password/

**Expected Results**:
- ✅ Redirects to `/reset-password/` (step 1)
- ✅ Error message: "Please start the password reset process from the beginning"
- ✅ Cannot skip steps
- ✅ No password reset possible

### Test Case 8: Case-Insensitive Answer Verification

**Objective**: Verify security answers are case-insensitive

**Steps**:
1. Set security answer as "MyAnswer"
2. Start password reset flow
3. Enter answer as "myanswer" (all lowercase)
4. Complete reset

**Expected Results**:
- ✅ Answer accepted despite different case
- ✅ Password reset succeeds
- ✅ Login with new password works

### Test Case 9: Updating Security Question

**Objective**: Verify users can change their security questions

**Steps**:
1. Log in with an account that has a security question set
2. Go to Edit Profile
3. Change:
   - **Security Question**: "What city were you born in?"
   - **Security Answer**: "NewYork"
4. Save changes
5. Log out and start password reset
6. Verify new question appears
7. Answer with "NewYork"

**Expected Results**:
- ✅ Question updates successfully
- ✅ Old answer no longer works
- ✅ New answer works
- ✅ Password reset completes

### Test Case 10: Security - Answer Hashing

**Objective**: Verify security answers are never stored in plain text

**Steps**:
1. Set a security answer: "TestAnswer123"
2. Check database directly

**Database Query**:
```sql
SELECT security_answer FROM pallate_profile WHERE user_id = <user_id>;
```

**Expected Results**:
- ✅ Answer starts with `pbkdf2_sha256$`
- ✅ Contains random salt
- ✅ Original answer not visible
- ✅ Cannot be reverse-engineered

**Example**:
```
pbkdf2_sha256$870000$randomsalt$hashedvalue
```

## Edge Cases to Test

### Edge Case 1: Session Timeout
1. Start password reset (Step 1)
2. Clear browser cookies/session
3. Try to proceed to Step 2

**Expected**: Redirects to Step 1 with error message

### Edge Case 2: Multiple Reset Attempts
1. Start reset for User A
2. Complete Step 1 for User B (different user)
3. Session should update to User B

**Expected**: Last user's reset_user_id is stored

### Edge Case 3: Special Characters in Answer
1. Set answer with special chars: "My-Pet's Name!"
2. Enter same during reset

**Expected**: Exact match required, special chars preserved

### Edge Case 4: Empty Security Question
1. Try to save profile with question but no answer
2. Or vice versa

**Expected**: Both should be optional, but if one is filled, consider validation

## Security Considerations

### What This Feature Provides:
- ✅ Password recovery without email dependency
- ✅ Hashed storage of security answers
- ✅ Session-based flow prevents URL manipulation
- ✅ Case-insensitive answer matching (user-friendly)
- ✅ Clear error messages without revealing sensitive info

### What This Feature Does NOT Provide:
- ❌ Multi-factor authentication
- ❌ Rate limiting on answer attempts
- ❌ Account lockout after failed attempts
- ❌ Email notification on password change
- ❌ Password history tracking

### Recommended Improvements (Future):
1. Add rate limiting (max 5 attempts per 15 minutes)
2. Log password reset activities
3. Send notification to user's backup email (if available)
4. Implement CAPTCHA to prevent automated attacks
5. Add account lockout after multiple failed answers

## Browser Testing

Test on multiple browsers:
- ✅ Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Safari (if available)

## Mobile Responsiveness

Test on mobile devices/responsive mode:
- ✅ Forms are readable
- ✅ Buttons are clickable
- ✅ Input fields are properly sized
- ✅ Dark theme renders correctly

## Integration Testing Checklist

- [ ] All 10 test cases passed
- [ ] Edge cases handled
- [ ] Security answer is always hashed
- [ ] Session management works correctly
- [ ] Error messages are user-friendly
- [ ] UI is consistent with existing design
- [ ] No console errors in browser
- [ ] Database constraints respected
- [ ] Migrations applied successfully
- [ ] Documentation updated

## Troubleshooting

### Issue: "CSRF verification failed"
**Solution**: Ensure `{% csrf_token %}` is present in all forms

### Issue: "Session data not persisting"
**Solution**: Check SESSION_ENGINE in settings.py, ensure cookies are enabled

### Issue: "Password reset succeeds but can't login"
**Solution**: Verify User.set_password() is called, not direct password field assignment

### Issue: "Security answer not matching"
**Solution**: Check hashing is consistent - use check_password() for verification

## Conclusion

This password reset system provides a robust alternative to email-based recovery, suitable for environments where email services (like Supabase SMTP) are unavailable. The security question approach balances user convenience with basic security measures.

**Important**: This is a development/fallback solution. For production systems, consider implementing additional security measures listed in the "Recommended Improvements" section.
