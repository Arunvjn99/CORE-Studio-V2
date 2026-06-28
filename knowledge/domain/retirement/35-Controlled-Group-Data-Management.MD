# Skill: Controlled Group Data Management
**Skill-ID:** 35-Controlled-Group-Data-Management
**World:** Retirement World v1.0
**Category:** Implementation & Data Integration
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the data architecture requirements for controlled group plans — multi-EIN structures, cross-employer service tracking, aggregated compliance testing, and contribution allocation. Controlled group rules are foundational to nondiscrimination testing and plan qualification; errors in controlled group data management produce systematic testing failures.

---

## 1. What a Controlled Group Is

Under IRC Section 414, all employers under common ownership (above a specified ownership threshold) are treated as a **single employer** for qualified retirement plan purposes. This means all employees of controlled group members must be counted for eligibility, vesting, and nondiscrimination testing purposes.

**Types of controlled groups:**

| Type | Definition |
|---|---|
| **Parent-Subsidiary Controlled Group** | A chain of organizations where the common parent owns more than a specified ownership threshold in each subsidiary (threshold is IRS-defined — do not hardcode) |
| **Brother-Sister Controlled Group** | Two or more organizations where the same five or fewer individuals own more than a specified percentage, with a specified minimum direct ownership by each (thresholds are IRS-defined) |
| **Combined Group** | A combination of parent-subsidiary and brother-sister groups |

**Affiliated Service Groups:** Organizations not technically in a controlled group but linked through service relationships may be treated as a single employer for plan purposes under IRC Section 414(m). Similar aggregation rules apply.

[DATE-VERIFY — confirm current ownership threshold requirements for each controlled group type]

---

## 2. Why Controlled Group Data Matters for Plan Administration

Without aggregating controlled group data:
- Employees of related employers are not counted for nondiscrimination testing → tests may pass when they should fail
- Employees of related employers may be excluded from eligibility when they should be included → qualification failure
- Contribution limits may not be calculated correctly across all plans → 415 violations

**Agent rule:** Every plan with a controlled group or affiliated service group relationship must be flagged for controlled group data management requirements.

---

## 3. Multi-EIN Data Architecture

Each employer in a controlled group has its own EIN. The platform must:
- Maintain a separate Employer record for each EIN in the controlled group
- Link all EINs in the controlled group to a "controlled group" parent configuration
- Track all employees by their employing EIN

**Platform requirements:**
- Support multi-EIN employer configurations linked to a controlled group
- Assign each participant record to their employing EIN
- Maintain the controlled group membership roster (which EINs are in the group, effective dates of membership)
- Support controlled group membership changes (acquisitions, divestitures change the composition of the group) with effective dates

[EDGE CASE — controlled group membership changes mid-year require explicit acceptance criteria for testing and eligibility]

---

## 4. Cross-Employer Service Tracking

Under IRC Section 414, service with any member of the controlled group must be counted as service with the current employer for:
- **Eligibility:** Prior service with a controlled group member counts toward eligibility service
- **Vesting:** Prior service with a controlled group member counts toward vesting service
- **Break-in-service:** Transfer between controlled group members does not cause a break in service

**Example concept:** An employee who worked for Company A (a controlled group member) for 2 years before transferring to Company B (another controlled group member) has 2 years of prior service credit at Company B for eligibility and vesting purposes.

**Platform requirements:**
- Track service history per participant across all employing EINs in the controlled group
- When a participant transfers between controlled group members:
  - Preserve prior service credit from the prior employer
  - Apply the prior service to eligibility and vesting at the new employer
  - Do not treat the transfer as a termination and rehire
- Service history must span the participant's entire controlled group employment history

---

## 5. Aggregated Compliance Testing

All members of a controlled group are treated as a single employer for ADP, ACP, 415, 416, 410(b), and 401(a)(4) testing. This means:
- All employees of controlled group members (whether or not they participate in the same plan) are counted in the eligible employee base
- HCE and NHCE classification is determined on a controlled group basis (not just within a single EIN)
- Coverage testing (410(b)) considers all controlled group employees

**If controlled group members sponsor separate plans:**
- Each plan must independently satisfy coverage and nondiscrimination testing
- However, the eligible employee base for each plan's testing includes all controlled group employees
- Plans may be required to be aggregated for testing if they fail independently but pass on an aggregated basis

**Platform requirements:**
- Support aggregated census data collection across all EINs in the controlled group
- Generate controlled group-wide HCE determination (using combined compensation and ownership data)
- Perform compliance testing using the aggregated eligible employee base
- Support plan-level testing results while flagging that the controlled group context was applied

---

## 6. Contribution Allocation Across Controlled Group Members

If a single plan covers employees of multiple controlled group members (common in MEP structures or where a plan sponsor covers employees of related entities):
- Each employer's contribution formula may differ within the plan document's parameters
- Employer contributions must be tracked by the contributing EIN
- Funding must be received separately from each EIN

**Platform requirements:**
- Support multi-EIN contribution tracking within a single plan
- Accept contribution files or API payloads from each EIN separately
- Allocate employer contributions to the correct EIN's participants
- Reconcile funding from each EIN separately

---

## 7. 415 Limit Application Across Controlled Group

Under IRC Section 415, the annual additions limit is applied on an employer basis, aggregating all qualified plans of the same employer (and all controlled group members are treated as a single employer).

**Implication:** A participant in two plans sponsored by different EINs in the same controlled group has their annual additions aggregated across both plans for the 415 limit.

**Platform requirements:**
- If a participant participates in multiple plans within the same controlled group, aggregate their annual additions across all plans for 415 monitoring
- Alert and correct when the combined annual additions across all plans would exceed the 415 limit

[COMPLIANCE-SENSITIVE]

---

## 8. PEP and MEP Controlled Group Considerations

In a Pooled Employer Plan (PEP) or Multiple Employer Plan (MEP), each participating employer may or may not be part of a controlled group with other participating employers.
- The PEP/MEP structure itself does not create a controlled group relationship between participating employers
- Each employer's employees are tested separately unless they are independently in a controlled group

**Platform requirements:**
- Support employer-level segmentation within a PEP/MEP structure
- Apply controlled group aggregation only for EINs that are genuinely in a controlled group with each other
- Do not aggregate unrelated PEP/MEP participating employers for testing purposes

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Controlled group aggregation is mandatory for compliance testing. Failure to aggregate results in testing on an incomplete eligible employee base, which can produce false passes.
- **[EDGE CASE]** — Controlled group membership changes mid-year (acquisitions, divestitures) require explicit acceptance criteria. A company joining or leaving the controlled group mid-year creates a complex partial-year testing scenario.
- Cross-employer service credit must be preserved at transfer — do not process a controlled group employee transfer as a termination and rehire.
- 415 limit aggregation across controlled group plans is mandatory — this requires the platform to know about all plans a participant participates in within the controlled group.
- Never hardcode controlled group ownership thresholds — reference as IRS-defined parameters.

---

## Sources

- IRC Sections 414(b), 414(c), 414(m) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- IRC Section 415(g) (415 Controlled Group Aggregation) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Controlled Group Resources | https://www.asppa.org | Retrieved 2026-03-06
