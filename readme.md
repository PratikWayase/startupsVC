#  AI Startup Guidance Tool

> An intelligent, AI-powered assistant that provides personalized guidance for startups across scaling, funding, team building, legal documents, and more.

Built with **Streamlit** and powered by **OpenRouter AI** (supporting GPT-4, Claude, Gemini, and more).

---


<img width="1897" height="924" alt="Screenshot 2025-11-09 114857" src="https://github.com/user-attachments/assets/94044094-99b1-4b0e-8ca7-7feb95ede6c2" />

##  Features

### Core Capabilities
-  **Multi-Model AI Support** - Choose from GPT-4o, Claude 3.5, Gemini Pro, and more
-  **Conversational Interface** - Context-aware follow-up questions
-  **Streaming Responses** - See guidance generate in real-time
-  **Dynamic Checklists** - Auto-generated, saveable action items
-  **Export Functionality** - Download guidance as Markdown or text
-  **Usage Analytics** - Track API calls and token usage
-  **Startup Profiles** - Save your startup info for personalized advice
-  **Conversation History** - Review and reference past queries

### Topic Coverage
1. **Scaling Business** - Growth strategies, infrastructure, processes
2. **Funding & Investment** - Fundraising, pitch decks, investor relations
3. **Team Setup & Hiring** - Recruitment, org design, culture building
4. **Legal Documents** - Formation docs, contracts, compliance
5. **Product Strategy** - MVP, roadmap, product-market fit
6. **Marketing & Growth** - Customer acquisition, channels, analytics
7. **General Advice** - Anything else startup-related

---

##  Installation

