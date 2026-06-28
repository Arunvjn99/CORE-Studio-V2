# Skill: Nondiscrimination Testing
**Skill-ID:** 05-Nondiscrimination-Testing
**World:** Retirement World v1.0
**Category:** Regulatory & Compliance
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill covers the full suite of nondiscrimination and compliance tests applicable to qualified DC plans — what each test measures, who it applies to, when it runs, how failure is corrected, and what the platform must do to support testing. See also Skill 36 (Compliance-Testing) for the operational testing cycle and platform architecture.

---

## 1. Why Nondiscrimination Rules Exist

Nondiscrimination rules ensure that tax-qualified plans provide proportionate benefits to rank-and-file employees, not just owners and executives. Congress conditions the tax advantages of qualified plans on genuine broad-based employee benefit. A plan that disproportionately benefits HCEs fails the test — and must correct or lose qualified status.

---

## 2. HCE and Key Employee Definitions

### Highly Compensated Employee (HCE)

An employee is an HCE if, for the prior plan year, they:
- Were a 5%-or-greater owner at any time during the current or prior year, OR
- Received compensation exceeding the IRS-indexed HCE compensation threshold (plan-configurable parameter per current IRS limit table)

**Agent rule:** HCE compensation thresholds are IRS-indexed and must never be hardcoded. Reference as "IRS-defined HCE compensation threshold (plan-configurable per current IRS limit table)."

**Prior-year vs. current-year testing method:** Plans may elect to use the current-year or prior-year NHCE data as the comparison group. This election is a plan-configurable parameter.

### Key Employee (for Top-Heavy testing)

An employee is a Key Employee if, at any time during the plan year, they are:
- An officer with compensation exceeding the IRS-indexed officer compensation threshold (plan-configurable per IRS rules)
- A more-than-5% owner
- A more-than-1% owner with compensation exceeding the IRS-indexed 1% owner threshold (plan-configurable per IRS rules)

---

## 3. Test Types — Full Reference

### ADP Test (Actual Deferral Percentage Test)

**What it measures:** Whether HCE elective deferral percentages are proportionate to NHCE deferral percentages.

**Who it applies to:** 401(k) plans not using ADP safe harbor.

**How it works:**
- Calculate the Actual Deferral Percentage (ADP) for each eligible employee = elective deferrals / plan year compensation
- Average the ADPs for HCEs and NHCEs separately
- HCE ADP may not exceed NHCE ADP by more than the permitted spread (per IRS rules — plan-configurable per current IRS guidance)

**Testing election:** Plans may use current-year or prior-year NHCE ADP data (plan-configurable election; prior-year is default unless current-year elected).

**When it runs:** Annually at plan year end; must be corrected within IRS correction deadlines. [DATE-VERIFY — confirm current ADP correction deadline]

**Corrective actions:**
- Distribute excess contributions to HCEs (taxable in year of distribution; 10% excise tax if not corrected timely)
- Make QNEC or QMAC contributions to NHCEs
- Combination of both

### ACP Test (Actual Contribution Percentage Test)

**What it measures:** Whether HCE matching and after-tax contributions are proportionate to NHCE contributions.

**Who it applies to:** 401(k) plans with matching or after-tax contributions not using ACP safe harbor.

**How it works:** Same proportionality framework as ADP test applied to employer matching contributions and employee after-tax contributions.

**Corrective actions:** Same as ADP — excess aggregate contributions distributed to HCEs or QMAC to NHCEs.

### 415 Annual Additions Test

**What it measures:** Whether total annual additions to a participant's account exceed the IRC 415 limit.

**Who it applies to:** All qualified plans — monitored per participant.

**Annual additions include:**
- Employee elective deferrals (pre-tax and Roth)
- Employer matching contributions
- Employer non-elective contributions
- Employee after-tax contributions
- Forfeitures allocated to the participant
- Does NOT include rollover contributions or loan repayments

**Limit:** The lesser of (a) a dollar cap (plan-configurable per current IRS 415 limit table) or (b) a percentage of the participant's compensation (plan-configurable per IRS rules). Never hardcode.

**Monitoring:** Must be monitored throughout the year, not just at year end. Platform must flag approaching limits and stop contributions when the limit is reached. [COMPLIANCE-SENSITIVE]

**Corrective action:** Return excess annual additions to participant; adjust employer contributions.

### 416 Top-Heavy Test

**What it measures:** Whether the plan is top-heavy — i.e., whether Key Employee account balances exceed a regulatory threshold percentage of total plan assets (plan-configurable per IRS rules).

**Who it applies to:** All qualified plans.

**Determination date:** Generally the last day of the preceding plan year. [DATE-VERIFY]

