# Skill: Eligibility Determination
**Skill-ID:** 11-Eligibility-Determination
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines how participants become eligible to participate in the plan — the rules, triggers, measurement methods, and platform workflows involved in eligibility determination. Eligibility is the gateway to enrollment; errors here prevent eligible employees from participating and create compliance exposure.

---

## 1. Eligibility Requirements

The plan's adoption agreement defines the eligibility requirements participants must meet before they can enroll. All eligibility parameters are plan-configurable within IRC and ERISA minimums and maximums.

### Age Requirement

The plan may require a participant to reach a minimum age before becoming eligible. The maximum age requirement permitted under IRC is plan-configurable per IRS rules. [DATE-VERIFY — confirm current maximum age requirement] Plans may also set a lower or no age requirement.

**Platform requirements:**
- Calculate participant age from date of birth
- Monitor for participants approaching the age threshold
- Generate eligibility alert when age threshold is met in conjunction with service requirement

### Service Requirement

The plan may require a period of service before eligibility is met, measured by:
- **Hours of service method:** The participant must complete a plan-configured minimum number of hours in a 12-month computation period.
- **Elapsed time method:** The participant must complete a period of elapsed time from their hire date (e.g., 3 months, 6 months, 1 year).

The computation period for initial eligibility begins on the employee's hire date and then shifts to the plan year. [DATE-VERIFY — confirm current computation period rules]

**Platform requirements:**
- Track hours of service per computation period (if hours method) or elapsed time (if elapsed time method)
- Monitor for service threshold completion
- Handle both computation methods per plan design

### Entry Dates

After satisfying eligibility requirements, a participant enters the plan on the next available entry date. Entry dates are plan-configurable:
- **Immediate:** Enters the plan the day eligibility requirements are met
- **First of the month:** Enters on the first day of the month following eligibility
- **First of the quarter:** Enters on the first day of the next quarter
- **Semi-annual:** Enters on the next January 1 or July 1
- **Annual:** Enters on the next January 1 (or plan year start)

**Platform requirements:**
- Calculate the projected entry date for each participant based on their hire date, eligibility requirements, and plan's entry date rule
- Generate the enrollment invitation on or before the entry date
- Track participants who have met eligibility requirements but have not yet reached their entry date (pipeline tracking)

---

## 2. Exclusion Classes

The plan may exclude certain employee classes from eligibility. Common exclusion classes (all plan-configurable; must comply with IRC nondiscrimination rules):
- Part-time employees below a plan-configured hours threshold
- Union employees covered by a collective bargaining agreement that does not include the plan
- Non-resident aliens with no U.S.-source income
- Employees under a minimum age (separate from the age requirement)
- Employees of excluded affiliated employers

**Platform requirements:**
- Configure exclusion classes per the plan's adoption agreement
- Apply exclusion logic in the eligibility determination engine
- Flag exclusion class membership on the participant record
- Note: Exclusion classes interact with LTPT rules — see below

---

## 3. LTPT Employee Tracking (SECURE 2.0 — 2-Year Rule)

[COMPLIANCE-SENSITIVE]

Under SECURE 2.0, employees who complete the plan-configurable qualifying hours threshold for **two consecutive 12-month periods** must be permitted to make elective deferrals, even if they would otherwise be excluded by a part-time exclusion class.

**Key rules:**
- The 2-year rule replaced the original SECURE Act's 3-year rule. [DATE-VERIFY — confirm effective date]
- LTPT employees must be permitted to make elective deferrals but the plan may continue to exclude them from employer contributions
- LTPT status does not grant vesting credit for years of service before the employee became eligible under LTPT rules (plan-configurable per IRS guidance) [DATE-VERIFY]
- The LTPT measurement begins with a plan-configurable 12-month period (original SECURE Act rules specified a starting date) [DATE-VERIFY]

**Platform requirements:**
- Track hours of service for all employees, including those in excluded part-time classes, across consecutive 12-month measurement periods
- Generate eligibility alert when an excluded part-time employee meets the 2-year LTPT threshold
- Flag the participant record with LTPT status
- Process LTPT entry date — the participant enters the plan on the next entry date following LTPT eligibility determination
- Maintain LTPT tracking even after the participant becomes eligible for the elective deferral source
- Suppress employer contribution eligibility for LTPT participants if the plan excludes them from employer contributions

---

## 4. 403(b) Universal Availability Rule

For 403(b) plans, the **Universal Availability Rule** under IRC Section 403(b)(12) requires that all employees be permitted to make elective deferrals unless specifically excluded by statute. The permitted exclusion classes under 403(b) are different from and more limited than those under 401(k).

**Platform requirements for 403(b) plans:**
- Apply the 403(b)-specific exclusion class list, not the 401(k) exclusion list
- Flag any attempt to exclude an employee class that is not permitted under 403(b) statute
- Track Universal Availability compliance

[COMPLIANCE-SENSITIVE]

---

## 5. Eligibility Determination Workflow

**Trigger:** New hire added to the system, or payroll/census file updates trigger a service/age milestone check.

**Process:**
1. System identifies new hire or returning employee
2. System evaluates age requirement against date of birth
3. System evaluates service requirement against hours or elapsed time data
4. System checks exclusion class membership
5. If all requirements met and no exclusion applies, system calculates the next entry date
6. System generates enrollment invitation workflow triggered on or before the entry date
7. If auto-enrollment applies, system queues auto-enrollment to take effect on the entry date
8. Participant record updated with eligibility status, projected entry date, and enrollment pending flag

**Ongoing monitoring:**
- The eligibility engine runs continuously or with each payroll cycle — not just at hire
- Employees may become eligible mid-year as they accumulate service or reach age thresholds
- LTPT employees must be monitored across consecutive plan years

---

## 6. Compliance Obligations Triggered by Eligibility

- Enrollment materials must be provided to newly eligible employees within ERISA-required timeframes
- Auto-enrollment notice must be provided (if auto-enrollment plan)
- QDIA notice must be provided (if QDIA auto-investment applies)
- Safe harbor notice must be provided (if safe harbor plan)

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — LTPT eligibility tracking is a SECURE 2.0 mandatory requirement. Failure to enroll eligible LTPT employees is a plan qualification failure.
- **[EDGE CASE]** — LTPT tracking requires multi-year hours accumulation logic. Explicit acceptance criteria required for LTPT implementations.
- Never hardcode age or service thresholds — always reference as plan-configurable parameters.
- 403(b) eligibility logic must use 403(b)-specific exclusion classes — do not copy 401(k) eligibility configuration without adjustment.
- Eligibility determination must run continuously, not just at hire — employees become eligible at various points throughout the year.

---

## Sources

- IRC Section 410(a) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022, Section 125 (LTPT) | https://www.congress.gov | Retrieved 2026-03-06
- IRC Section 403(b)(12) (Universal Availability) | IRS | https://www.irs.gov | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