### Prerequisites
- Python 3.8+
- pip or conda
- OpenRouter API key ([Get one free](https://openrouter.ai/keys))

### Setup Steps

1. **Clone or Download the Files**
```bash
# Create a project directory
mkdir startup-guide-tool
cd startup-guide-tool
```

2. **Install Dependencies**
```bash
pip install streamlit requests
```

3. **Add the Files**
Place these files in your project directory:
- `app.py` (main application)
- `prompts.py` (prompt templates)
- `utils.py` (utility functions)
- `config.py` (configuration settings)

4. **Run the Application**
```bash
streamlit run app.py
```

5. **Get Your API Key**
- Visit [OpenRouter](https://openrouter.ai/keys)
- Sign up (free tier available)
- Generate an API key
- Enter it in the sidebar when prompted

---

## Usage Guide

### Quick Start

1. **Enter API Key**
   - Open the sidebar (top-left)
   - Paste your OpenRouter API key
   - Select your preferred AI model

2. **Choose a Topic**
   - Select from 7 specialized topics
   - Or use "General Advice" for anything else

3. **Ask Your Question**
   - Type your specific question
   - Click example questions for quick start
   - Be specific for better results

4. **Get Guidance**
   - Click " Get Guidance"
   - Watch response stream in real-time
   - Review actionable checklist
   - Export if needed

### Advanced Features

#### Startup Profile
Save your startup details once, get personalized advice forever:
```
- Industry: SaaS, Fintech, etc.
- Stage: Idea, MVP, Growth, etc.
- Team Size: Solo, 2-5, 6-10, etc.
```

#### Follow-Up Questions
- **Refine** - Get more detailed, specific advice
- **Simplify** - Condense to immediate action steps
- **Expand** - Deep dive with comprehensive insights

#### Action Checklists
- Auto-extracted from AI responses
- Track completion with checkboxes
- Progress indicator shows % complete
- Saved in session state

#### Export Options
- **Markdown** - Structured format with checklist
- **Text** - Plain text for easy sharing
- Includes timestamp and disclaimer

---

##  Example Queries

### Scaling Business
> "How do I scale my SaaS from 100 to 1,000 users while maintaining quality?"

### Funding & Investment
> "What should be in my seed round pitch deck? We're a fintech startup."

### Team Setup & Hiring
> "What should my first 5 hires be for an AI/ML startup?"

### Legal Documents
> "What documents do I need to incorporate in Delaware as a C-Corp?"

### Product Strategy
> "How do I validate product-market fit for a B2B SaaS tool?"

### Marketing & Growth
> "Best customer acquisition channels for a $50/month B2B SaaS?"

---



### Model Selection
Choose based on your needs:

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| **GPT-4o Mini** | ⚡⚡⚡ | 💰 | ⭐⭐⭐ | General queries, fast responses |
| **GPT-4o** | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐⭐ | Complex analysis, high quality |
| **Claude 3.5 Sonnet** | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐⭐ | Technical content, detailed analysis |
| **Gemini Pro** | ⚡⚡⚡ | 💰 | ⭐⭐⭐ | Quick advice, cost-effective |

### Response Settings
- **Max Tokens**: 500-3000 (longer = more detail)
- **Streaming**: On for real-time, Off for complete response
- **Context**: Include conversation history for follow-ups

---

##  Usage Statistics

Track your usage in the sidebar:
- **API Calls** - Total requests made
- **Tokens Used** - Approximate token consumption
- **Conversation History** - Review past queries

---

## 🐛 Troubleshooting

### Common Issues

**"Invalid API Key"**
- Verify key from [OpenRouter](https://openrouter.ai/keys)
- Check for extra spaces or characters
- Ensure key starts with `sk-or-v1-`

**"Rate Limit Reached"**
- Wait 1-2 minutes
- Free tier has usage limits
- Consider upgrading plan

**"Network Error"**
- Check internet connection
- Verify OpenRouter API is accessible
- Try different model

**"Response Cut Off"**
- Increase max_tokens in settings
- Try shorter, more focused query
- Use "Expand" button for more detail

**"No Checklist Generated"**
- Response might not contain actionable items
- Try asking for "step-by-step guide"
- Use "Refine" to get structured output

---

## Security & Privacy

- **API Keys**: Stored only in session, never saved to disk
- **Conversations**: Kept in browser memory, cleared on refresh
- **No Data Logging**: Your queries aren't stored on our servers
- **OpenRouter Privacy**: Check [OpenRouter's privacy policy](https://openrouter.ai/privacy)

---

##  Pro Tips

1. **Be Specific**: "Scale my e-commerce site from 100 to 1000 users" > "Help me scale"
2. **Use Profile**: Fill out startup profile for personalized advice
3. **Ask Follow-Ups**: Use Refine/Simplify/Expand for better responses
4. **Export Everything**: Save good advice for future reference
5. **Try Different Models**: GPT-4o for quality, GPT-4o-mini for speed
6. **Checklist Progress**: Track your action items over time
7. **Conversation Context**: Enable context for multi-turn discussions

---


### Planned Features
- [ ] PDF generation for reports
- [ ] Document upload and analysis
- [ ] Multi-language support
- [ ] Resource library with templates
- [ ] Collaborative features (team sharing)
- [ ] Financial modeling calculators
- [ ] Competitor analysis with web search
- [ ] Integration with project management tools

---

## 🤝 Contributing

Found a bug? Have a feature request? Want to contribute?

1. **Report Issues**: Describe the problem clearly
2. **Suggest Features**: Explain the use case
3. **Submit PRs**: Follow code style, add tests

---

## 📄 License

This project is open-source. Feel free to use, modify, and distribute.

**Attribution**: Built by SitaRaman

---

## 🙏 Acknowledgments

- **OpenRouter** - Multi-model API access
- **Streamlit** - Web app framework
- **OpenAI, Anthropic, Google** - AI models
- **Startup Community** - Feedback and testing

---



---

## 🌟 Show Your Support

If this tool helped you, please:
- ⭐ Star the repository
- 🐦 Share on social media
- 📝 Write a review
- 💡 Suggest improvements

---

**Made with ❤️ for the Startup Community**

*Last Updated: November 2025*
