# Human Essays Needed for Evaluation

## Status
🔴 **INCOMPLETE** - Awaiting 10 human-written essays

Current dataset:
- ✅ 10 AI-generated essays (complete)
- ❌ 10 human-written essays (needed)

## Required Format

Please provide **10 human-written college admissions essays** in the following JSON format:

```json
{
  "id": 11,
  "text": "The actual full text of the essay goes here...",
  "label": "human",
  "source": "Where this essay came from (e.g., 'Reddit r/ApplyingToCollege', 'Student volunteer submission', etc.)"
}
```

### Required Fields

1. **id**: Integer, must be 11-20 (IDs 1-10 are AI essays)
2. **text**: String, the complete essay text
3. **label**: Must be exactly `"human"`
4. **source**: String, accurate attribution of where the essay came from

### Optional Fields

You may also include:
- `"notes"`: Any relevant context about the essay
- `"author_background"`: Anonymous demographic info if relevant (e.g., "ESL student", "high achiever", etc.)

## Data Integrity Requirements

✅ **DO**:
- Use genuine human-written essays
- Accurately attribute the source
- Preserve original text (typos, grammar, style)
- Use publicly available essays or essays you have permission to use
- Anonymize any identifying information

❌ **DO NOT**:
- Use AI-generated text labeled as human
- Fabricate sources
- Claim essays came from Reddit/forums unless they actually did
- Include personally identifying information

## Acceptable Sources

Examples of legitimate sources:
- Public college essay examples from Reddit (with subreddit citation)
- Published essay collections (with citation)
- Student volunteers who gave permission
- Your own past essays (with self-attribution)
- Public educational websites with example essays

## How to Add Them

1. Open `data/test_essays.json`
2. Add your 10 human essay objects to the `"essays"` array
3. Ensure IDs are 11-20
4. Save the file
5. Run: `cd backend && python evaluate.py`

## Validation

The evaluation script will validate:
- Exactly 10 human + 10 AI essays
- All required fields present
- Labels are either "human" or "ai"
- No missing text or metadata

## Example Entry

```json
{
  "id": 11,
  "text": "I've always been the kid who takes things apart. Not to break them, but to understand them. Last summer I spent three weeks rebuilding my dad's old lawnmower engine. It didn't work when I was done (turned out I mixed up two gaskets), but I learned more from that failure than any success. That's when I realized engineering isn't about getting it right the first time. It's about being curious enough to try again.",
  "label": "human",
  "source": "Reddit r/ApplyingToCollege, u/anonymous (2024)",
  "notes": "Informal tone, specific failure details, conversational structure"
}
```

## Questions?

If you need clarification on format or have questions about data integrity, ask before adding essays.
