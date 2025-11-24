# Custom Goals Feature

## Overview
Added ability for users to set custom nutrition goals during registration and update them in settings.

## Changes Made

### 1. Registration Page (`backend/templates/register.html`)
**Added:**
- Goal input fields for:
  - Daily Calories (1000-5000 kcal)
  - Daily Protein (50-300g)
  - Daily Carbs (50-500g)
  - Daily Fat (20-200g)
- Default values provided (2000 kcal, 120g protein, 250g carbs, 65g fat)
- Styled goals section with purple theme

### 2. Settings Page (`backend/templates/settings.html`)
**New page created with:**
- Display of current goals in card format
- Form to update all nutrition goals
- Recommended ranges for each nutrient
- Account information display (read-only)
- Success/error message handling

### 3. Backend Routes (`backend/app.py`)

#### Updated `/register` route:
- Extracts custom goals from form data
- Creates user with personalized goals
- Falls back to defaults if not provided

#### New `/settings` route:
- GET: Displays current user goals
- POST: Updates user goals in database
- Requires authentication
- Shows success/error messages

### 4. Styling (`backend/static/css/style.css`)
**Added styles for:**
- `.goals-section` - Registration goals container
- `.form-row` - Two-column form layout
- `.settings-container` - Settings page layout
- `.settings-card` - Card styling
- `.current-goals` - Goal display grid
- `.goal-item` - Individual goal cards
- `.success-message` - Success feedback
- Responsive design for mobile

### 5. Navigation
**Updated templates:**
- `chat.html` - Added Settings link
- `calendar.html` - Added Settings link

## User Flow

### Registration
1. User fills in name, email, password
2. User sets custom nutrition goals (or uses defaults)
3. Goals are saved to ChromaDB
4. User is logged in and redirected to chat

### Settings
1. User clicks "Settings" in navigation
2. Current goals displayed in cards
3. User can update any goal value
4. Click "Save Changes"
5. Goals updated in database
6. Success message displayed

## Database Schema

### User Document (ChromaDB)
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "hashed_password",
  "created_at": "2025-11-25T00:00:00Z",
  "goals": {
    "daily_calories": 2000,
    "daily_protein": 120,
    "daily_carbs": 250,
    "daily_fat": 65
  }
}
```

## API Endpoints

### POST /register
**Request:**
```
name=John Doe
email=user@example.com
password=securepass
daily_calories=2200
daily_protein=150
daily_carbs=280
daily_fat=70
```

**Response:**
- Redirects to `/` (chat page)
- Session cookie set

### GET /settings
**Response:**
- Renders settings page with current goals

### POST /settings
**Request:**
```
daily_calories=2200
daily_protein=150
daily_carbs=280
daily_fat=70
```

**Response:**
- Updates goals in database
- Renders settings page with success message

## Testing

### Manual Testing Steps
1. **Registration with custom goals:**
   - Go to `/register`
   - Fill in all fields including custom goals
   - Submit form
   - Verify goals are saved

2. **Registration with default goals:**
   - Go to `/register`
   - Fill in only name, email, password
   - Submit form
   - Verify default goals (2000/120/250/65) are used

3. **Update goals in settings:**
   - Login
   - Go to `/settings`
   - Change goal values
   - Click "Save Changes"
   - Verify success message
   - Check that new goals are reflected in recommendations

4. **Goal validation:**
   - Try to set calories < 1000 or > 5000
   - Try to set protein < 50 or > 300
   - Verify HTML5 validation works

## Benefits

1. **Personalization**: Users can set goals based on their specific needs
2. **Flexibility**: Goals can be updated anytime
3. **Better Recommendations**: AI uses custom goals for personalized advice
4. **User Control**: Empowers users to manage their nutrition targets

## Future Enhancements

- Goal presets (Weight Loss, Muscle Gain, Maintenance)
- Goal history tracking
- Progress visualization
- Goal achievement badges
- Macro ratio calculator
- BMR/TDEE calculator integration

---

**Feature Status**: ✅ Complete and Ready for Testing
**Date**: November 25, 2025
**Developer**: Team Mindful Eating
