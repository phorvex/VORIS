# VORIS Content Safety & Protection Systems

## Overview

VORIS includes comprehensive content safety measures to ensure respectful, professional interactions and prevent misuse of the system.

## 🛡️ Name Validation System

### Multi-Layer Protection

1. **Input Validation**
   - All user-provided names are validated before storage
   - Offensive content is rejected immediately with clear feedback
   - Users are prompted to provide an alternative, respectful name

2. **Storage Validation**
   - Memory is sanitized when loaded from disk
   - Any offensive content stored externally is automatically removed
   - System auto-corrects compromised memory files

3. **Display Validation**
   - Names are re-validated before being displayed in greetings
   - Offensive names are never shown to the user
   - System falls back to system username if stored name is invalid

### Protected Methods

- `is_name_acceptable(name)` - Centralized validation function
- `load_memory()` - Sanitizes on load
- `initialize()` - Validates before greeting
- `user_name_set` intent handler - Validates on input
- `user_identity` intent handler - Validates on display

### Validation Process

```python
1. Normalize input (lowercase, remove non-letters)
2. Check against comprehensive offensive word list
3. Reject if any pattern matches
4. Provide respectful feedback
5. Clear from memory if found
```

## 🚫 Blocked Content

The system blocks the following categories:

### Racial Slurs & Discrimination
- Comprehensive list of racial epithets and variations
- Covers multiple languages and leetspeak variations

### Profanity
- Strong profanity in multiple forms
- Common misspellings and variations

### Sexual Content
- Explicit sexual terms
- Inappropriate language

### Hate Speech
- Homophobic terms
- Derogatory language targeting any group

## ✅ How It Works

### Example 1: Rejection
```
> my name is [offensive term]
[VORIS]: I cannot accept that name. Please provide a different, respectful name.
[VORIS]: I'm designed to maintain a professional and respectful interaction.
```

### Example 2: Auto-Correction
If memory file is compromised:
```python
# On load, VORIS automatically:
1. Detects offensive content
2. Removes it from memory
3. Saves cleaned version
4. Continues normally
```

### Example 3: Safe Fallback
```
> who am i?
[VORIS]: Your system username is phorvex.
[VORIS]: If you'd like, you can tell me your preferred name...
```

## 🔧 Technical Implementation

### File Protections

**voris_advanced.py**
- `is_name_acceptable()` - 30+ offensive patterns checked
- Normalized comparison (case-insensitive, symbol-stripped)
- Applied at all interaction points

### Validation Points

1. **User Input** (line ~295)
   ```python
   if not self.is_name_acceptable(user_name):
       self.speak("I cannot accept that name...")
       return
   ```

2. **Memory Load** (line ~80)
   ```python
   if not self.is_name_acceptable(name):
       memory["user_preferences"]["name"] = ""
       self.save_memory_data(memory)
   ```

3. **Display** (line ~160, ~290)
   ```python
   if user_name and self.is_name_acceptable(user_name):
       # Show personalized greeting
   else:
       # Use system username
   ```

## 📋 Best Practices

### For Users
- Use your real name or a respectful nickname
- Avoid special characters in names (they're stripped anyway)
- VORIS will politely decline inappropriate names

### For Developers
- Always use `is_name_acceptable()` for any user-provided text
- Validate on input, storage, and display
- Provide clear, respectful feedback
- Never store offensive content

## 🔒 Privacy & Security

### What's Protected
- User-provided names and preferences
- Conversation history (sanitized)
- Custom commands (validated)

### What's Not Stored
- Offensive content (auto-removed)
- Sensitive system information
- Raw command outputs with personal data

## 🛠️ Maintenance

### Adding New Patterns
To add new offensive patterns to block:

```python
# In is_name_acceptable() method
offensive_patterns = [
    # ... existing patterns ...
    "newpattern",  # Add here
]
```

### Testing Protection
```bash
cd /run/media/phorvex/LLM/VORIS
python3 -c "
from voris_advanced import VorisAdvanced
v = VorisAdvanced(voice_enabled=False)
print(v.is_name_acceptable('John'))     # True
print(v.is_name_acceptable('[offensive]'))  # False
"
```

## 📊 Protection Status

- ✅ **Active**: Multi-layer validation enabled
- ✅ **Automatic**: No manual intervention needed
- ✅ **Comprehensive**: 30+ patterns blocked
- ✅ **Respectful**: Clear, professional feedback
- ✅ **Persistent**: Survives file modifications

## 🎯 Goals

1. **Respect** - Maintain professional interactions
2. **Safety** - Prevent misuse and offensive content
3. **Usability** - Don't interfere with normal use
4. **Transparency** - Clear feedback when content is blocked

## 📝 Change Log

### Version 1.0.0 (December 19, 2025)
- ✅ Implemented multi-layer name validation
- ✅ Added automatic memory sanitization
- ✅ Comprehensive offensive pattern list
- ✅ Validation at all interaction points
- ✅ Respectful rejection messages
- ✅ Auto-correction of compromised files

---

**VORIS is designed to be helpful, harmless, and honest.**  
Content safety is a core feature, not an afterthought.
