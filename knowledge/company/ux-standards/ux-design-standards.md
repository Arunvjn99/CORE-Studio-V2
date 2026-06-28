# UX Design Standards

## 1. Nielsen's 10 Usability Heuristics (Apply to Every Screen)

1. **Visibility of system status** — Always keep users informed about what's happening via timely feedback (loading states, progress indicators, success/error messages)
2. **Match between system and real world** — Use language and concepts familiar to the user; follow real-world conventions; never use internal jargon
3. **User control and freedom** — Provide clear "undo" and "escape" routes; users make mistakes and need to recover easily
4. **Consistency and standards** — Follow platform conventions; use the same words, actions, and situations consistently
5. **Error prevention** — Design to prevent problems from occurring; confirm destructive actions; disable unavailable options
6. **Recognition over recall** — Minimise memory load; make objects, actions, and options visible; instructions should be visible or easy to retrieve
7. **Flexibility and efficiency** — Accelerators (shortcuts) for expert users; let users tailor frequent actions
8. **Aesthetic and minimalist design** — Every extra unit of information competes with relevant information; remove visual noise
9. **Help users recognise, diagnose, and recover from errors** — Error messages in plain language, explain the problem, suggest a solution
10. **Help and documentation** — Provide contextual help that is easy to search and focused on the user's task

## 2. Information Architecture

### Navigation Patterns
- **Primary navigation**: max 5–7 items; group by user mental model not org structure
- **Breadcrumbs**: required for 3+ hierarchy levels; show current location
- **Search**: include when content > 50 items or deep hierarchy
- **Tab navigation**: for switching between related views on the same page; max 8 tabs
- **Sidebar navigation**: for apps with many sections; show active state clearly
- **Mobile navigation**: hamburger menu acceptable only below 768px; prefer bottom tab bar for 3–5 primary destinations

### Content Hierarchy
- One primary action per screen (main CTA)
- Two secondary actions maximum per screen
- Use progressive disclosure to hide advanced options until needed
- F-pattern or Z-pattern reading: place most important content in top-left area

## 3. Form Design

### Structure
- Single-column forms outperform multi-column on completion rate
- Group related fields logically (personal info, contact info, payment)
- Use sections with clear labels for long forms (> 8 fields)
- Progress indicator for multi-step forms (show step X of N)

### Field Design
- Label above field (not inline/floating) for best legibility
- Placeholder text for format hints only ("MM/DD/YYYY"), never as label replacement
- Field width should indicate expected input length (postcode = short; address = long)
- Autofill support: use correct `autocomplete` attribute values

### Validation
- Validate on blur (when field loses focus), not on each keystroke
- Show errors adjacent to the field, not only at top of form
- Error message: specific and actionable ("Password must be at least 8 characters" not "Invalid password")
- Success state: green checkmark after valid entry
- Inline suggestions: show password strength meter while typing

### Button Labels
- Use verb + noun: "Save changes", "Create account", "Submit application"
- Never: "Submit", "OK", "Yes" without context
- Destructive actions: red button, require confirmation dialog
- Loading state: disable button + show spinner + change label ("Saving…")

## 4. Feedback & States

Every interactive element must have defined states:
- **Default**: resting state
- **Hover**: cursor:pointer + subtle background/border change
- **Focus**: visible 2px outline (keyboard users)
- **Active/Pressed**: slightly darker or depressed appearance
- **Disabled**: 40% opacity, cursor:not-allowed, no hover effect
- **Loading**: spinner or skeleton; disable interaction
- **Error**: red border + error message
- **Success**: green border + success message

### Loading States
- Skeleton screens preferred over spinners for content areas (less perceived wait)
- Spinner for actions (save, delete) where duration is < 3s
- Progress bar for file uploads, long processes
- Never block the entire page for actions that only affect part of the UI

### Empty States
- Every list/table/dashboard must have a designed empty state
- Include: illustration or icon, clear explanation, primary action to add first item
- Empty state is NOT the same as error state — don't show error UI for empty data

## 5. Mobile UX Standards

- Touch targets minimum 44×44px (Apple HIG), 48×48px preferred (Material)
- Bottom-aligned primary actions — thumbs reach bottom easier on large phones
- Swipe gestures must have visible alternative (button/tap)
- Avoid hover-only interactions — hover does not exist on touch screens
- Input fields: show correct keyboard type (`type="email"`, `type="tel"`, `type="number"`)
- Pinch-to-zoom must not be disabled
- Safe area insets: respect iPhone notch/home indicator (`env(safe-area-inset-*)`)
- Modals on mobile: full-screen or bottom sheet — avoid small centered modals

## 6. Typography in UX

- **Type scale**: use a modular scale (1.25 or 1.333 ratio)
  - Display: 40–56px | H1: 32px | H2: 24px | H3: 20px | Body: 16px | Small: 14px | Caption: 12px
- **Line length**: 60–72 characters for body text; 45–60 for narrow columns
- **Line height**: 1.5 for body (16px text = 24px line height); 1.2 for headings
- **Font weight**: 400 body, 500 labels/emphasis, 600 subheadings, 700 headings, 800 display
- **Letter spacing**: -0.02em to -0.04em on large headings; normal (0) on body text
- Never use more than 2 typefaces in a single design

## 7. Spacing & Layout

- Base unit: 4px or 8px grid
- Consistent spacing scale: 4, 8, 12, 16, 24, 32, 48, 64, 96px
- Section spacing (between major content blocks): 48–80px on desktop, 32–48px on mobile
- Card internal padding: 20–32px
- Input field padding: 10–14px vertical, 12–16px horizontal
- Max content width: 1280px (wide layouts), 960px (comfortable reading), 720px (article/form)

## 8. Interaction Design

### Micro-interactions
- Transitions: 150–300ms for UI elements; 300–500ms for page transitions
- Easing: ease-out for elements appearing, ease-in for disappearing, ease-in-out for continuous motion
- Never animate for animation's sake — every animation must aid comprehension
- Respect `prefers-reduced-motion` — disable non-essential animations

### Affordances
- Buttons must look tappable (filled or bordered, not plain text unless clearly a link)
- Draggable elements: show drag handle icon or cursor:grab
- Expandable items: use chevron icon indicating direction of expansion
- Scrollable areas: show scrollbar on hover; use scroll shadows to indicate more content

## 9. Error Handling UX

- **Prevention first**: disable invalid inputs, warn before destructive actions
- **Detection**: validate in real-time where appropriate (URL format, email format)
- **Recovery**: always provide a clear path to fix the error
- **404 pages**: explain what happened, provide search or home link
- **500 pages**: apologise, explain the issue is on our side, provide retry option
- **Offline states**: detect with Network API, show clear offline indicator

## 10. Onboarding & Empty States

### First-Use Onboarding
- Maximum 3 onboarding screens before reaching the product
- Show value proposition immediately; don't front-load setup
- Allow skipping — let users explore before completing profile
- Contextual tooltips inline are better than upfront tutorials

### Progressive Onboarding
- Show hints when a feature is encountered for the first time
- Use "Welcome" empty states with a prominent action to get started
- Track completion: show setup checklist for complex products (like Notion's getting-started sidebar)

## 11. Data Visualisation

- Choose chart type by data type: bar (comparison), line (trend over time), pie (composition, max 5 segments), scatter (correlation)
- Always include axis labels and units
- Colour-blind safe palettes: avoid red+green alone for pass/fail; add pattern or shape
- Show data table alternative for complex charts (accessibility)
- Tooltips on hover with exact values
- Empty chart state: show the axes but explain no data available yet
