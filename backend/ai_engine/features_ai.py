# =========================================
# FEATURES AI ENGINE - 100% FREE FOREVER
# Uses flan-t5-small (runs locally, offline)
# No API key, no credits, no limits
# First run downloads model (~300MB), then offline forever
# =========================================

print("Loading local AI model...")

model = None
tokenizer = None

try:
    from transformers import T5ForConditionalGeneration, T5Tokenizer
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
    print("LOCAL AI MODEL LOADED: flan-t5-small (FREE FOREVER)")
except Exception as e:
    print(f"Could not load AI model: {e}")
    print("Install with: pip install transformers sentencepiece torch")


def ask_local_ai(prompt, max_tokens=250):
    """Run AI locally - FREE, no API needed"""
    if model and tokenizer:
        try:
            inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = model.generate(**inputs, max_new_tokens=max_tokens, do_sample=True, temperature=0.7, top_p=0.9)
            return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        except Exception as e:
            print(f"AI Error: {e}")
    return None


# =========================================
# 1. MAKE NOTES
# =========================================
def make_notes_ai(text):
    if not text.strip():
        return "No content to convert into notes."

    result = ask_local_ai(f"Make bullet point study notes from this text: {text}", max_tokens=300)
    if result and len(result) > 10:
        # Format as bullet points if not already
        if "*" not in result and "-" not in result:
            lines = result.split(". ")
            result = "\n".join("* " + l.strip().capitalize() for l in lines if l.strip())
        return result

    # Fallback
    sentences = text.replace("\n", " ").split(".")
    notes = []
    for s in sentences:
        s = s.strip()
        if s and len(s) > 5:
            notes.append("* " + s.capitalize())
    return "\n".join(notes) if notes else "Could not generate notes."


# =========================================
# 2. IMPROVE ASSIGNMENT
# =========================================
def improve_assignment_ai(text):
    if not text.strip():
        return "No content provided."

    result = ask_local_ai(f"Rewrite this text with better grammar and vocabulary: {text}", max_tokens=400)
    if result and len(result) > 10:
        return result

    try:
        import language_tool_python
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        return language_tool_python.utils.correct(text, matches)
    except:
        return text


# =========================================
# 3. SIMPLIFY TEXT
# =========================================
def simplify_ai(text):
    if not text.strip():
        return "No content provided."

    result = ask_local_ai(f"Simplify this text using easy words: {text}", max_tokens=300)
    if result and len(result) > 10:
        return result

    sentences = text.split(".")
    return ". ".join(s.strip().capitalize() for s in sentences if s.strip()) + "."


# =========================================
# 4. EXPAND TEXT
# =========================================
def expand_ai(text):
    if not text.strip():
        return "No content provided."

    result = ask_local_ai(f"Expand this text with more details and examples: {text}", max_tokens=500)
    if result and len(result) > len(text):
        return result

    expanded = text.strip()
    if not expanded.endswith("."):
        expanded += "."
    expanded += " This concept is important and deserves further explanation."
    expanded += " Understanding this topic builds a stronger foundation for learning."
    expanded += " By exploring the details, we gain deeper insights into the subject."
    return expanded


# =========================================
# 5. PARAGRAPH BUILDER
# =========================================
def paragraph_ai(text):
    if not text.strip():
        return "No topic provided."

    result = ask_local_ai(f"Write a detailed paragraph about: {text}", max_tokens=400)
    if result and len(result) > 20:
        return result

    topic = text.strip().capitalize().rstrip(".")
    return (
        f"{topic} is an important subject that has gained significant attention. "
        f"It involves various aspects essential for understanding the broader context. "
        f"Students and professionals can benefit from studying {text.strip().lower()} in depth. "
        f"The key concepts include understanding the fundamentals and applying them effectively. "
        f"By gaining knowledge in this area, one can develop better skills and insights. "
        f"Overall, {text.strip().lower()} plays a crucial role in academic and professional development."
    )
