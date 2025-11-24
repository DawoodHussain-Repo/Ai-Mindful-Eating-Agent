# AI Mindful Eating Agent - Complete Setup Guide

## 🚀 Quick Start

This guide will help you set up the AI Mindful Eating Agent with ChromaDB and Gemini AI integration.

## 📋 Prerequisites

- **Python 3.8+** installed
- **ChromaDB Cloud Account** (free tier available at [trychroma.com](https://trychroma.com))
- **Google Gemini API Key** (free tier available at [ai.google.dev](https://ai.google.dev))

## 🔧 Step 1: Get Your API Keys

### ChromaDB Setup

1. Go to [https://trychroma.com](https://trychroma.com)
2. Sign up for a free account
3. Create a new database
4. Copy your:
   - API Key
   - Tenant ID
   - Database name

### Gemini API Setup

1. Go to [https://ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Create a new API key
4. Copy the key

## 📝 Step 2: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
```

Create `.env` file with the following content:

```env
# ChromaDB Configuration
CHROMA_API_KEY=your_chroma_api_key_here
CHROMA_TENANT=your_tenant_id_here
CHROMA_DATABASE=Mindful%20Eating%20Agent

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important:** Replace the placeholder values with your actual API keys!

## 🏗️ Step 3: Install Dependencies

### Windows

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/Mac

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ✅ Step 4: Test Your Setup

Run the ChromaDB connection test:

```bash
python test_chromadb.py
```

You should see:
```
✅ Successfully connected to ChromaDB!
✅ Heartbeat successful!
✅ All tests completed!
```

## 🎯 Step 5: Start the Application

### Option 1: Quick Start (Windows)

From the root directory:
```bash
start-fullstack.cmd
```

### Option 2: Manual Start

```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000`

## 🌟 Features

### 1. **Smart Food Recognition**
- Static database for common foods (instant lookup)
- ChromaDB cache for previously searched foods
- Gemini AI for unknown foods (learns and caches)

### 2. **Natural Language Processing**
- "I had 2 grilled chicken breasts"
- "ate a large pizza"
- "8oz salmon with rice"

### 3. **AI-Powered Recommendations**
- Personalized meal suggestions
- Pattern analysis
- Goal tracking

### 4. **Nutrition Tracking**
- Calories, protein, carbs, fat, fiber
- Daily and weekly summaries
- Calendar view

## 🔍 How It Works

### Food Lookup Flow

```
User Input: "I had sushi"
    ↓
1. Check Static Database (fast)
    ↓ (not found)
2. Check ChromaDB Cache (medium)
    ↓ (not found)
3. Ask Gemini AI (intelligent)
    ↓
4. Cache Result in ChromaDB
    ↓
5. Return Nutrition Data
```

### Example: Unknown Food

```
User: "I had a burrito bowl"
System: 🤖 Using Gemini AI to lookup: burrito bowl
Gemini: Returns nutrition data
System: ✅ Cached for future use
Result: Instant lookup next time!
```

## 📊 API Endpoints

### Health Check
```bash
GET /health
```

### Log Food
```bash
POST /api/log-food
{
  "food_text": "grilled chicken and rice",
  "meal_type": "lunch"
}
```

### Get Meal Suggestions (AI-Powered)
```bash
GET /api/meal-suggestions
```
Returns personalized meal suggestions based on your current nutrition and goals.

### Chat Interface
```bash
POST /api/chat
{
  "message": "I had pizza for lunch",
  "conversation_history": []
}
```

## 🛠️ Troubleshooting

### ChromaDB Connection Failed

**Error:** `Failed to initialize ChromaDB`

**Solution:**
1. Check your `.env` file exists in `backend/` directory
2. Verify API keys are correct (no extra spaces)
3. Test connection: `python test_chromadb.py`

### Gemini API Error

**Error:** `GEMINI_API_KEY not found`

**Solution:**
1. Add `GEMINI_API_KEY` to your `.env` file
2. Get a free key from [ai.google.dev](https://ai.google.dev)
3. Restart the application

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'chromadb'`

**Solution:**
```bash
pip install -r requirements.txt
```

## 🎨 UI Features

- **Chat Interface:** Natural conversation for food logging
- **Dashboard:** Daily nutrition overview
- **Calendar View:** Historical data visualization
- **Recommendations:** AI-powered suggestions

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secret
- The `.env` file is already in `.gitignore`

## 📈 Performance

- **Static DB:** < 1ms lookup
- **ChromaDB Cache:** ~10ms lookup
- **Gemini AI:** ~1-2s lookup (first time only)
- **Cached Foods:** Instant on subsequent lookups

## 🆘 Support

If you encounter issues:

1. Check the console output for error messages
2. Run `python test_chromadb.py` to verify connection
3. Ensure all API keys are correct in `.env`
4. Check that Python 3.8+ is installed

## 🎉 You're Ready!

Your AI Mindful Eating Agent is now set up with:
- ✅ ChromaDB cloud storage
- ✅ Gemini AI integration
- ✅ Smart nutrition caching
- ✅ Natural language processing

Start logging your meals and let AI help you reach your nutrition goals! 🥗💪
