# Skill: Vesting Framework
**Skill-ID:** 06-Vesting-Framework
**World:** Retirement World v1.0
**Category:** Regulatory & Compliance
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the vesting framework for DC plans — vesting schedule types, service calculation methods, forfeiture mechanics, and the edge cases that arise in break-in-service and rehire scenarios. Vesting determines how much of a participant's employer contributions are non-forfeitable and drives distribution and loan eligibility calculations.

---

## 1. What Vesting Is

**Vesting** is the process by which a participant acquires a non-forfeitable right to employer contributions in their account. Before a participant is fully vested in an employer contribution source, the unvested portion is subject to forfeiture upon termination of employment.

**Critical rule — elective deferrals are always 100% vested immediately.** This is a statutory requirement, not a plan design choice. It applies to all employee pre-tax and Roth elective deferrals. [COMPLIANCE-SENSITIVE]

---

## 2. Vesting Schedule Types

### Immediate Vesting

The participant is 100% vested in employer contributions from the date contributed. The plan chooses immediate vesting as its plan design; no schedule is needed.

**Common for:** Employer non-elective contributions in some plans; mandatory for safe harbor employer contributions in Traditional Safe Harbor plans.

### Cliff Vesting

The participant becomes 100% vested after completing a plan-configured number of years of service. **Zero vesting accrues before that cliff point.** The maximum cliff for employer matching contributions in a DC plan is plan-configurable per IRC vesting schedule limits. [DATE-VERIFY — confirm current maximum cliff vesting periods]

**Example concept:** A participant with a 3-year cliff schedule has 0% vested for years 1 and 2, and 100% vested on the first day of year 3. If they terminate in year 2, they forfeit all employer contributions.

### Graded Vesting

The participant vests incrementally — a plan-configured percentage per year of service — until reaching 100%. The maximum graded vesting schedule is plan-configurable per IRC limits. [DATE-VERIFY — confirm current maximum graded vesting schedule]

**Example concept:** A 6-year graded schedule might vest 20% per year starting in year 2, reaching 100% in year 6.

### QACA Safe Harbor Vesting

A QACA (Qualified Automatic Contribution Arrangement) safe harbor plan is permitted to use up to a 2-year cliff vesting schedule for safe harbor employer contributions. This is an exception to the usual immediate vesting requirement for safe harbor contributions in Traditional Safe Harbor plans.

---

## 3. Service Calculation Methods

The plan document must specify which method is used to calculate vesting service.

### Hours of Service Method

Years of vesting service are counted based on hours worked (and hours for which pay is received or due) in a computation period (typically a 12-month period). An employee who completes the plan-configured minimum number of hours in a computation period earns a year of vesting service.

**Platform requirements:**
- Track hours of service per participant per computation period
- Source data: payroll or HR system
- Apply the plan-configured hours threshold to determine whether a year of service is earned
- Accumulate years of vesting service over the participant's history

### Elapsed Time Method

Vesting service is measured by the period of time elapsed between the hire date (or other applicable start date) and the date of severance from service, regardless of hours worked. Each plan year (or month, depending on plan design) of elapsed time counts as a year of service.

**Platform requirements:**
- Calculate elapsed time from hire date to termination (or current date for active employees)
- No hours tracking required
- More straightforward calculation but captures all time even during low-hours periods

---

## 4. Vesting Percentage Calculation

The platform must calculate each participant's vested percentage for each employer contribution source separately, because:
- Different employer contribution sources (match, non-elective, profit sharing) may have different vesting schedules
- A plan may have multiple vesting schedules in effect simultaneously for different sources or different plan years (due to amendments)
- The vested percentage drives the distributable balance and the loan collateral available

**Vested balance = Account balance in source × Vested percentage for that source**

The platform must maintain a vesting record per participant per source and update it whenever:
- A new year of vesting service is earned
- The participant terminates employment (finalize vesting)
- The plan is amended (may prospectively or retroactively change vesting schedule — see anti-cutback rules)
- The participant is rehired (service restoration may apply)

---

## 5. Forfeiture Mechanics

