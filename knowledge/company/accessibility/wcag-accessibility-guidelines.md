# Accessibility Guidelines — WCAG 2.1 AA & 2.2

## Core Principle
Every interface must be Perceivable, Operable, Understandable, and Robust (POUR). Target WCAG 2.1 Level AA as the baseline for all designs.

## 1. Colour Contrast
- Normal text (< 18px or < 14px bold): minimum contrast ratio **4.5:1** against background
- Large text (≥ 18px regular or ≥ 14px bold): minimum contrast ratio **3:1**
- UI components and graphical objects (icons, input borders, focus indicators): minimum **3:1**
- Never convey information by colour alone — always pair with text, icon, or pattern
- Test combinations: white `#FFFFFF` on `#767676` passes AA (4.54:1); black `#000000` on `#767676` also passes

## 2. Touch & Click Targets
- Minimum touch target size: **44×44 CSS pixels** (WCAG 2.5.5)
- WCAG 2.2 adds Target Size (Minimum) at **24×24 CSS pixels** with adequate spacing
- Preferred minimum for mobile: **48×48 px** to reduce mis-taps
- Spacing between adjacent targets: at least **8px** gap

## 3. Focus Management & Keyboard Navigation
- Every interactive element must be reachable and operable via keyboard (Tab, Shift+Tab, Enter, Space, arrow keys)
- Visible focus indicator required — minimum 2px solid outline with 3:1 contrast against adjacent colours
- Use `focus-visible` CSS pseudo-class so focus only shows on keyboard (not mouse click)
- Focus order must follow logical reading order (left→right, top→bottom in LTR layouts)
- Modals and drawers: trap focus within the overlay; return focus to trigger on close
- Skip-to-content link as first focusable element on every page

## 4. Screen Reader & Semantic HTML
- Use native HTML elements wherever possible: `<button>`, `<a>`, `<input>`, `<select>`, `<table>`
- Every form field must have a visible `<label>` — never rely on placeholder text alone
- Images: meaningful images need descriptive `alt` text; decorative images use `alt=""`
- Icons used alone: add `aria-label` on the button; hide the icon from AT with `aria-hidden="true"`
- Landmark roles: every page must have `<main>`, `<nav>`, `<header>`, `<footer>`
- Heading hierarchy: one `<h1>` per page; do not skip heading levels (h1→h2→h3)
- Dynamic content changes: use `aria-live="polite"` for non-urgent updates, `aria-live="assertive"` for errors only
- Modals: `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to modal title

## 5. Forms & Error Handling
- Error messages must be specific ("Enter a valid 10-digit phone number", not "Invalid input")
- Error state: use `aria-invalid="true"` on the input and `aria-describedby` pointing to the error message element
- Required fields: mark with `aria-required="true"` and a visible indicator (asterisk with legend)
- Group related fields with `<fieldset>` and `<legend>`
- Inline validation: show errors after field loses focus (not on every keystroke — frustrates users)
- Success confirmation: announce via `aria-live` region

## 6. Images, Media & Animation
- Videos must have captions (closed captions, not just auto-generated)
- Audio content needs a transcript
- Avoid autoplay of audio or video
- Animations and transitions: respect `prefers-reduced-motion` media query — disable or reduce motion
- Flashing content: nothing must flash more than 3 times per second (seizure risk)

## 7. Responsive & Zoom
- Content must be readable and functional at 200% browser zoom without horizontal scrolling
- Text must scale with browser font size (use rem/em units, not px for font sizes)
- Do not disable pinch-zoom on mobile (`user-scalable=no` is forbidden)

## 8. Links & Navigation
- Link text must be descriptive ("Download Q4 report PDF" not "Click here")
- Identical link text on a page must go to the same destination
- New-window links: warn users with `aria-label` or visible "(opens in new tab)"
- Breadcrumb navigation: use `<nav aria-label="Breadcrumb">` with `aria-current="page"` on last item

## 9. Tables
- Use `<table>`, `<th scope="col/row">`, `<caption>` for data tables
- Do not use tables for layout
- Complex tables: use `id`/`headers` attribute pairing

## 10. WCAG 2.2 New Criteria (AA)
- **2.4.11 Focus Not Obscured (Minimum)**: keyboard focus indicator must not be fully hidden by sticky headers/footers
- **2.4.12 Focus Not Obscured (Enhanced)**: focused component fully visible (AAA but good practice)
- **2.5.3 Label in Name**: visible label text must be contained in the accessible name
- **2.5.7 Dragging Movements**: all drag operations must have a pointer alternative
- **3.2.6 Consistent Help**: help mechanisms in same location across pages
- **3.3.7 Redundant Entry**: do not ask users to re-enter information already provided in same session
- **3.3.8 Accessible Authentication (Minimum)**: cognitive function tests (CAPTCHA, puzzles) must have an alternative

## 11. Component-Specific Rules

### Buttons
- `<button type="button">` for actions, `<button type="submit">` for form submit
- Never use `<div>` or `<span>` as buttons
- Loading state: `aria-busy="true"`, `aria-label="Saving..."` while in progress
- Disabled buttons: use `aria-disabled="true"` (not `disabled` attribute when you still want focus)

### Inputs & Selects
- Placeholder text contrast must also meet 4.5:1 (often missed — `#999` on `#FFF` = 2.85:1, FAILS)
- `<select>` is preferred over custom dropdowns for accessibility; if custom, implement full ARIA combobox pattern
- Date inputs: support keyboard entry, not just date picker widgets

### Modals / Dialogs
- Trigger: `aria-haspopup="dialog"` on trigger button
- Close: Escape key must close; clicking backdrop must close
- Focus: move focus to first focusable element inside dialog on open

### Tables & Data Grids
- Sortable columns: `aria-sort="ascending|descending|none"` on `<th>`
- Selected rows: `aria-selected="true"`

## 12. Testing Checklist
- [ ] Run axe DevTools or Lighthouse accessibility audit (target score 90+)
- [ ] Keyboard-only navigation test: tab through every interactive element
- [ ] Screen reader test: NVDA+Firefox (Windows), VoiceOver+Safari (Mac/iOS), TalkBack (Android)
- [ ] Colour contrast check on all text/background combinations
- [ ] Zoom to 200% — check no content loss
- [ ] Reduced motion test: enable OS reduced motion and verify animations stop
- [ ] High contrast mode (Windows) — check visibility
