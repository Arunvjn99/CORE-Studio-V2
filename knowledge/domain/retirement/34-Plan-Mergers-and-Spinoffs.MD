# Skill: Plan Mergers and Spinoffs
**Skill-ID:** 34-Plan-Mergers-and-Spinoffs
**World:** Retirement World v1.0
**Category:** Implementation & Data Integration
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines plan merger and spinoff mechanics — what they are, what data and financial operations they require, the anti-cutback constraints that apply, and why they are among the most complex events in plan administration. Mergers and spinoffs are infrequent but high-risk; errors have plan-wide consequences.

---

## 1. What Plan Mergers and Spinoffs Are

### Plan Merger

A plan merger is the combination of two or more plans into a single surviving plan. All participant accounts, assets, and liabilities from the merging plans are transferred to the surviving plan.

**Common triggers:**
- Corporate merger or acquisition
- Simplification of multiple plans into one
- Transition from one plan type to another (e.g., merging a profit-sharing plan into a 401(k))

### Plan Spinoff

A plan spinoff is the separation of a portion of a plan into a new standalone plan. A subset of participants and their associated assets are transferred from the original plan to the new plan.

**Common triggers:**
- Corporate divestiture (a business unit is sold and its employees are spun off to a new plan sponsored by the acquiring employer)
- Separation of a plan segment for administrative or design purposes

---

## 2. Regulatory Requirements for Mergers and Spinoffs

**IRC Section 414(l) — Non-Diminishment Rule:**

In a merger or spinoff, each participant must receive a benefit immediately after the event that is at least equal to the benefit they had immediately before. This is the **non-diminishment rule** — no participant can lose benefits as a result of a merger or spinoff.

**Anti-cutback rule (ERISA Section 204(g) / IRC Section 411(d)(6)):**

A merger or spinoff may not eliminate or restrict an optional form of benefit that was available to participants in the prior plan. If the surviving plan does not offer a distribution option that was available in the merged plan, an anti-cutback analysis must be performed.

[RECOMMEND LEGAL/COMPLIANCE REVIEW for all merger and spinoff transactions]

---

## 3. Merger Workflow

**Step 1 — Transaction Documentation**
- Board resolutions from both plan sponsors
- Merger agreement
- Analysis of plan design differences between the merging plans
- Anti-cutback analysis

**Step 2 — Participant Communication**
- Notify participants in the merging plan of the merger and the effective date
- Provide information about any changes to plan design that result from the merger
- If a blackout period is required, issue ERISA 101(i) blackout notice at least 30 days in advance [DATE-VERIFY]

**Step 3 — Plan Design Harmonization**
- Review the design differences between the merging plans (eligibility, vesting schedules, distribution options, investment menu)
- Determine which design will apply in the surviving plan
- Prepare plan amendments to harmonize design, subject to anti-cutback constraints

**Step 4 — Asset Transfer and Reconciliation**
- Transfer all assets from the merging plan's trust to the surviving plan's trust
- Reconcile transferred assets to the merging plan's final account balances by participant and by fund
- Confirm receipt with the surviving plan's custodian

**Step 5 — Data Migration**
- Transfer participant records (demographics, account balances by source and fund, vesting service history, loan data, beneficiary designations) from the merging plan to the surviving plan
- Validate all migrated data against the merging plan's final records

**Step 6 — Compliance Testing on the Surviving Plan**
- The merged plan must perform compliance testing (ADP, ACP, 415, 416, 410(b)) for the plan year in which the merger occurs, using data from both plans for the entire plan year
- If the merger occurs mid-year, testing may need to be performed on the merged group for the full plan year

**Step 7 — Form 5500 Filing**
- The merging plan files a final Form 5500 marked as a final filing
- The surviving plan reports the absorbed assets and participants in its annual filing

---

## 4. Spinoff Workflow

**Step 1 — Transaction Documentation**
- Plan sponsor authorization for the spinoff
- Identification of the participant group being spun off (by business unit, EIN, or other criteria)
- Anti-cutback analysis for the new plan's design vs. the original plan's design

**Step 2 — New Plan Establishment**
- New plan document and adoption agreement for the spun-off plan
- New custodian/trust account established (or specified)
- New recordkeeping configuration for the new plan

**Step 3 — Asset and Data Segregation**
- Identify the assets attributable to the spun-off participants in the original plan
- Transfer the spun-off participants' account balances (by source and by fund) to the new plan's trust
- Reconcile the transfer to both the original plan's and the new plan's trust statements

**Step 4 — Participant Record Transfer**
- Transfer participant records for the spun-off participants to the new plan's recordkeeping system
- Update employment data to reflect the new plan sponsor

**Step 5 — Compliance Testing**
- The original plan and the new plan must separately satisfy compliance testing for the plan year of the spinoff
- Short plan year testing rules may apply if the spinoff occurs mid-year [EDGE CASE — short plan year testing requires explicit acceptance criteria]

---

## 5. Anti-Cutback Analysis

Before any merger or spinoff is executed, the plan administrator (typically with legal counsel) must perform an anti-cutback analysis:
1. Document all optional forms of benefit available in the plans involved
2. Identify any optional forms that will not be available in the surviving or new plan
3. Determine whether grandfathering of eliminated optional forms is required
4. Prepare the plan amendment to address anti-cutback requirements

[RECOMMEND LEGAL/COMPLIANCE REVIEW — anti-cutback analysis must be performed by qualified legal/compliance professionals]

---

## 6. Platform Requirements for Mergers and Spinoffs

**For mergers:**
- Support intake of a second plan's participant data (all sources, all funds) into the surviving plan
- Merge participant records (avoiding duplicate SSNs — if a participant was in both plans, consolidate correctly)
- Maintain prior plan source/money type mappings in the surviving plan's configuration
- Track which participants came from which original plan for testing purposes

**For spinoffs:**
- Support export of a defined subset of participant records and balances to a new plan
- Verify that the exported balances reconcile to the original plan's records minus the exported amounts
- Close the spun-off participants' records in the original plan
- Establish the spun-off participants in the new plan with their historical data intact

**For both:**
- Maintain audit trail of all data transferred (participant-level, source-level, fund-level)
- Support the compliance testing data requirements for the plan year of the merger/spinoff

---

## Agent Rules

- **[EDGE CASE]** — Plan mergers and spinoffs require explicit acceptance criteria for data integrity, anti-cutback compliance, and compliance testing. Never include merger/spinoff in a generic feature without dedicated edge case handling.
- **[RECOMMEND LEGAL/COMPLIANCE REVIEW]** — All merger and spinoff transactions require legal and tax counsel involvement.
- Anti-cutback analysis must be completed before any merger or spinoff is executed — not after.
- Short plan years arising from mid-year mergers/spinoffs have specialized compliance testing rules. [EDGE CASE]
- If a participant appears in both the merging plan and the surviving plan, careful record deduplication is required to avoid creating duplicate participant accounts.

---

## Sources

- IRC Section 414(l) (Merger and Spinoff Non-Diminishment) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- ERISA Section 204(g) (Anti-Cutback) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRS Revenue Ruling 81-27 (Plan Mergers) | https://www.irs.gov | Retrieved 2026-03-06
- ASPPA Plan Merger and Spinoff Resources | https://www.asppa.org | Retrieved 2026-03-06
