# Writing Clearly and Concisely

A skill that applies Steven Pinker's *The Sense of Style* to produce clear prose that readers outside your head can follow, and strips the hype and filler that make blog posts, social posts, and docs read as AI-written.

## Purpose

This skill helps you write better prose for human readers. It draws from two sources:

1. **The Sense of Style** (Pinker, 2014) - Guidance on clarity grounded in linguistics and cognitive science. Its "classic style" and "curse of knowledge" chapters explain why readers get lost in expert writing, which makes it well suited to technical blog posts.
2. **AI Pattern Avoidance** - Patterns that make blogs, social posts, and docs read as machine-written (hook formulas, inflated significance, AI vocabulary), with fixes

Whether you're writing documentation, commit messages, error messages, or any text humans will read, this skill helps you cut fluff and say what you mean.

## When to Use

Use this skill whenever you write prose for humans:

- **Documentation** - README files, API docs, technical explanations
- **Git workflow** - Commit messages, pull request descriptions
- **User-facing text** - Error messages, UI copy, help text, tooltips
- **Code comments** - Inline documentation, docstrings
- **Reports and summaries** - Status updates, analysis, explanations
- **Editing** - Improving clarity of existing text

**Trigger phrases:**
- "Write documentation for..."
- "Draft a README"
- "Edit this for clarity"
- "Make this more concise"
- "Review this commit message"

## How It Works

1. **Load the skill** when writing prose for human readers
2. **Apply Pinker's core principles** - classic style, beat the curse of knowledge, given-before-new, consistent terms
3. **Avoid AI patterns** - no puffery, no empty phrases, no promotional adjectives
4. **Reference detailed guides** when needed for specific rules

### Context-Efficient Approach

The skill uses progressive disclosure to save context:

- **SKILL.md** (~900 tokens) loads first and covers most tasks on its own
- **Reference files** load only when needed: `signs-of-ai-writing.md` (~1,300 tokens) for blog and social posts or AI-tell reviews, `sense-of-style.md` (~1,300 tokens) for long documents or explaining edits

## Key Features

### Pinker's Core Principles

The skill emphasizes these ideas from *The Sense of Style*:

| Idea | Principle |
|------|-----------|
| Classic style | Point the reader at the subject; cut metadiscourse and needless hedges |
| Curse of knowledge | Write for a smart outsider; define jargon, unpack abstractions, give examples |
| Zombie nouns | Turn nominalizations back into verbs |
| Given before new | Start with what the reader knows; end with what's new |
| Coherence | Call each thing by one name; make connections explicit |
| Usage | Follow rules that aid clarity; ignore myths |

### AI Pattern Detection

The skill identifies and eliminates common LLM writing patterns:

- **Puffery**: pivotal, crucial, vital, testament, enduring legacy
- **Empty "-ing" phrases**: ensuring reliability, showcasing features
- **Promotional adjectives**: groundbreaking, seamless, robust, cutting-edge
- **Overused AI vocabulary**: delve, leverage, foster, realm, tapestry
- **Social-post formulas**: "Here's the thing:", broetry, engagement bait, hashtag stacks
- **Formatting overuse**: excessive bullets, emoji decorations, bold on every other word

## Reference Files

| Section | File | Tokens | Content |
|---------|------|--------|---------|
| Writing principles | `sense-of-style.md` | ~1,300 | Classic style, curse of knowledge, syntax, coherence, usage |
| AI patterns | `signs-of-ai-writing.md` | ~1,300 | Content, language, social-post, and formatting patterns with fixes |

## Usage Examples

### Example 1: Tightening a Commit Message

**Before:**
> This commit implements the functionality for ensuring that user authentication is properly handled, showcasing robust error handling capabilities.

**After:**
> Add user authentication with error handling

### Example 2: Rewriting Documentation

**Before:**
> This groundbreaking feature leverages cutting-edge technology to deliver a seamless experience, fostering better engagement and driving impactful results.

**After:**
> This feature uses WebSocket connections to update the dashboard in real time.

### Example 3: Beating the Curse of Knowledge

**Before:**
> The reconciler runs during the RC phase to handle drift.

**After:**
> Every 30 seconds, the reconciler compares the cluster's actual state with the config file and fixes any differences.

### Example 4: Removing Hedging

**Before:**
> It is important to note that the API might potentially return an error in certain situations.

**After:**
> The API returns an error when the token expires.

## Best Practices

1. **Be specific, not grandiose** - Say what it actually does, not how important it is
2. **Cut first, add later** - Remove words until meaning suffers, then add back what's needed
3. **Write for an outsider** - Define terms and give an example for each abstraction
4. **Revive zombie nouns** - "Caching cut latency" beats "The implementation of caching resulted in a reduction of latency"
5. **Use concrete language** - "The server crashed" beats "An issue occurred"
6. **Load reference files sparingly** - The principles in SKILL.md cover most tasks

## Directory Structure

```
writing-clearly-and-concisely/
  SKILL.md                 # Main skill definition
  README.md                # This file
  sense-of-style.md        # Notes on Pinker's The Sense of Style
  signs-of-ai-writing.md   # AI pattern detection guide
```

## Installation

**Claude Code:**
```bash
cp -r skills/writing-clearly-and-concisely ~/.claude/skills/
```

**Claude.ai:**
Add the skill to project knowledge or paste SKILL.md contents into your conversation.

## Attribution

- Original skill by @joshuadavidthomas from [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills) (MIT)
- Writing principles summarized from *The Sense of Style* by Steven Pinker (2014)
- AI patterns adapted from Wikipedia's field guide to AI-generated content (CC BY-SA 4.0)
