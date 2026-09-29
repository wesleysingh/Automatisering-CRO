# Skill: `claude-api`

## Wanneer gebruiken

Gebruik **`/claude-api`** wanneer:
- De code `import anthropic` of `@anthropic-ai/sdk` bevat
- Het project een Claude-model aanroept via de Anthropic API
- De gebruiker vraagt om prompt caching, tool use, of batch-verwerking
- Een bestaande Claude-integratie geüpgraded moet worden naar een nieuwer model
- Er vragen zijn over SDK-gebruik, API-tokens of model-IDs

## Wat het doet

- Bouwt, debugt en optimaliseert Claude API-applicaties
- Voegt automatisch **prompt caching** toe voor kostenbesparing
- Helpt bij migratie tussen modelversies (bijv. Sonnet 4.5 → 4.6)
- Adviseert over tool use, thinking-modus, citation-features

## Huidige modelversies (mei 2026)

| Model | ID |
|-------|----|
| Opus 4.7 | `claude-opus-4-7` |
| Sonnet 4.6 | `claude-sonnet-4-6` |
| Haiku 4.5 | `claude-haiku-4-5-20251001` |

## Triggers in project-CLAUDE.md

- "anthropic", "claude API", "SDK", "prompt caching", "tool use"
- Aanwezige bestanden: `anthropic`, `claude_client.py`, `llm.ts`
- Import: `from anthropic import Anthropic` of `import Anthropic from '@anthropic-ai/sdk'`

## Voorbeeld aankondiging

> 🎯 **Skill: `claude-api`** — Dit project importeert de Anthropic SDK en maakt Claude API-aanroepen. Ik gebruik de claude-api skill om de integratie te optimaliseren en prompt caching toe te voegen.
