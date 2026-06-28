# Skill: Plan Amendment Workflow
**Skill-ID:** 25-Plan-Amendment-Workflow
**World:** Retirement World v1.0
**Category:** Plan Administration Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the plan amendment workflow — types of amendments, retroactive amendment rules, anti-cutback constraints, SECURE 2.0 amendment deadlines, and the platform implications of retroactive effective dates. Plan amendments are high-risk operations; an effective date error or an un-updated configuration can silently operate contrary to plan terms, which is itself a qualification failure.

---

## 1. Types of Plan Amendments

### Discretionary Amendments

A plan sponsor voluntarily amends the plan to change plan design — eligibility rules, contribution formulas, vesting schedules, distribution options, investment menu, loan policy, etc.

**Examples:**
- Changing the matching contribution formula
- Adding auto-enrollment
- Changing the vesting schedule (subject to anti-cutback rules)
- Adding a Roth contribution feature
- Adding PLESA accounts

### Required Amendments (Mandatory)

Laws and regulations require plan sponsors to amend their plans to reflect new rules. Failure to adopt a required amendment can result in plan disqualification.

**Examples:**
- SECURE 2.0 mandatory provisions (mandatory auto-enrollment for new plans, LTPT 2-year rule, Roth catch-up mandate)
- IRS determination letter remedial amendment cycles

**Agent rule:** [DATE-VERIFY] all SECURE 2.0 required amendment deadlines before writing requirements — SECURE 2.0 provided extended deadlines for plans that operationally implemented provisions before formal amendment.

---

## 2. Retroactive Amendment Rules

Certain plan amendments may be made retroactively to a prior plan year if adopted by the plan's amendment deadline. Retroactive amendments allow plan sponsors to make plan design changes that apply to a period that has already passed.

**Retroactive amendment conditions:**
- The amendment must be adopted by the plan's amendment deadline (plan-configurable per IRS rules; varies by amendment type) [DATE-VERIFY]
- The amendment must not reduce accrued benefits (anti-cutback rule — see Section 4)
- Operational compliance with the amendment's provisions during the retroactive period is required (the plan must have actually operated consistently with the amendment)

**SECURE 2.0 extended amendment deadlines:** SECURE 2.0 provided an extended period for plans to formally adopt amendments reflecting SECURE 2.0 provisions they operationally implemented. [DATE-VERIFY — confirm current extended amendment deadline per provision]

---

## 3. Amendment Workflow

**Step 1 — Amendment Identification**
- Plan sponsor or TPA identifies the amendment needed (discretionary change or required provision)
- Document the effective date and scope of the amendment

**Step 2 — Legal/Compliance Review**
- Confirm the amendment is permitted under the plan document and applicable law
- Verify anti-cutback compliance
- If SECURE 2.0 amendment: confirm the effective date and whether the plan has been operationally implementing the provision

**Step 3 — Adoption Agreement Update**
- Draft the amended adoption agreement or plan document
- Plan sponsor executes the amendment
- Record the amendment adoption date and effective date (these may differ)

**Step 4 — Platform Configuration Update**
- Update platform parameters to reflect the amendment
- Apply the effective date to the updated configuration
- For retroactive effective dates: configure the platform to apply the amended rules from the retroactive effective date

**Step 5 — Retroactive Recalculation (if applicable)**
- Identify all transactions affected by the retroactive effective date
- Recalculate contributions, vesting, distributions, or other affected items from the retroactive effective date forward
- Post corrective transactions to true-up participants' accounts
- Generate audit trail for all recalculated transactions

**Step 6 — Notice to Participants**
- If the amendment constitutes a material modification, generate an SMM (Summary of Material Modifications) within the required timeframe [DATE-VERIFY]
- If the amendment affects participant rights (e.g., new distribution option, vesting change), generate appropriate participant communication

