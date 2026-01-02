# Ollama LLM Integration for VORIS

VORIS now includes optional integration with **Ollama** for enhanced natural language understanding using local Large Language Models.

## What is Ollama?

Ollama allows you to run powerful LLMs (like Llama, Mistral, etc.) locally on your machine, giving VORIS much better conversational abilities and understanding.

## Features

With Ollama enabled, VORIS can:
- Understand conversational questions better
- Handle corrections and informal statements ("that's not true", "you're wrong")
- Answer complex questions intelligently
- Provide context-aware responses
- Handle typos and misspellings better
- Respond naturally to follow-up questions

## Installation

### 1. Install Ollama

```bash
# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from: https://ollama.ai
```

### 2. Pull a Model

```bash
# Recommended: Llama 3.2 (lightweight and fast)
ollama pull llama3.2

# Or other models:
ollama pull llama3.1      # Larger, more powerful
ollama pull mistral       # Alternative model
ollama pull phi3          # Very lightweight
```

### 3. Start Ollama Service

```bash
# Ollama usually starts automatically after installation
# To manually start:
ollama serve
```

### 4. Verify Installation

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags
```

## Configuration

VORIS will automatically detect if Ollama is available when it starts.

You can customize Ollama settings in `~/.voris/config.json`:

```json
{
  "ollama_url": "http://localhost:11434",
  "ollama_model": "llama3.2:latest",
  "ollama_temperature": 0.7,
  "ollama_max_tokens": 500
}
```

### Available Settings

- **ollama_url**: URL where Ollama is running (default: `http://localhost:11434`)
- **ollama_model**: Which model to use (default: `llama3.2:latest`)
- **ollama_temperature**: Creativity level 0-1 (default: `0.7`)
- **ollama_max_tokens**: Maximum response length (default: `500`)

## Usage

Once Ollama is installed and running, VORIS will automatically use it when:

1. **Unknown commands**: Questions or statements that don't match built-in commands
2. **Conversational queries**: "that's not true", "explain that", "what do you think"
3. **Complex questions**: Multi-part questions or follow-ups

### Example Interactions

```
> what is your name
[VORIS]: I am VORIS - Voice Operated Responsive Intelligence System.

> your brain is still not connecting right
[VORIS]: I apologize if I'm not understanding you correctly. I'm designed to...

> that's not true
[VORIS]: You're right, let me clarify...

> has donald trump ever been convicted of a crime?
[VORIS]: Based on public information, Donald Trump was convicted in May 2024...
```

## Switching Models

To use a different model:

```bash
# List available models
ollama list

# Pull a new model
ollama pull mistral

# Tell VORIS to use it by editing ~/.voris/config.json
# Or use a future command (to be implemented)
```

## Troubleshooting

### VORIS doesn't detect Ollama

1. Check if Ollama is running:
   ```bash
   systemctl status ollama
   # or
   ps aux | grep ollama
   ```

2. Test Ollama directly:
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. Restart VORIS after starting Ollama

### Slow responses

- Use a smaller model like `llama3.2` or `phi3`
- Reduce `ollama_max_tokens` in config
- Ensure your system has enough RAM (8GB+ recommended)

### Model not found

```bash
# Pull the model first
ollama pull llama3.2
```

## Performance Tips

- **Best balance**: `llama3.2` (fast, good quality)
- **Fastest**: `phi3` or `tinyllama` (lightweight but less capable)
- **Best quality**: `llama3.1` or `mixtral` (slower, needs more resources)

## System Requirements

- **RAM**: 
  - Minimum 4GB for small models
  - 8GB+ recommended for llama3.2
  - 16GB+ for larger models
- **Storage**: 2-8GB per model
- **CPU**: Any modern processor (GPU acceleration optional)

## Disabling Ollama

If you don't want to use Ollama, simply don't install it or stop the service:

```bash
sudo systemctl stop ollama
```

VORIS will gracefully fall back to its built-in NLP engine.

## Future Enhancements

Planned features:
- Runtime model switching via voice command
- Conversation history and context
- Fine-tuning with user preferences
- Integration with more LLM backends

## Learn More

- Ollama Website: https://ollama.ai
- Available Models: https://ollama.ai/library
- VORIS Documentation: See README.md
