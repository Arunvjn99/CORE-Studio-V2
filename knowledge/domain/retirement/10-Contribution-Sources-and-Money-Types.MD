# Skill: Contribution Sources and Money Types
**Skill-ID:** 10-Contribution-Sources-and-Money-Types
**World:** Retirement World v1.0
**Category:** Data & Entities
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill is the definitive reference for every contribution source (money type) in a DC plan. Source classification is foundational — it determines vesting schedule, distribution eligibility, tax withholding, 415 limit inclusion, rollover eligibility, and 1099-R reporting. Every contribution, balance, and transaction must be correctly tagged with a source.

---

## Why Source Classification Matters

A single error in source classification can cascade into:
- Incorrect vesting (distributing unvested employer funds prematurely, or withholding vested funds)
- Incorrect tax withholding on distributions (different sources have different tax treatment)
- 415 limit violations (some sources count toward annual additions, others do not)
- Nondiscrimination testing failures (ADP/ACP tests are source-specific)
- Incorrect 1099-R reporting codes

---

## Source Reference Table

| Source / Money Type | Who Contributes | Vesting | Counts Toward 415 | Always Rollover-Eligible | Tax on Distribution | Notes |
|---|---|---|---|---|---|---|
| Employee Pre-Tax (Elective Deferral) | Employee | 100% Immediate (statutory) | Yes | Yes (if ERD) | Ordinary income + potential penalty | Subject to annual deferral limit |
| Designated Roth | Employee (after-tax) | 100% Immediate (statutory) | Yes | Yes (if ERD) | Tax-free if qualified; basis recovery if not | Separate account required; qualified distribution = tax-free |
| Employer Match | Employer | Per plan vesting schedule | Yes | Yes (if ERD) | Ordinary income + potential penalty | Match formula is plan-configurable |
| Employer Non-Elective / Profit Sharing | Employer | Per plan vesting schedule | Yes | Yes (if ERD) | Ordinary income + potential penalty | Discretionary amount; employer decides annually |
| Rollover | Employee (from prior plan/IRA) | 100% Immediate | No | Yes | Ordinary income + potential penalty | Never counts toward 415; always immediately distributable |
| After-Tax (Non-Roth) | Employee (after-tax, non-designated Roth) | 100% Immediate | Yes | Basis portion not taxed; earnings portion yes | Complex ordering rules | Rare; less common in modern plans |
| QNEC (Qualified Non-Elective Contribution) | Employer (corrective) | 100% Immediate (required for QNEC qualification) | Yes | Yes | Ordinary income + potential penalty | Used to correct ADP/ACP failures; must satisfy specific IRS requirements |
| QMAC (Qualified Matching Contribution) | Employer (corrective) | 100% Immediate (required for QMAC qualification) | Yes | Yes | Ordinary income + potential penalty | Used to correct ACP failures; must satisfy specific IRS requirements |
| Safe Harbor Employer (Traditional) | Employer | 100% Immediate (required) | Yes | Yes | Ordinary income + potential penalty | Required for Traditional Safe Harbor ADP/ACP exemption |
| Safe Harbor Employer (QACA) | Employer | Up to 2-year cliff vesting permitted | Yes | Yes | Ordinary income + potential penalty | QACA permits limited vesting on safe harbor match |
| Employer Roth (SECURE 2.0) | Employer (after-tax, Roth) | Per plan vesting schedule | Yes | Yes | Tax-free if qualified distribution of Roth earnings | New under SECURE 2.0; participant elects Roth treatment at time of employer contribution; includible in income at time of contribution [DATE-VERIFY] |
| PLESA | Employee (after-tax) | 100% Immediate | Yes (up to plan-configurable limit) | Yes — any time without penalty | Tax-free (after-tax basis) | SECURE 2.0; non-HCE participants only; separate account [DATE-VERIFY] |
| Loan Repayment | Employee (loan repayment) | N/A | No | N/A | N/A | Not a contribution; credits loan sub-account; must be allocated back to original sources upon payoff |
| Student Loan Payment Match (SLPM) | Employer (match on QLSP) | Per plan vesting schedule | Yes | Yes | Ordinary income + potential penalty | SECURE 2.0; employer match triggered by participant student loan payment [DATE-VERIFY] |

---

## 1. Employee Pre-Tax (Elective Deferral)

**What it is:** A contribution made from an employee's compensation on a pre-tax basis pursuant to a salary reduction agreement.

**Key rules:**
- Always 100% vested immediately — statutory requirement, not plan design
- Subject to the annual elective deferral limit (plan-configurable per current IRS limit table — do not hardcode)
- Catch-up contributions (age 50+) and Super Catch-Up (ages 60–63, SECURE 2.0) are additional layers of pre-tax or Roth contributions tracked separately
- Eligible rollover distribution upon termination, death, disability, or reaching age 59½

**Platform requirements:** Track year-to-date deferrals; monitor against annual deferral limit; stop contributions when limit is reached; alert participant and plan sponsor.

[COMPLIANCE-SENSITIVE]

---

## 2. Designated Roth

**What it is:** An employee contribution made on an after-tax basis, designated as Roth at the time of contribution.