**Platform requirements:**
- Version-control all adoption agreement changes with adoption date and effective date
- Maintain the ability to retrieve the plan document in effect on any given date
- Support retroactive effective date configuration with recalculation capability
- Audit trail: all configuration changes must be logged with who made the change, when, and what changed

---

## 4. Anti-Cutback Rules (ERISA Section 204(g), IRC Section 411(d)(6))

A plan amendment may not eliminate or restrict an **optional form of benefit** already accrued by a participant.

**What anti-cutback protects:**
- The right to receive a distribution in a form previously available
- The right to receive a distribution at a time previously permitted
- Vesting schedules: a plan amendment may not reduce the vested percentage of any participant (though a plan may change to an equally favorable or more favorable schedule going forward)

**Key anti-cutback implications:**
- A plan that previously allowed lump sum distributions cannot amend to eliminate lump sums for already-accrued benefits
- A plan that changes from a 6-year graded vesting schedule to a 3-year cliff must allow participants with 3+ years of service to elect the prior schedule

**Vesting schedule anti-cutback protection:**
- When a plan amends its vesting schedule to be less favorable, participants with at least 3 years of service may elect to have their vesting determined under the prior schedule [DATE-VERIFY — confirm current 3-year election rule]

**Platform requirements:**
- When processing a vesting schedule amendment, flag if the new schedule is less favorable for any participant
- Implement the prior-schedule election process for eligible participants
- Track which vesting schedule version applies to each participant

[COMPLIANCE-SENSITIVE] [RECOMMEND LEGAL/COMPLIANCE REVIEW for all amendments that may implicate anti-cutback rules]

---

## 5. Mid-Year Amendments to Safe Harbor Plans

Safe harbor plans (Traditional and QACA) face restrictions on mid-year plan amendments. Generally, mid-year amendments that reduce or eliminate safe harbor contributions are prohibited unless specific conditions are met (financial hardship of the employer, plan notice, etc.). [DATE-VERIFY — confirm current mid-year amendment rules for safe harbor plans]

**Platform implication:** When an amendment is requested for a safe harbor plan mid-year, the platform must flag the mid-year safe harbor amendment restriction for plan sponsor and TPA review before processing.

---

## 6. Retroactive Recalculation — Platform Complexity

Retroactive effective date logic is one of the most complex and high-risk platform operations:

**Risks:**
- Transaction records from the retroactive period must be identified and recalculated
- Recalculations may affect participant vesting, contribution allocations, limit monitoring results, and distributions already taken
- Distributions already processed cannot be "un-processed" — they require corrective distributions or contributions
- Tax reporting (1099-R) may need to be corrected for prior years

**Platform requirements:**
- Identify all transactions with effective dates on or after the retroactive effective date
- Apply the amended rules to recalculate affected transactions
- Post corrective transactions as new entries — never overwrite original transaction records
- Maintain the original transactions and the corrective transactions in the audit trail with clear linkage
- Generate a retroactive recalculation report showing all affected participants and the before/after impact

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Operating contrary to plan terms (even due to a delay in platform configuration) is a plan qualification failure.
- **[RECOMMEND LEGAL/COMPLIANCE REVIEW]** — All amendments with retroactive effective dates; all amendments that may implicate anti-cutback rules; all mid-year safe harbor amendments.
- **[DATE-VERIFY]** — SECURE 2.0 extended amendment deadlines must be confirmed before writing any requirement about when a plan must adopt an amendment.
- Adoption date and effective date are different concepts — the adoption date is when the amendment was signed; the effective date is when it takes effect. Both must be tracked.
- Retroactive recalculation should never overwrite original records — always post corrective transactions as new entries with links to the originals.

---

## Sources

- ERISA Section 204(g) (Anti-Cutback) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRC Section 411(d)(6) (Anti-Cutback) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 — Amendment Deadline Provisions | https://www.congress.gov | Retrieved 2026-03-06
- IRS Revenue Procedure on Plan Amendments | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
