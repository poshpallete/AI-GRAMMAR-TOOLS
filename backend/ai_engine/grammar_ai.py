# =========================================
# GRAMMAR AI ENGINE - FREE OFFLINE
# Uses language_tool_python (no API key needed)
# =========================================

import html

import language_tool_python

tool = language_tool_python.LanguageTool('en-US')


def grammar_engine(text):
    if not text or text.strip() == "":
        return "", "", [], "", "", "", []

    try:
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)

        errors = []
        candidates = []

        for match in matches:
            start = match.offset

            # Handle BOTH old and new versions of language_tool_python
            try:
                length = match.errorLength
            except AttributeError:
                try:
                    length = match.error_length
                except AttributeError:
                    length = match.errorlength if hasattr(match, 'errorlength') else len(match.context) if hasattr(match, 'context') else 1

            end = start + length
            wrong_text = text[start:end]
            if not wrong_text.strip():
                continue
            candidates.append((start, end, match.message))

        highlighted_parts = []
        cursor = 0
        for start, end, message in sorted(candidates, key=lambda item: (item[0], item[1])):
            if start < cursor or start >= len(text):
                continue
            end = min(end, len(text))
            highlighted_parts.append(html.escape(text[cursor:start]))
            highlighted_parts.append(
                "<span style='color:#ff4444; text-decoration:underline; font-weight:bold;'>"
                + html.escape(text[start:end])
                + "</span>"
            )
            errors.append(message)
            cursor = end
        highlighted_parts.append(html.escape(text[cursor:]))
        highlighted = "".join(highlighted_parts)

        # Good version = just corrected
        good_sentence = corrected

        # Better version = corrected + properly capitalized
        sentences = corrected.split(". ")
        better_parts = []
        for s in sentences:
            s = s.strip()
            if s:
                better_parts.append(s[0].upper() + s[1:] if len(s) > 1 else s.upper())
        better_sentence = ". ".join(better_parts)
        if better_sentence and not better_sentence.endswith("."):
            better_sentence += "."

        # Best version = same as better (offline mode)
        best_sentence = better_sentence

        # Suggestions
        suggestions = []
        error_lower = " ".join(e.lower() for e in errors)
        if "tense" in error_lower:
            suggestions.append("Be consistent with verb tenses throughout your writing.")
        if "agreement" in error_lower or "subject" in error_lower:
            suggestions.append("Ensure subject-verb agreement in all sentences.")
        if "spelling" in error_lower or "misspell" in error_lower:
            suggestions.append("Double-check spelling of commonly confused words.")
        if "comma" in error_lower or "punctuation" in error_lower:
            suggestions.append("Review punctuation rules, especially comma usage.")
        if len(errors) > 5:
            suggestions.append("Consider breaking long sentences into shorter, clearer ones.")
        if len(errors) == 0:
            suggestions.append("Great writing! No grammar errors detected.")
        if not suggestions:
            suggestions.append("Review basic grammar rules to improve your writing.")
            suggestions.append("Read more to naturally improve vocabulary and sentence structure.")

        return corrected, highlighted, errors, good_sentence, better_sentence, best_sentence, suggestions

    except Exception as e:
        print("ERROR in grammar_engine:", e)
        return text, html.escape(text), [str(e)], text, text, text, ["An error occurred during analysis."]