**Consequence of top-heavy status:** If the plan is top-heavy, the employer must make a minimum contribution to non-Key Employee accounts (amount is plan-configurable per IRS minimum rules — do not hardcode).

**Safe harbor interaction:** Safe harbor 401(k) plans satisfying ADP/ACP safe harbor may be treated as satisfying the minimum contribution requirement for non-Key employees in certain circumstances. [DATE-VERIFY — confirm current interaction rules]

### 410(b) Coverage Test

**What it measures:** Whether the plan covers a sufficient percentage of non-highly compensated employees.

**Who it applies to:** All qualified plans.

**Two tests (plan must satisfy at least one):**
- **Ratio percentage test:** The percentage of NHCEs benefiting under the plan must be at least 70% of the percentage of HCEs benefiting (plan-configurable ratio per IRS rules)
- **Average benefits test:** A more complex alternative involving average benefit percentage calculations

**Controlled group aggregation:** All members of a controlled group must be aggregated for 410(b) testing. Employees of all controlled group members are treated as employed by a single employer.

### 401(a)(4) General Nondiscrimination Test

**What it measures:** Whether contributions or benefits do not discriminate in favor of HCEs, considering all plan features.

**Who it applies to:** All qualified plans; applied when ADP/ACP safe harbor is not in place.

**General test:** Contributions or benefits satisfy nondiscrimination if they are nondiscriminatory in amount and availability. Cross-testing (general test based on benefits rather than contributions) may be used for profit-sharing plans.

---

## 4. Safe Harbor Alternatives

Plans may avoid ADP and ACP testing by adopting a safe harbor design:

| Safe Harbor Type | ADP Relief | ACP Relief | Conditions |
|---|---|---|---|
| Traditional Safe Harbor | Yes | Yes (if match meets safe harbor formula) | Specified employer contributions; annual notice; immediate vesting on safe harbor contributions |
| QACA Safe Harbor | Yes | Yes (if match meets QACA formula) | Auto-enrollment; minimum default deferral; auto-escalation; up to 2-year cliff vesting |

Top-heavy testing is simplified but not fully eliminated for safe harbor plans.

---

## 5. Controlled Group Aggregation Requirements

Under IRC Section 414, all members of a controlled group (parent-subsidiary or brother-sister) or affiliated service group are treated as a single employer for qualified plan testing purposes.

**Platform must support:**
- Multi-EIN controlled group configuration
- Employee tracking across all controlled group members
- Aggregated census data for testing purposes
- Allocation of employer contributions across participating employers

[EDGE CASE — controlled group membership changes mid-year require explicit acceptance criteria]

---

## 6. HCE/NHCE Classification Workflow

The platform must perform an annual HCE determination process:
1. Identify all employees who meet HCE criteria (ownership test or prior-year compensation test) for the current plan year
2. Generate the HCE list for the plan year
3. Flag NHCE population as the complement of the HCE list among eligible employees
4. Use this classification in ADP/ACP calculations and all nondiscrimination testing

**Prior-year compensation lookback:** The HCE compensation test uses prior-plan-year compensation. The platform must maintain prior-year compensation data for each employee.

---

## 7. Corrective Actions Summary

| Test | Failure | Corrective Options | Deadline |
|---|---|---|---|
| ADP | HCE ADP too high | (1) Refund excess to HCEs; (2) QNEC to NHCEs; (3) Combination | Plan-configurable per IRS correction deadline — [DATE-VERIFY] |
| ACP | HCE ACP too high | (1) Refund excess aggregate contributions to HCEs; (2) QMAC to NHCEs | Same as ADP |
| 415 | Annual additions exceed limit | Return excess to participant; adjust employer contributions | Before plan year end or corrective contribution |
| 416 (Top-Heavy) | Plan is top-heavy | Make minimum contribution to non-Key employees | By end of plan year |
| 410(b) | Insufficient NHCE coverage | Restructure plan; include additional employees | By end of plan year with retroactive amendment |

---

## 8. Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Tag all requirements touching HCE classification, ADP/ACP testing, 415 limits, and top-heavy determinations.
- Never hardcode HCE thresholds, 415 limits, top-heavy thresholds, or any IRS-indexed value.
- Always flag controlled group scenarios as **[EDGE CASE]** requiring explicit acceptance criteria.
- Safe harbor plan design eliminates ADP/ACP testing burden — always verify safe harbor status before designing compliance testing workflows.
- Correction deadlines are regulatory — always [DATE-VERIFY] before finalizing any correction timeline requirement.

---

## Sources

- IRC Sections 401(a)(4), 401(k), 401(m), 410(b), 414, 415, 416 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- IRS Publication 560 | https://www.irs.gov/publications/p560 | Retrieved 2026-03-06
- ASPPA Compliance Testing Resources | https://www.asppa.org | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