When a participant terminates employment without being fully vested in employer contribution sources, the unvested portion is **forfeited** to the plan's forfeiture account.

**Timing of forfeiture:** Forfeitures are generally processed after the participant receives a distribution of their vested balance, or (if no distribution is taken) after the participant incurs a plan-configured number of consecutive breaks in service. [DATE-VERIFY — confirm current forfeiture timing rules]

**Forfeiture account permitted uses (plan-configurable):**
- Reduce employer contributions
- Pay plan expenses
- Fund QNECs or QMACs
- Reallocate to remaining participants (if plan document permits)

**Timing of forfeiture usage:** Forfeitures must be used within the plan year they arise or the following plan year (plan-configurable per plan document and IRS guidance). [DATE-VERIFY — confirm forfeiture usage timing rules]

---

## 6. Break-in-Service Rules

A **break in service** occurs when a former employee does not complete the minimum hours of service (or equivalent under elapsed time method) in a plan year or computation period.

### One-Year Break in Service

A participant incurs a one-year break in service if they fail to complete the plan-configured minimum hours in a computation period.

**Effect:** Pause in vesting service accrual during the break period.

### Permanent Break in Service (Rule of Parity)

Under the Rule of Parity, if the number of consecutive one-year breaks equals or exceeds the greater of (a) five or (b) the participant's pre-break years of vesting service, the break is permanent and pre-break service need not be restored upon rehire.

**Platform must:**
- Track consecutive break years per participant
- Determine when the Rule of Parity threshold is met
- Flag participants approaching permanent break status

[EDGE CASE — break-in-service and service restoration rules for each implementation require explicit acceptance criteria]

### Maternity/Paternity Leave Protection

Hours of service must be credited for absences due to pregnancy, childbirth, or child adoption (up to a plan-configurable maximum hours) solely to prevent a break in service. [DATE-VERIFY — confirm current maternity/paternity leave rules]

---

## 7. Rehire and Service Restoration

Upon rehire, the platform must evaluate:

1. **Did a permanent break in service occur?** If not, prior vesting service must be restored.
2. **Was prior unvested balance forfeited?** If the participant returns before a permanent break in service (or meets the service threshold to restore), the plan may be required to restore the forfeiture from the forfeiture account.
3. **What is the participant's vesting schedule?** If the plan amended its vesting schedule after the prior termination, determine which schedule applies to pre-break and post-rehire service.

[EDGE CASE — rehire vesting scenarios require explicit acceptance criteria for every implementation]

---

## 8. Anti-Cutback Rules (ERISA Section 204(g))

A plan amendment may not eliminate or restrict an optional form of benefit already accrued. For vesting purposes, a plan amendment that reduces the vesting schedule must provide that participants with at least three years of service may elect to have their vesting determined under the prior schedule. [DATE-VERIFY — confirm current anti-cutback vesting rules]

**Platform implication:** When processing plan amendments that change the vesting schedule, the platform must:
- Apply the new schedule prospectively for new contributions
- Honor the prior schedule for participants who elect it under the anti-cutback protection
- Track which vesting schedule version applies to each participant

---

## 9. Plan Termination — Full Vesting

Upon plan termination, **all participant accounts must become 100% vested** regardless of years of vesting service. [COMPLIANCE-SENSITIVE]

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Elective deferrals are always 100% immediately vested; this cannot be modified by plan design.
- Never hardcode vesting schedule maximums — reference as plan-configurable per current IRC vesting requirements.
- Always treat break-in-service and rehire vesting as **[EDGE CASE]** requiring explicit acceptance criteria.
- Anti-cutback rules apply to vesting schedule amendments — flag for legal review if a plan amendment reduces vesting. **[RECOMMEND LEGAL/COMPLIANCE REVIEW]**
- Vested balance drives distribution eligibility and loan collateral — errors in vesting calculations propagate to distribution and loan processing.

---

## Sources

- IRC Sections 411, 414 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- ERISA Sections 203, 204 | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DOL Regulations 29 CFR Part 2530 (Hours of Service) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Vesting Resources | https://www.asppa.org | Retrieved 2026-03-06
