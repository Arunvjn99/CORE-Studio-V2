# CORE 2.0 Design System

> Category: Enterprise Platform
> Clean, professional enterprise UI. Structured hierarchy, semantic colour, accessibility-first.

## 1. Visual Theme & Atmosphere

CORE 2.0 is an enterprise design system built for clarity, efficiency, and scale. It communicates authority and trustworthiness through a restrained colour palette, structured typography, and a component library optimised for complex workflows — plan management, employee data, financial tables, document upload, and multi-step forms.

The aesthetic sits between the precision of Stripe and the structure of IBM Carbon: clean white surfaces with a single strong primary accent, semantic status colours that carry real meaning, and elevation used sparingly to separate layers of interaction. Every pixel earns its place. There is no decoration for its own sake.

**Key Characteristics:**
- Pure white (`#FFFFFF`) canvas with a light neutral background (`#F5F6F8`) for page-level contrast
- Single primary accent (`#2563EB` — professional blue) used only on primary buttons, active states, links, focus rings, and selected states
- Semantic status colours: green success, amber warning, red critical, blue info — never used decoratively
- 4px base spacing grid with named tokens XS/S/M/L/XL/XXL
- Border radius: small (4px) for inputs, medium (8px) for buttons, large (12px) for cards, pill (9999px) for badges
- Elevation system: Level 0 flat → Level 1 cards → Level 2 dropdowns → Level 3 modals
- Typography: Inter as primary typeface; clear scale from page titles down to helper text
- WCAG 2.1 AA mandatory across all components

## 2. Color System

### Primary
- `#2563EB` — primary actions, active controls, links, focus indicators, selected states
- `#1D4ED8` — hover state of primary
- `#EFF6FF` — tinted background behind primary elements (active rows, info surfaces)
- `#BFDBFE` — primary border tint (selected chip borders, active input borders)

### Success
- `#16A34A` — success badges, validation success, positive statuses, confirmation icons
- `#DCFCE7` — success badge background / success state surfaces
- `#BBF7D0` — success border

### Warning
- `#D97706` — warnings, attention-required actions, validation warnings
- `#FEF3C7` — warning surface background
- `#FDE68A` — warning border

### Critical
- `#DC2626` — errors, destructive actions, failed operations, critical icons
- `#FEE2E2` — error surface background
- `#FECACA` — error border

### Info
- `#0284C7` — informational alerts, neutral guidance
- `#E0F2FE` — info surface background

### Neutral
- `#111827` — primary text (headings, labels, values)
- `#374151` — secondary text (descriptions, table values)
- `#6B7280` — tertiary text (helper text, placeholder, disabled labels)
- `#9CA3AF` — placeholder text
- `#E5E7EB` — default border / dividers
- `#F3F4F6` — subtle surface (zebra rows, input background)
- `#F5F6F8` — page background
- `#FFFFFF` — card surface, input surface, modal background

## 3. Typography

### Font Family
Primary: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

### Scale
| Level | Size | Weight | Line Height | Usage |
|---|---|---|---|---|
| Page Title | 24px | 700 | 1.25 | Component pages, application headers, major sections |
| Section Header | 18px | 600 | 1.35 | Documentation sections, screen sections |
| Body | 14px | 400 | 1.5 | Labels, inputs, descriptions, table values |
| Small | 13px | 400 | 1.45 | Supporting text, secondary information |
| Helper Text | 12px | 400 | 1.4 | Validation messages, supporting information, status messages |
| Caption / Label | 11px | 600 | 1.4 | Uppercase overlines, chip labels, badge text (letter-spacing: 0.04em) |

### Rules
- Headings: colour `#111827`, never pure black
- Body and values: colour `#374151`
- Helper / muted: colour `#6B7280`
- Disabled: colour `#9CA3AF`

## 4. Spacing System

Base unit: 4px

| Token | Value | Usage |
|---|---|---|
| XS | 4px | Icon spacing, tight internal gaps |
| S | 8px | Label-to-control spacing, icon-label gap |
| M | 16px | Component internal padding (inputs, buttons, cells) |
| L | 24px | Card padding, form field group spacing |
| XL | 40px | Section spacing within a page |
| XXL | 64px | Page-level section spacing, major layout gaps |

### Layout Rules
- Component internal spacing: XS between icon and label; S between label and control; M padding inside the control
- Card internal padding: L (24px)
- Between form sections: XL (40px)
- Between page sections: XXL (64px)

## 5. Radius System

