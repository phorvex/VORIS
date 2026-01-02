# Managing Ollama with VORIS

## Problem: Ollama Timeouts

If you're experiencing timeout errors with Ollama, here are your options:

### Option 1: Disable Ollama (Fastest Fix)

Create or edit `~/.voris/config.json`:

```json
{
  "ollama_enabled": false
}
```

VORIS will work perfectly fine without Ollama, using its built-in NLP.

### Option 2: Increase Timeout

If you want to keep Ollama but it's slow, increase the timeout:

```json
{
  "ollama_enabled": true,
  "ollama_timeout": 120
}
```

### Option 3: Use a Faster Model

The phi3 model may be too resource-intensive. Try these lighter models:

```bash
# Very lightweight and fast
ollama pull tinyllama

# Better quality but still fast
ollama pull llama3.2
```

Then update config:

```json
{
  "ollama_model": "tinyllama:latest"
}
```

### Option 4: Stop Ollama Service

If you don't want Ollama running at all:

```bash
# Stop the service
sudo systemctl stop ollama

# Disable on boot
sudo systemctl disable ollama
```

## Current Recommended Configuration

For your system (4GB RAM, 4 cores), I recommend:

```json
{
  "ollama_enabled": false
}
```

Or if you want to try LLM features:

```bash
# Pull lightweight model
ollama pull tinyllama

# Edit config
nano ~/.voris/config.json
```

```json
{
  "ollama_enabled": true,
  "ollama_model": "tinyllama:latest",
  "ollama_timeout": 30,
  "ollama_max_tokens": 200
}
```

## Performance Comparison

| Model | RAM Usage | Speed | Quality |
|-------|-----------|-------|---------|
| phi3 | 3-4GB | Slow | Good |
| tinyllama | 1GB | Fast | Basic |
| llama3.2 | 2-3GB | Medium | Best |

## Testing Your Configuration

After changing config, test with:

```bash
python3 check_ollama.py
```

Or just run VORIS and try a question:

```bash
python3 voris_advanced.py

> what is your favorite color
```

If it responds without errors/timeouts, you're good!

## Troubleshooting

**"Read timed out" errors:**
- Increase `ollama_timeout` or disable Ollama
- Use a lighter model
- Check system resources: `htop`

**Ollama using too much RAM:**
- Stop Ollama: `sudo systemctl stop ollama`
- Or disable in config: `"ollama_enabled": false`

**Want debugging info:**
```json
{
  "ollama_debug": true
}
```

## Quick Commands

```bash
# Check Ollama status
systemctl status ollama

# List installed models
ollama list

# Stop Ollama
sudo systemctl stop ollama

# Start Ollama
sudo systemctl start ollama

# Check resource usage
htop
# (Look for 'ollama' processes)
```

## My Recommendation

Since phi3 is timing out on your system, I suggest:

**Best approach:** Disable Ollama for now
```bash
mkdir -p ~/.voris
cat > ~/.voris/config.json << 'EOF'
{
  "ollama_enabled": false
}
EOF
```

VORIS will work great without it! The built-in NLP handles most commands well.

If you later want to try LLM features:
1. Install a lighter model: `ollama pull tinyllama`
2. Enable in config with higher timeout
3. Test with simple questions first

---

**Note:** With Ollama disabled, you won't see debug errors and VORIS will respond instantly to all commands using its built-in intelligence.
