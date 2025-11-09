"""
Configuration settings for Startup Guide Tool
"""

class Config:
    """Application configuration"""
    
    # API Settings
    DEFAULT_MODEL = "openai/gpt-4o-mini"
    AVAILABLE_MODELS = [
        "openai/gpt-4o-mini",
        "openai/gpt-4o",
        "anthropic/claude-3-5-sonnet",
        "google/gemini-pro",
        "meta-llama/llama-3-70b-instruct"
    ]
    
    # Token Limits
    DEFAULT_MAX_TOKENS = 2000
    MIN_MAX_TOKENS = 500
    MAX_MAX_TOKENS = 4000
    
    # Response Settings
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_TOP_P = 0.9
    ENABLE_STREAMING = True
    
    # Conversation Settings
    MAX_CONVERSATION_HISTORY = 20  # Store last 20 messages
    CONTEXT_WINDOW_SIZE = 6  # Use last 6 messages for context
    
    # UI Settings
    TOPICS = {
        " Scaling Business": "scaling",
        " Funding & Investment": "funding",
        " Team Setup & Hiring": "team",
        " Legal Documents": "documents",
        " Product Strategy": "product",
        " Marketing & Growth": "marketing",
        " General Advice": "general"
    }
    
    # Export Settings
    EXPORT_FORMATS = ["markdown", "text", "json"]
    
    # Rate Limiting (Client-side tracking)
    RATE_LIMIT_REQUESTS = 50  # Max requests per session
    RATE_LIMIT_WARNING_THRESHOLD = 40
    
    # Cache Settings
    ENABLE_CACHE = True
    CACHE_TTL_SECONDS = 3600  # 1 hour
    
    # Startup Profile Fields
    INDUSTRIES = [
        "SaaS",
        "E-commerce",
        "Fintech",
        "Healthcare",
        "EdTech",
        "AI/ML",
        "Gaming",
        "Social Media",
        "Marketplace",
        "Developer Tools",
        "Other"
    ]
    
    STAGES = [
        "Idea",
        "MVP",
        "Early Stage",
        "Growth",
        "Scale-up",
        "Established"
    ]
    
    TEAM_SIZES = [
        "Solo Founder",
        "2-5",
        "6-10",
        "11-25",
        "26-50",
        "50+"
    ]
    
    # Feature Flags
    FEATURES = {
        "streaming": True,
        "conversation_history": True,
        "export": True,
        "checklists": True,
        "startup_profile": True,
        "usage_stats": True,
        "follow_up_suggestions": True,
        "quality_scoring": False  # Beta feature
    }
    
    # Error Messages
    ERROR_MESSAGES = {
        "no_api_key": " Please provide an OpenRouter API key in the sidebar.",
        "invalid_api_key": " Invalid API key format. Please check your key.",
        "empty_query": " Please enter a question to get guidance.",
        "api_error": " Error calling API. Please try again.",
        "rate_limit": " Rate limit reached. Please wait a moment.",
        "network_error": " Network error. Please check your connection."
    }
    
    # Success Messages
    SUCCESS_MESSAGES = {
        "profile_saved": " Profile saved successfully!",
        "history_cleared": " History cleared successfully!",
        "exported": " Exported successfully!"
    }
    
    # Help Text
    HELP_TEXT = {
        "api_key": "Get your API key from https://openrouter.ai/keys",
        "model_selection": "Choose the AI model. GPT-4o-mini is fast and cost-effective.",
        "streaming": "Show responses as they're generated for better UX",
        "max_tokens": "Longer responses use more tokens (and cost more)",
        "context": "Include previous messages for context-aware responses"
    }
    
    # Resources and Links
    RESOURCES = {
        "openrouter_docs": "https://openrouter.ai/docs",
        "openrouter_keys": "https://openrouter.ai/keys",
        "openrouter_models": "https://openrouter.ai/models",
        "yc_library": "https://www.ycombinator.com/library",
        "stripe_atlas": "https://stripe.com/atlas",
        "crunchbase": "https://www.crunchbase.com",
        "angellist": "https://www.angellist.com"
    }
    
    # Disclaimer
    DISCLAIMER = """
    💡 **Disclaimer**: This is AI-generated general advice. 
    Always consult with legal, financial, or domain experts for critical business decisions.
    """
    
    # Footer
    FOOTER = """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Built with ❤️ by SitaRaman | Powered by OpenRouter AI</p>
        <p style='font-size: 0.8rem;'>🌟 Star this project | 📧 Contact for feedback</p>
    </div>
    """
    
    @classmethod
    def get_model_info(cls, model: str) -> dict:
        """Get information about a specific model"""
        model_info = {
            "openai/gpt-4o-mini": {
                "name": "GPT-4o Mini",
                "provider": "OpenAI",
                "speed": "Fast",
                "cost": "Low",
                "quality": "Good",
                "best_for": "General queries, cost-effective"
            },
            "openai/gpt-4o": {
                "name": "GPT-4o",
                "provider": "OpenAI",
                "speed": "Medium",
                "cost": "Medium",
                "quality": "Excellent",
                "best_for": "Complex analysis, high-quality responses"
            },
            "anthropic/claude-3-5-sonnet": {
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "speed": "Medium",
                "cost": "Medium",
                "quality": "Excellent",
                "best_for": "Detailed analysis, technical content"
            },
            "google/gemini-pro": {
                "name": "Gemini Pro",
                "provider": "Google",
                "speed": "Fast",
                "cost": "Low",
                "quality": "Good",
                "best_for": "Quick responses, general advice"
            }
        }
        return model_info.get(model, {})
    
    @classmethod
    def estimate_cost(cls, model: str, tokens: int) -> float:
        """Estimate cost for API call"""
        # Rough cost estimates per 1K tokens (input + output combined average)
        costs_per_1k = {
            "openai/gpt-4o-mini": 0.0002,
            "openai/gpt-4o": 0.005,
            "anthropic/claude-3-5-sonnet": 0.004,
            "google/gemini-pro": 0.0001
        }
        
        cost_per_1k = costs_per_1k.get(model, 0.001)
        return (tokens / 1000) * cost_per_1k
    
    @classmethod
    def get_topic_color(cls, topic: str) -> str:
        """Get color scheme for topic"""
        colors = {
            "scaling": "#667eea",
            "funding": "#f093fb",
            "team": "#4facfe",
            "documents": "#43e97b",
            "product": "#fa709a",
            "marketing": "#feca57",
            "general": "#a29bfe"
        }
        return colors.get(topic, "#667eea")
    
    @classmethod
    def get_icon_for_topic(cls, topic: str) -> str:
        """Get emoji icon for topic"""
        icons = {
            "scaling": "",
            "funding": "",
            "team": "",
            "documents": "",
            "product": "",
            "marketing": "",
            "general": ""
        }
        return icons.get(topic, "")