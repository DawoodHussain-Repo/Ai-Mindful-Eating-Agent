# Mindful Eating - Next.js Frontend

Modern, minimal UI built with Next.js 15, TypeScript, Tailwind CSS, and shadcn/ui.

## Features

- ✅ **Personalized Onboarding** - Set custom calorie, protein, carbs, and fat goals
- ✅ **Simple Food Logging** - Natural language food entry
- ✅ **Real-time Progress Tracking** - Visual progress bars for daily goals
- ✅ **AI Recommendations** - Personalized nutrition insights
- ✅ **Clean Minimal UI** - Built with shadcn/ui components
- ✅ **Responsive Design** - Works on desktop and mobile

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Backend**: Flask API (Python)
- **Database**: MongoDB

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend Flask server running on `http://localhost:5000`
- MongoDB running locally

### Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   # .env.local is already created with:
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   ```
   http://localhost:3000
   ```

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx              # Landing page
│   ├── login/
│   │   └── page.tsx          # Login page
│   ├── onboarding/
│   │   └── page.tsx          # 3-step onboarding flow
│   ├── dashboard/
│   │   └── page.tsx          # Main dashboard
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   └── ui/                   # shadcn/ui components
├── lib/
│   ├── api.ts                # API client for Flask backend
│   └── utils.ts              # Utility functions
└── public/                   # Static assets
```

## Pages

### 1. Landing Page (`/`)
- Hero section with value proposition
- Feature highlights
- CTA buttons for signup/login

### 2. Onboarding (`/onboarding`)
**Step 1: Basic Info**
- Name, email, password

**Step 2: Calorie & Protein Goals**
- Daily calorie target
- Daily protein target (grams)

**Step 3: Macro Goals**
- Daily carbs target (grams)
- Daily fat target (grams)
- Summary of all goals

### 3. Login (`/login`)
- Email and password authentication
- Link to onboarding for new users

### 4. Dashboard (`/dashboard`)
**Main Features:**
- Food logging form with meal type selection
- Today's meals list with nutrition breakdown
- Daily progress bars (calories, protein, carbs, fat)
- AI-powered recommendations sidebar

## API Integration

The frontend communicates with the Flask backend via REST API:

### Endpoints Used:

```typescript
// Authentication
POST /register - Create new user with custom goals
POST /login - Authenticate user
GET /logout - End session

// Food Logging
POST /api/log-food - Log a meal
GET /api/get-logs - Get today's meals
GET /api/get-recommendations - Get AI recommendations
GET /api/get-stats - Get user statistics
```

### API Client (`lib/api.ts`)

```typescript
import { api } from '@/lib/api';

// Register with custom goals
await api.register(email, password, name, {
  daily_calories: 2000,
  daily_protein: 120,
  daily_carbs: 250,
  daily_fat: 65
});

// Log food
await api.logFood('grilled chicken 6oz, brown rice 1 cup', 'lunch');

// Get logs
const data = await api.getLogs();
```

## UI Components (shadcn/ui)

Used components:
- `Button` - Primary actions
- `Card` - Content containers
- `Input` - Text inputs
- `Label` - Form labels
- `Select` - Dropdowns
- `Textarea` - Multi-line text
- `Progress` - Progress bars
- `Badge` - Status indicators
- `Separator` - Visual dividers
- `Tabs` - Tab navigation
- `Dialog` - Modals

## Styling

### Color Scheme
- **Primary**: Green (#16a34a) - Health, growth
- **Secondary**: Blue - Trust, calm
- **Background**: Gradient from green-50 to blue-50
- **Text**: Gray scale for hierarchy

### Design Principles
- **Minimal**: Clean, uncluttered interface
- **White Space**: Generous spacing for readability
- **Typography**: Clear hierarchy with font weights
- **Responsive**: Mobile-first approach

## Development

### Run Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
npm start
```

### Lint Code
```bash
npm run lint
```

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## CORS Configuration

The Flask backend needs CORS enabled for the Next.js frontend:

```python
# backend/app.py
from flask_cors import CORS

CORS(app, supports_credentials=True, origins=['http://localhost:3000'])
```

## Session Management

- Sessions are managed by Flask backend
- Cookies are sent with `credentials: 'include'`
- Session persists for 7 days
- Automatic redirect to login if session expires

## Features in Detail

### Onboarding Flow
1. **Progressive Disclosure**: 3 steps to avoid overwhelming users
2. **Visual Progress**: Progress bar shows completion
3. **Validation**: Form validation before proceeding
4. **Helpful Tips**: Guidance for setting realistic goals

### Food Logging
1. **Natural Language**: Type food descriptions naturally
2. **Meal Type Selection**: Breakfast, lunch, dinner, snack
3. **Portion Guidance**: Hints for including portion sizes
4. **Instant Feedback**: Immediate nutrition breakdown

### Progress Tracking
1. **Visual Progress Bars**: Easy-to-understand goal tracking
2. **Color Coding**: Green for on-track, red for over
3. **Remaining Calories**: Shows how much left to eat
4. **Macro Breakdown**: Detailed protein, carbs, fat tracking

### AI Recommendations
1. **Personalized**: Based on your eating patterns
2. **Contextual**: Considers time of day, current intake
3. **Actionable**: Specific suggestions, not generic advice
4. **Positive**: Encouraging tone, not restrictive

## Troubleshooting

### Backend Connection Issues
```bash
# Check if backend is running
curl http://localhost:5000

# Check CORS headers
curl -H "Origin: http://localhost:3000" http://localhost:5000
```

### Session Issues
- Clear browser cookies
- Check Flask session configuration
- Verify MongoDB is running

### Build Errors
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

## Future Enhancements

- [ ] Dark mode support
- [ ] Mobile app (React Native)
- [ ] Meal planning feature
- [ ] Recipe suggestions
- [ ] Social sharing
- [ ] Progress charts and analytics
- [ ] Barcode scanning
- [ ] Voice input for food logging

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Check documentation
- Review API integration
- Verify backend is running
- Check browser console for errors

---

**Built with ❤️ using Next.js and shadcn/ui**