| Token | Value | Usage |
|---|---|---|
| Small | 4px | Inputs, selects, checkboxes, table cells |
| Medium | 8px | Buttons, upload controls, date pickers |
| Large | 12px | Cards, containers, modals |
| Pill | 9999px | Chips, badges, tags |

## 6. Elevation System

| Level | Shadow | Usage |
|---|---|---|
| 0 | none | Flat surfaces: forms, tables, page background |
| 1 | `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)` | Cards: employee cards, investment cards, plan cards |
| 2 | `0 4px 12px rgba(0,0,0,0.10), 0 2px 4px rgba(0,0,0,0.06)` | Floating: dropdowns, date pickers, tooltips |
| 3 | `0 20px 40px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.08)` | Modals: confirmation dialogs, alert modals |

## 7. Focus System

Every interactive element must expose visible focus for keyboard and AT users.

- Focus ring: `2px solid #2563EB` outline + `2px` offset
- Applied to: buttons, inputs, selects, date pickers, upload areas, checkboxes, chips, table action cells
- Never suppress outline — use `focus-visible` CSS so focus only shows on keyboard (not on mouse click)

## 8. Components

### Button
- **Primary**: `background: #2563EB; color: #FFFFFF; border-radius: 8px; padding: 10px 20px; font-size: 14px; font-weight: 600`
- **Secondary**: `background: #FFFFFF; color: #111827; border: 1.5px solid #E5E7EB; border-radius: 8px; padding: 9px 20px; font-weight: 500`
- **Tertiary**: `background: transparent; color: #2563EB; border: none; padding: 9px 16px; font-weight: 500`
- **Destructive**: `background: #DC2626; color: #FFFFFF; border-radius: 8px; padding: 10px 20px; font-weight: 600`
- Sizes: Regular (14px, 10/20px padding) | Small (13px, 8/16px) | XS (12px, 6/12px)
- Disabled: 40% opacity, `cursor: not-allowed`

### Input Text
- `background: #FFFFFF; border: 1.5px solid #E5E7EB; border-radius: 4px; padding: 10px 14px; font-size: 14px; color: #111827`
- Focus: border-color `#2563EB`, box-shadow `0 0 0 3px #EFF6FF`
- Success: border-color `#16A34A`, box-shadow `0 0 0 3px #DCFCE7`
- Warning: border-color `#D97706`, box-shadow `0 0 0 3px #FEF3C7`
- Critical (error): border-color `#DC2626`, box-shadow `0 0 0 3px #FEE2E2`
- View mode: `background: #F3F4F6; border-color: transparent; color: #374151`
- Disabled: `background: #F9FAFB; color: #9CA3AF; cursor: not-allowed`

### Card
- `background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08)`
- Plan Details Card: structured rows with label/value pairs; header with title + badge
- Employee Card: avatar (40px initials circle) + name + role + status badge
- Investment Card: fund name + allocation % + bar graph + value

### Badge / Status
- **Success**: `background: #DCFCE7; color: #16A34A; border-radius: 9999px; padding: 3px 10px; font-size: 12px; font-weight: 600`
- **Warning**: `background: #FEF3C7; color: #D97706; border-radius: 9999px; padding: 3px 10px; font-size: 12px; font-weight: 600`
- **Critical**: `background: #FEE2E2; color: #DC2626; border-radius: 9999px; padding: 3px 10px; font-size: 12px; font-weight: 600`
- **Info**: `background: #E0F2FE; color: #0284C7; border-radius: 9999px; padding: 3px 10px; font-size: 12px; font-weight: 600`
- **Neutral**: `background: #F3F4F6; color: #374151; border-radius: 9999px; padding: 3px 10px; font-size: 12px; font-weight: 600`
- Strong variant: increase background opacity; Subtle variant: reduce to 50% opacity background

### Data Table
- Header row: `background: #F9FAFB; border-bottom: 2px solid #E5E7EB; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: #6B7280; padding: 12px 16px`
- Data row: `border-bottom: 1px solid #E5E7EB; padding: 14px 16px; font-size: 14px; color: #374151`
- Hover row: `background: #F5F6F8`
- Selected row: `background: #EFF6FF; border-left: 3px solid #2563EB`
- Sortable column: show sort icon on hover; active sort icon coloured `#2563EB`
- Action cell: icon buttons (16px), show on row hover only