**Key rules:**
- Always 100% vested immediately
- Tracked in a **separate designated Roth account** — must not be commingled with pre-tax deferrals
- Qualified distributions (after 5-taxable-year period and age 59½, death, or disability) are entirely tax-free
- Non-qualified distributions: basis (contributions) is tax-free; earnings are taxable
- Subject to the same annual elective deferral limit as pre-tax deferrals (combined limit)
- **No lifetime RMDs for designated Roth accounts in employer plans (SECURE 2.0)** [DATE-VERIFY]
- Roth in-plan conversion: pre-tax balances may be converted to Roth within the plan if plan permits

**Platform requirements:** Maintain separate Roth account; track 5-year participation period; apply Roth ordering rules for non-qualified distributions; suppress RMD for Roth balances of living participants.

---

## 3. Employer Match

**What it is:** An employer contribution made in connection with an employee's elective deferrals, pursuant to the plan's matching formula.

**Key rules:**
- Match formula is plan-configurable (not hardcoded)
- Subject to plan vesting schedule (immediate, cliff, or graded)
- Counted toward the participant's 415 annual additions limit
- Per-payroll vs. annual match calculation — if annual, a year-end true-up may be required
- Safe harbor match contributions (Traditional or QACA) have specific formula and vesting requirements

**Platform requirements:** Calculate match per the plan's configured formula; apply vesting schedule; track for 415 monitoring; perform year-end true-up if applicable.

---

## 4. Employer Non-Elective / Profit Sharing

**What it is:** A discretionary employer contribution not tied to a specific employee deferral. The employer decides the contribution amount each plan year.

**Key rules:**
- Subject to plan vesting schedule
- Counted toward 415 annual additions limit
- Allocation formula is plan-configurable (pro-rata, integrated with Social Security, new comparability cross-testing)
- Must satisfy nondiscrimination requirements (401(a)(4) general test)

**Platform requirements:** Process allocations per the plan's configured formula; apply vesting; include in 415 monitoring; generate allocation report for plan sponsor approval.

---

## 5. Rollover

**What it is:** A contribution representing assets transferred from a prior employer plan or IRA into the current plan.

**Key rules:**
- 100% immediately vested — always
- Does NOT count toward the 415 annual additions limit
- Always immediately distributable (rollover balances may be distributed at any time regardless of triggering event restrictions)
- Source plan must be an eligible retirement plan (qualified plan, 403(b), governmental 457(b), IRA)
- After-tax rollover amounts require separate tracking for basis

**Platform requirements:** Accept incoming rollover; validate source plan type; track rollover balance separately; ensure immediate distributability flag.

---

## 6. QNEC and QMAC

**What they are:** Corrective employer contributions made to correct ADP (QNEC) or ACP (QMAC) nondiscrimination test failures.

**Key rules:**
- Must be 100% immediately vested to qualify as QNEC/QMAC
- Must satisfy specific IRS nondiscrimination requirements
- Used to increase NHCE contribution percentages to bring the plan into compliance
- Counted toward 415 annual additions limit
- May be used as the basis for ADP/ACP safe harbor contributions in lieu of a full safe harbor plan design

**Platform requirements:** Post corrective contributions to QNEC/QMAC source; ensure immediate vesting; include in 415 monitoring; generate correction documentation for EPCRS if applicable.

---

## 7. After-Tax (Non-Roth)

**What it is:** Employee after-tax contributions that are not designated as Roth. Relatively rare in modern plans.

**Key rules:**
- 100% immediately vested
- Counted toward 415 annual additions limit
- Complex distribution ordering rules: after-tax basis is not taxed; earnings on after-tax are taxable
- May be rolled out to a Roth IRA directly (after-tax basis and earnings)
- ACP test applies to after-tax contributions

**Platform requirements:** Track basis separately from earnings; apply correct tax withholding and 1099-R reporting; support ACP testing data aggregation.

---

## 8. Source Segregation Requirements

Every account / sub-account in the recordkeeping system must be tagged with a single source. The platform must:
- Maintain separate sub-account balances for each source for each participant
- Apply the correct vesting schedule to each employer source independently
- Apply the correct distribution eligibility rules based on source
- Generate 1099-R with correct distribution codes for each source distributed
- Track basis separately for Roth, after-tax, and rollover sources

---

## 9. Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Every contribution transaction must have a source tag. Never process a contribution without a source classification.
- Elective deferrals and Roth deferrals are always 100% immediately vested — this cannot be changed by plan design.
- Rollover contributions never count toward 415 annual additions and are always immediately distributable.
- QNEC and QMAC must be immediately vested to satisfy their corrective purpose.
- Never hardcode contribution limits — reference as plan-configurable per current IRS limit table.
- When a plan adds a new source type (e.g., Employer Roth, PLESA under SECURE 2.0), the platform must support the source across all downstream processing: vesting, distribution, 415 monitoring, and tax reporting.

---

## Sources

- IRC Sections 402(g), 403(b), 408, 414(v), 415 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov | Retrieved 2026-03-06
- IRS Revenue Ruling 2006-45 (Designated Roth) | https://www.irs.gov | Retrieved 2026-03-06
- ASPPA Money Type Reference | https://www.asppa.org | Retrieved 2026-03-06
