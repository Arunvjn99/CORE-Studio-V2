# Brand & Design Language Guidelines

## 1. Brand Voice & Tone

### Personality Attributes
- **Clear**: say exactly what we mean; no jargon or corporate speak
- **Confident**: authoritative but not arrogant; we know our domain
- **Human**: warm, empathetic, approachable — we talk to people, not at them
- **Precise**: accurate, specific, and trustworthy — especially in financial and health contexts

### Tone by Context
| Context | Tone | Example |
|---|---|---|
| Success state | Warm, celebratory | "Application submitted! We'll review it within 24 hours." |
| Error state | Calm, helpful | "Something went wrong. Try again or contact support." |
| Onboarding | Encouraging, clear | "Let's set up your account — it takes about 2 minutes." |
| Loading | Reassuring | "Checking your details…" |
| Empty state | Inviting | "No projects yet. Create your first one to get started." |
| Destructive action | Direct, cautious | "Delete this account? This cannot be undone." |

### Writing Rules
- Sentence case for headings and labels (not Title Case)
- Use contractions in UI copy (it's, you're, we'll) — more conversational
- Address users as "you" not "the user"
- Refer to the product in first-person plural ("we", "our") for messages from the system
- Active voice: "Save your changes" not "Changes will be saved"
- Avoid: "please", "sorry", "unfortunately" — they slow reading without adding value
- Avoid: "click" (device-agnostic) — prefer "select", "choose", "tap", "press"

### Content Length
- Button labels: 1–3 words
- Headings: 5 words maximum
- Error messages: 1–2 sentences, action-oriented
- Tooltips: 1 sentence
- Descriptions: 2–3 sentences maximum; if more is needed, link to documentation

## 2. Logo Usage

- Minimum clear space: equal to the height of the logo's cap-height on all sides
- Minimum size: 24px height digital, 10mm print
- Do not rotate, distort, recolour, or add effects to the logo
- On dark backgrounds: use the white/light variant
- On busy backgrounds: use the contained (with background box) variant
- Never place the logo on low-contrast surfaces

## 3. Colour System

### Primary Palette
| Token | Hex | Usage |
|---|---|---|
| `primary` | `#5B5EF4` | Primary buttons, active states, key links |
| `primary-hover` | `#4A4DD6` | Hover state of primary elements |
| `primary-light` | `#5B5EF412` | Tinted backgrounds behind primary elements |

### Neutral Palette
| Token | Hex | Usage |
|---|---|---|
| `background` | `#FFFFFF` | Page background |
| `surface` | `#F7F7F7` | Card backgrounds, inset sections |
| `surface-subtle` | `#F0F0F0` | Hover backgrounds, zebra stripes |
| `text-primary` | `#171717` | Main body text, headings |
| `text-secondary` | `#525252` | Supporting text, descriptions |
| `text-tertiary` | `#8A8A8A` | Captions, metadata, placeholders |
| `border` | `#E5E5EA` | Default borders |
| `border-strong` | `#D1D1D6` | Stronger borders, input focus |

### Semantic Colours
| Token | Hex | Usage |
|---|---|---|
| `success` | `#34C759` | Confirmed, completed, valid states |
| `success-light` | `#34C75912` | Success message background |
| `warning` | `#FF9500` | Caution, needs attention |
| `warning-light` | `#FF950012` | Warning message background |
| `danger` | `#FF3B30` | Errors, destructive actions |
| `danger-light` | `#FF3B3012` | Error message background |
| `info` | `#0A84FF` | Informational, neutral notices |
| `info-light` | `#0A84FF12` | Info message background |

### Colour Usage Rules
- Primary colour for ONE action per screen — do not use on nav AND button AND badge AND icon
- Never use `#000000` pure black on white — use `#171717` (less harsh, still accessible)
- Never use semantic colours decoratively — red means error, green means success, always
- Dark mode: surface `#1C1C1E`, background `#000000`, text-primary `#FFFFFF`, border `rgba(255,255,255,0.1)`

## 4. Typography

### Type Scale
| Level | Size | Weight | Line Height | Usage |
|---|---|---|---|---|
| Display | 48px | 800 | 1.1 | Hero headlines |
| H1 | 36px | 700 | 1.2 | Page titles |
| H2 | 28px | 700 | 1.25 | Section titles |
| H3 | 22px | 600 | 1.3 | Sub-section titles |
| H4 | 18px | 600 | 1.35 | Card titles |
| Body Large | 16px | 400 | 1.6 | Long-form content |
| Body | 14px | 400 | 1.5 | Default UI text |
| Small | 13px | 400 | 1.45 | Secondary info |
| Caption | 12px | 500 | 1.4 | Labels, badges, metadata |
| Overline | 11px | 600 | 1.4 | Section labels (UPPERCASE + letter-spacing 0.06em) |

### Font Stack
Primary: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
Monospace: `"JetBrains Mono", "Fira Code", Menlo, monospace`

### Typography Rules
- Never more than 3 font sizes in a single card or section
- Heading letter-spacing: -0.02em (tight) for display sizes, normal for smaller headings
- Bold text (600+) should not be set smaller than 12px
- All-caps text: letter-spacing 0.06–0.10em always; never all-caps body text
- Italic: use sparingly for quotes, emphasis, or technical terms only

## 5. Spacing & Layout System

### Spacing Scale (4px base)
`4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96px`

### Layout Grid
- Desktop: 12-column, 1280px max-width, 24px gutters, 40px margins
- Tablet (768–1024px): 8-column, 16px gutters, 24px margins
- Mobile (< 768px): 4-column, 16px gutters, 16px margins
- Content max-width for forms: 560px; for articles: 720px; for dashboards: 1200px

### Spacing Rules
- Between major page sections: 64–80px desktop, 48px mobile
- Between cards in a grid: 16–24px
- Inside a card: 20–32px padding
- Between related form fields: 16px
- Between unrelated form groups: 32px
- Button padding: 10px vertical, 20px horizontal (default); 8px/16px (compact)

## 6. Border Radius

| Token | Value | Usage |
|---|---|---|
| `radius-xs` | 4px | Tags, small chips, table cells |
| `radius-sm` | 6px | Input fields, small buttons |
| `radius-md` | 10px | Buttons, inputs (default) |
| `radius-lg` | 16px | Cards, panels, modals |
| `radius-xl` | 24px | Large feature cards, hero sections |
| `radius-full` | 9999px | Badges, pills, avatars |

## 7. Iconography

- Use a consistent icon library (Lucide, Heroicons, or Phosphor)
- Size: 16px for inline text, 20px for buttons, 24px for standalone actions, 32px for feature icons
- Stroke weight: 1.5px for 16–20px icons, 1px for 24px+
- Never scale icons with CSS transform — use the correct size variant
- Icon-only buttons always require an accessible label
- Icons must have at least 3:1 contrast ratio against their background

## 8. Imagery & Illustration

- Photography style: real people in authentic situations, not stock-photo perfection
- Illustration style: consistent line weight, limited colour palette (max 4 colours from brand palette)
- No gradient backgrounds in product UI — gradients acceptable in marketing hero sections only
- Placeholder images: use blurred/gray versions of the actual content (not generic grey boxes)
- Image aspect ratios: 16:9 hero, 4:3 card, 1:1 avatar; maintain consistently within a component

## 9. Shadow System

| Token | Value | Usage |
|---|---|---|
| `shadow-xs` | `0 1px 2px rgba(0,0,0,0.06)` | Subtle lift, dropdown items |
| `shadow-sm` | `0 1px 3px rgba(0,0,0,0.08)` | Cards, default elevated elements |
| `shadow-md` | `0 4px 12px rgba(0,0,0,0.08)` | Modals, dropdowns, popovers |
| `shadow-lg` | `0 8px 24px rgba(0,0,0,0.10)` | Drawers, feature panels |

Shadow rules:
- Maximum one shadow layer per element
- No coloured shadows (except brand-specific design systems like Stripe's blue-tinted shadows)
- On dark surfaces: use opacity-based white glow rather than dark shadows