### Modal
- Overlay: `background: rgba(0,0,0,0.5); backdrop-filter: blur(2px)`
- Container: `background: #FFFFFF; border-radius: 12px; padding: 32px; max-width: 480px; box-shadow: 0 20px 40px rgba(0,0,0,0.12)`
- Status icon (48px circle): success green, warning amber, error red, info blue
- Title: 18px, font-weight 700, `#111827`; Description: 14px, `#374151`, margin-top 8px
- Actions: right-aligned, primary + secondary buttons; 16px gap
- Close (X): top-right, icon button, ghost variant

### Checkbox
- 18×18px control; `border: 2px solid #E5E7EB; border-radius: 4px; background: #FFFFFF`
- Checked: `background: #2563EB; border-color: #2563EB` with white checkmark SVG
- Indeterminate: `background: #2563EB; border-color: #2563EB` with white minus
- Disabled: `background: #F3F4F6; border-color: #E5E7EB; cursor: not-allowed`
- Focus: `box-shadow: 0 0 0 3px #EFF6FF`

### Chip / Tag
- `border: 1.5px solid #E5E7EB; border-radius: 9999px; padding: 4px 14px; font-size: 13px; font-weight: 500; color: #374151`
- Active: `background: #EFF6FF; border-color: #BFDBFE; color: #2563EB`
- With checkmark: show `✓` before label text when active

### Accordion
- Header: `padding: 16px; border-bottom: 1px solid #E5E7EB; font-size: 14px; font-weight: 600; color: #111827; cursor: pointer`
- Toggle icon: chevron, rotates 180° when expanded
- Panel: `padding: 16px; background: #FAFAFA; font-size: 14px; color: #374151`
- Summary variant: header includes a summary value (e.g., "Total: $12,450") right-aligned in muted colour

### Date Picker
- Trigger input: same as Input Text with calendar icon (right-aligned, `#6B7280`)
- Calendar popup: Level 2 elevation, `border-radius: 12px`; Month/year header + day grid
- Selected day: `background: #2563EB; color: #FFFFFF; border-radius: 50%`
- Today: `border: 2px solid #2563EB; border-radius: 50%`
- Range: start/end filled primary; range fill `#EFF6FF`

### Drag & Drop Upload
- Area: `border: 2px dashed #E5E7EB; border-radius: 8px; padding: 32px; text-align: center; background: #FAFAFA`
- Drag-over: `border-color: #2563EB; background: #EFF6FF`
- Success result: green border `#16A34A` + filename + file size + remove icon
- Error result: red border `#DC2626` + error message
- Show accepted types and max size as helper text below the area

### Select Input
- Same base style as Input Text + chevron icon right-aligned
- Dropdown: Level 2 elevation, `border-radius: 8px`, `max-height: 240px`, scrollable
- Option hover: `background: #F3F4F6`
- Selected option: `background: #EFF6FF; color: #2563EB; font-weight: 500`
- With search: search field at top of dropdown, `border-bottom: 1px solid #E5E7EB`

## 9. Accessibility Standards

All components must implement:
- **Keyboard**: Tab to focus, Enter/Space to activate buttons and checkboxes, Escape to close modals/dropdowns, Arrow keys in lists
- **Screen reader**: `aria-label` on icon-only buttons, `aria-describedby` linking inputs to helper/error text, `aria-invalid` on error inputs, `aria-live="polite"` for dynamic status messages, `role="dialog"` + `aria-modal="true"` on modals
- **Focus visibility**: 2px primary blue focus ring on every interactive element; never remove focus outline
- **Colour contrast**: minimum 4.5:1 for body text, 3:1 for large text and UI components
- **Disabled states**: `aria-disabled="true"` (not just the `disabled` attribute) so element remains focusable and discoverable

## 10. Design Patterns

### Forms
- Input Text + Select + Date Picker + Checkbox are preferred controls
- Labels always above inputs (never floating or inline-only)
- Group related fields in cards (Level 1 elevation)
- Validation: inline, on blur — error message below the field using Helper Text style
- Multi-step forms: progress bar at top (completed steps in primary blue, upcoming in neutral grey)

### Tables
- Use Data Table with sorting + filtering for any dataset > 10 rows
- Row actions: icon buttons visible on hover (edit pencil, delete trash, view eye)
- Empty state: centred illustration + title + description + primary CTA

### Status Communication — hierarchy
1. Badge — inline status on a record
2. Inline validation — form field error/success
3. Alert banner — page-level status
4. Modal — requires user decision before continuing

### Progressive Disclosure
- Accordion for grouped financial data, plan details, investment breakdowns
- Modal for actions requiring user focus and confirmation
- Never show more than 7 fields on screen without sectioning into accordions or steps
