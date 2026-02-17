#!/bin/bash

# Load from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ Loaded configuration from .env"
    echo "Provider: $OPENAI_BASE_URL"
    echo "Model:    $OPENAI_MODEL_NAME"
    echo "---------------------------------------------------------"
    python3 investment_committee.py
    exit 0
fi

echo "🚀 Starting Investment Committee Agent Configuration..."
echo "---------------------------------------------------------"
echo "Select your AI Provider:"
echo "1) OpenAI (Paid, Requires API Key)"
echo "2) Groq (Free/Fast, Requires Free API Key)"
echo "3) Ollama (Local/Free, Requires 'ollama serve' running)"
echo "4) Google Gemini (Free Tier Available)"
echo "5) GitHub Models (Free, Requires GitHub Token)"
echo "6) Custom (Enter your own Base URL)"
read -p "Choose [1-6]: " choice

case $choice in
    1)
        echo "Using OpenAI (Official)"
        export OPENAI_BASE_URL="https://api.openai.com/v1"
        export OPENAI_MODEL_NAME="gpt-4o"
        read -p "Enter your OpenAI API Key (sk-...): " key
        export OPENAI_API_KEY=$key
        ;;
    2)
        echo "Using Groq (Free & Fast)"
        export OPENAI_BASE_URL="https://api.groq.com/openai/v1"
        # Using Llama 3 70B as it's smart enough for investment analysis
        export OPENAI_MODEL_NAME="llama3-70b-8192" 
        echo "Get a free key at: https://console.groq.com/keys"
        read -p "Enter your Groq API Key (gsk-...): " key
        export OPENAI_API_KEY=$key
        ;;
    3)
        echo "Using Ollama (Local)"
        export OPENAI_BASE_URL="http://localhost:11434/v1"
        export OPENAI_API_KEY="ollama" # Fake key required
        echo "Make sure you have run 'ollama pull llama3' or similar."
        read -p "Enter model name (default: llama3): " model
        export OPENAI_MODEL_NAME=${model:-llama3}
        ;;
    4)
        echo "Using Google Gemini (via OpenAI Compatibility)"
        # Use v1beta endpoint for chat completions compatibility
        export OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/"
        # Gemini API expects just the model name for OpenAI compatibility endpoint
        export OPENAI_MODEL_NAME="gemini-1.5-flash"
        echo "Get a free key at: https://aistudio.google.com/"
        read -p "Enter your Google AI Studio API Key: " key
        export OPENAI_API_KEY=$key
        ;;
    5)
        echo "Using GitHub Models (Free via Azure AI)"
        export OPENAI_BASE_URL="https://models.inference.ai.azure.com"
        export OPENAI_MODEL_NAME="gpt-4o"
        echo "Get a token at: https://github.com/settings/tokens (Select 'Fine-grained' -> No permissions needed, just public access)"
        read -p "Enter your GitHub PAT (github_pat_...): " key
        export OPENAI_API_KEY=$key
        ;;
    6)
        read -p "Enter Base URL (e.g. https://api.deepseek.com/v1): " base_url
        export OPENAI_BASE_URL=$base_url
        read -p "Enter API Key: " key
        export OPENAI_API_KEY=$key
        read -p "Enter Model Name: " model
        export OPENAI_MODEL_NAME=$model
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo "---------------------------------------------------------"
echo "✅ Configuration Set!"
echo "Provider: $OPENAI_BASE_URL"
echo "Model:    $OPENAI_MODEL_NAME"
echo "---------------------------------------------------------"

python3 investment_committee.py
