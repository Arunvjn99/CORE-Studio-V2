# Skill: Enrollment
**Skill-ID:** 12-Enrollment
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill covers the participant enrollment process — how participants enter the plan, how default elections are set, how beneficiary designations are captured, and what notices must be generated. Enrollment drives the initial configuration of a participant's account and activates deferral deductions.

---

## 1. Enrollment Types

### Affirmative Enrollment

The participant takes an active step to enroll — completing an enrollment form or online enrollment process — and elects a deferral rate and investment elections. No contribution occurs unless the participant acts.

**Platform requirements:**
- Enrollment portal or paper enrollment intake
- Deferral rate election (percentage of compensation or flat dollar — plan-configurable)
- Investment election across available funds
- Beneficiary designation capture
- Payroll integration activation to begin deferral deductions on the next payroll cycle after entry date

### Auto-Enrollment

The plan automatically enrolls eligible participants at a plan-configured default deferral rate unless the participant affirmatively opts out before the first automatic deferral.

**Mandatory for new 401(k) and 403(b) plans under SECURE 2.0** (effective date plan-configurable per IRS guidance). [DATE-VERIFY]

**Platform requirements:**
- Default deferral rate (plan-configurable; must meet SECURE 2.0 minimum for new plans — do not hardcode)
- Opt-out window and opt-out processing
- Default investment in QDIA (if no investment election is made)
- Auto-enrollment notice generation and delivery before first automatic deferral
- For EACA: enforce 90-day permissive withdrawal window
- For QACA: enforce minimum default deferral rate and auto-escalation per QACA requirements

---

## 2. EACA and QACA Structures

### EACA (Eligible Automatic Contribution Arrangement)

An automatic enrollment arrangement meeting IRS requirements. Provides:
- **90-day permissive withdrawal:** Participants who were auto-enrolled and did not affirmatively elect may withdraw their automatic contributions within 90 days of the first automatic deferral, without penalty (ordinary income tax applies; no 10% early distribution penalty)
- **QDIA safe harbor:** Default investment in a QDIA is protected from fiduciary liability
- Required notice must be provided before or on the date of first automatic enrollment

**Platform requirements:**
- Track the 90-day withdrawal window per participant from the first automatic deferral date
- Process 90-day withdrawals without the 10% penalty; apply correct 1099-R distribution code
- Close the 90-day window when it expires and lock out the permissive withdrawal option
- Generate EACA notice; track delivery

### QACA (Qualified Automatic Contribution Arrangement)

An EACA that also satisfies ADP/ACP safe harbor requirements. Additional requirements:
- Minimum default deferral rate (plan-configurable per IRS QACA minimums — do not hardcode)
- Auto-escalation (annual deferral rate increase up to a plan-configurable cap)
- Required employer safe harbor contributions (matching or non-elective per QACA formula)
- Permits up to 2-year cliff vesting on safe harbor employer contributions (unlike Traditional Safe Harbor which requires immediate vesting)

**Platform requirements:**
- All EACA requirements plus:
- Enforce QACA minimum default deferral rate
- Auto-escalation engine (annual increase on plan-configured schedule)
- Track QACA 2-year cliff vesting for safe harbor contributions separately from other employer sources

---

## 3. QDIA Default Investment Logic

If a participant does not make an investment election (either because they are auto-enrolled or because they affirmatively enrolled without choosing investments), contributions must be routed to the plan's **Qualified Default Investment Alternative (QDIA)**.

**Common QDIA types:**
- Target-Date Funds (TDF series based on participant's expected retirement year) — most common
- Balanced funds
- Managed accounts

**Platform requirements:**
- Route contributions to the plan's designated QDIA when no investment election exists
- Generate QDIA notice before or at the time contributions are first invested in the QDIA [COMPLIANCE-SENSITIVE]
- Maintain the ability for participants to transfer out of the QDIA to other plan investments at any time
- Track whether a participant's QDIA investment resulted from a default (no election) vs. an affirmative choice — relevant for 404(c) protection
- For TDF QDIAs, the platform may need to automatically assign the correct vintage TDF based on the participant's expected retirement year (calculated from date of birth)

---

## 4. Deferral Rate Election

Participants elect a deferral rate as:
- **Percentage of compensation** (most common) — percentage is plan-configurable; IRS annual deferral limit applies
- **Flat dollar amount** (if plan permits) — platform must monitor against IRS annual deferral limit in dollar terms

**Platform requirements:**
- Enforce the plan-configured minimum and maximum deferral rates (if any)
- Monitor year-to-date deferrals against the annual elective deferral limit (plan-configurable per IRS limit table)
- Monitor additional catch-up contribution eligibility (age 50+; Super Catch-Up ages 60–63 under SECURE 2.0)
- Integrate with payroll to activate the elected deferral rate beginning on the next available payroll cycle

---

## 5. Beneficiary Designation

Enrollment must capture a beneficiary designation.

**Spousal beneficiary rules:**
- If a participant is married, ERISA and plan terms may require the spouse to be the primary beneficiary unless the spouse provides written, notarized consent to an alternate designation
- The platform must capture marital status and flag designations that may require spousal consent
- Spousal consent must be captured and stored before the alternate designation is effective

[COMPLIANCE-SENSITIVE]

**Platform requirements:**
- Beneficiary designation form (online or paper)
- Capture: beneficiary name, relationship, designation type (primary/contingent), percentage allocation
- Validate that primary beneficiary percentages total 100%
- Validate that contingent beneficiary percentages total 100%
- Flag and hold non-spouse primary beneficiary designations for spousal consent if participant is married
- Version-control beneficiary designations with effective dates

---

## 6. Investment Election Changes Post-Enrollment

After enrollment, participants may change their investment elections at any time (subject to plan and fund trading restrictions):
- **Future contributions:** Change how new contributions are allocated across funds
- **Existing balances:** Transfer existing balances between funds (fund-to-fund transfer)

Both types of changes must be processed within the plan's trade execution window. See Skill 14 (Investment Management) for trading mechanics.

---

## 7. Enrollment Notices Required

| Notice | Timing |
|---|---|
| Auto-enrollment notice | Before or on first automatic deferral |
| QDIA notice | Before or at time of first QDIA investment |
| Safe harbor notice (if safe harbor plan) | At least 30 days before plan year start (or before entry for new participants) |
| EACA 90-day withdrawal notice | At auto-enrollment |

---

## 8. Agent Rules

- **[COMPLIANCE-SENSITIVE]** — QDIA notice is required before the first QDIA investment. Failure to deliver is an ERISA violation.
- **[COMPLIANCE-SENSITIVE]** — Spousal consent rules for beneficiary designations must be enforced for married participants.
- Auto-enrollment is mandatory for new 401(k)/403(b) plans under SECURE 2.0 — verify effective date and plan type before writing scope. [DATE-VERIFY]
- Never hardcode default deferral rates or QACA minimums — these are plan-configurable per IRS guidance.
- The 90-day EACA withdrawal window must be tracked per participant from the date of the first automatic deferral — not from the plan's entry date.

---

## Sources

- IRC Section 401(k)(2), 401(k)(13) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL Regulation 29 CFR 2550.404c-5 (QDIA) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 — Mandatory Auto-Enrollment | https://www.congress.gov | Retrieved 2026-03-06
- ERISA Sections 205, 404(c) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
