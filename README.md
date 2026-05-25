<div align="center">

# ✦ Postly

### AI-Powered LinkedIn Post Generator

*Empowering influencers and professionals to create high-quality LinkedIn content at scale — in seconds, not hours.*

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com)
[![Groq](https://img.shields.io/badge/Groq_LLM-000000?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

[Live Demo](https://postly-duo3.onrender.com) · [Report Bug](https://github.com/itsDharan/Postly/issues) · [Request Feature](https://github.com/itsDharan/Postly/issues)

</div>

---

## 📌 The Problem

LinkedIn has become the **#1 platform for professional branding**, with over **1 billion users** and **9 billion content impressions per week**. In today's corporate landscape:

- **93% of B2B marketers** use LinkedIn for content marketing
- **Influencers and thought leaders** are expected to post **3-5 times per week** to stay relevant
- **Corporate teams** rely on employee advocacy and influencer partnerships to drive brand reach
- Yet, **creating high-quality, on-brand content consistently is time-consuming and expensive**

Professionals spend **30-60 minutes per post** researching, writing, and refining content — often resulting in inconsistent tone, missed posting schedules, and burnout.

---

## 💡 What Postly Solves

**Postly eliminates the content creation bottleneck** by using AI to generate LinkedIn posts that match a specific influencer's writing style, tone, and topics — in under 10 seconds.

| Without Postly | With Postly |
|:---:|:---:|
| 30-60 min per post | **~10 seconds** per post |
| Inconsistent tone across posts | **Style-matched** to influencer voice |
| Single language only | **6 languages** including Hinglish |
| Manual research for topics | **AI-powered** topic suggestions |
| No version control | **Edit, regenerate, and iterate** |

### How It Works

```
1. Select Influencer Style  →  Choose whose writing voice to emulate
2. Pick Topic + Length       →  Configure post parameters
3. Generate                  →  AI creates a post matching the influencer's style
4. Edit & Publish            →  Refine and post directly to LinkedIn
```

The system uses **few-shot learning** — it analyzes real posts from each influencer to understand their:
- Writing patterns and sentence structure
- Preferred hashtag usage
- Topic expertise and vocabulary
- Tone (motivational, technical, storytelling, etc.)

---

## 🏢 How the Influencer System Works in Modern Corporate Settings

### The Influencer Economy Today

The influencer marketing industry is projected to reach **$32.55 billion by 2025**. On LinkedIn specifically:

```
┌─────────────────────────────────────────────────────┐
│           Corporate Influencer Ecosystem             │
├─────────────────────────────────────────────────────┤
│                                                      │
│   Brand/Company                                      │
│       │                                              │
│       ├── Internal Thought Leaders (C-Suite, VPs)    │
│       ├── Employee Advocates (Team members)          │
│       └── External Influencer Partners               │
│               │                                      │
│               ├── Industry Experts                   │
│               ├── Niche Content Creators             │
│               └── Community Builders                 │
│                                                      │
│   All need: Consistent, on-brand, high-quality       │
│   content at scale                                   │
└─────────────────────────────────────────────────────┘
```

### How Postly Fits In

| Corporate Need | Postly's Solution |
|---|---|
| **Employee Advocacy Programs** | Generate on-brand posts for team members to share |
| **Thought Leadership** | Maintain consistent posting for executives with packed schedules |
| **Multi-market Reach** | Generate posts in 6 languages from a single prompt |
| **Brand Consistency** | AI learns each influencer's unique voice — no generic content |
| **Content Velocity** | Scale from 2 posts/week to 20+ without additional headcount |

---

## 🏗️ Architecture & Scalability

### System Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Frontend   │     │   Backend    │     │   Data Layer     │
│  (Streamlit) │────▶│  (Python)    │────▶│  (MongoDB Atlas) │
│              │     │              │     │                  │
│  • Login/    │     │  • Auth      │     │  • User profiles │
│    Register  │     │  • Few-shot  │     │  • Post datasets │
│  • Post UI   │     │    learning  │     │  • Influencer    │
│  • Edit/     │     │  • Post      │     │    metadata      │
│    Regenerate│     │    generation│     │                  │
└──────────────┘     └──────┬───────┘     └──────────────────┘
                            │
                     ┌──────▼───────┐
                     │   Groq LLM   │
                     │  (Llama 3.3  │
                     │   70B)       │
                     │              │
                     │  • Content   │
                     │    generation│
                     │  • Style     │
                     │    matching  │
                     └──────────────┘
```

### Scalability Design

| Dimension | Current | Scalable To |
|---|---|---|
| **Influencers** | 3 profiles | Unlimited — add JSON dataset + DB entry |
| **Languages** | 6 supported | Any language the LLM supports |
| **Users** | Multi-user auth | Thousands (MongoDB Atlas scales automatically) |
| **Posts/Dataset** | 150 per influencer | Thousands — more data = better style matching |
| **LLM Provider** | Groq (Llama 3.3 70B) | Swappable — OpenAI, Anthropic, local models |
| **Deployment** | Render (Free) | Any cloud — AWS, GCP, Azure, Docker |

### Adding a New Influencer (3 Steps)

```python
# 1. Prepare their LinkedIn posts as JSON
# Data/NewInfluencer_Data.json
[
  {"text": "Post content...", "line_count": 5, "language": "English", "tags": ["AI", "Tech"]},
  ...
]

# 2. Add to seed.py DATASET_MAP
DATASET_MAP = {
    "Data/NewInfluencer_Data.json": "new_influencer_data",
}

# 3. Add to auth.py INFLUENCERS dict
INFLUENCERS = {
    "New Influencer": "new_influencer_username",
}
```

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|---|---|---|
| **Frontend** | Streamlit | Rapid UI with Python, real-time interactivity |
| **LLM** | Groq (Llama 3.3 70B) | Ultra-fast inference (~200 tokens/sec) |
| **Database** | MongoDB Atlas | Flexible document store, free tier, cloud-native |
| **Auth** | passlib (PBKDF2-SHA256) | Industry-standard password hashing |
| **Deployment** | Render | Free tier, auto-deploy from GitHub |
| **AI Framework** | LangChain | Prompt engineering and LLM orchestration |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Groq API Key](https://console.groq.com) (free)
- [MongoDB Atlas](https://www.mongodb.com/atlas) cluster (free M0 tier)

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/itsDharan/Postly.git
cd Postly

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo GROQ_API_KEY=your_groq_api_key > .env
echo MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true >> .env

# 4. Seed the database
python seed.py

# 5. Run the app
streamlit run main.py
```

### Deploy to Render

1. Push code to GitHub
2. Create a **Web Service** on [Render](https://render.com)
3. Set environment variables: `GROQ_API_KEY`, `MONGO_URI`
4. Build: `pip install -r requirements.txt`
5. Start: `streamlit run main.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

---

## 📂 Project Structure

```
Postly/
├── main.py              # Streamlit app — UI, routing, and page logic
├── auth.py              # User authentication and MongoDB connection
├── few_shot.py          # Few-shot learning — loads and filters influencer posts
├── post_generator.py    # Prompt engineering and LLM-powered post generation
├── LLM_helper.py        # Groq LLM client configuration
├── preprocess.py        # Data preprocessing — extracts metadata from raw posts
├── seed.py              # Database seeding script for MongoDB Atlas
├── Data/
│   ├── Murli_Data.json      # Influencer 1 post dataset (150 posts)
│   ├── Khushbu_data.json    # Influencer 2 post dataset (150 posts)
│   └── Adil_Data.json       # Influencer 3 post dataset (10 posts)
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment blueprint
├── .python-version      # Python version pin for Render
└── .gitignore           # Git ignore rules
```

---

## ✨ Key Features

- 🔐 **Secure Authentication** — User registration and login with hashed passwords
- 🎭 **Multi-Influencer Styles** — Switch between different influencer writing voices
- 🌍 **6 Languages** — English, Hinglish, French, Spanish, Chinese, Russian
- 📏 **Adjustable Length** — Short (1-5 lines), Medium (6-10), Long (11-15)
- ✏️ **Edit & Regenerate** — Refine AI-generated posts before publishing
- 🔗 **Direct LinkedIn Integration** — One-click open to LinkedIn for posting
- 🎨 **Premium Dark UI** — Glassmorphism design with 3D animations

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Murli Dharan**

- GitHub: [@itsDharan](https://github.com/itsDharan)

---

<div align="center">

*Built with ❤️ using Streamlit, Groq, and MongoDB Atlas*

</div>
