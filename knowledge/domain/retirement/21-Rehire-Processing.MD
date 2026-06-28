# Skill: Rehire Processing
**Skill-ID:** 21-Rehire-Processing
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the platform workflows triggered when a former employee is rehired — break-in-service analysis, prior service credit restoration, forfeiture restoration eligibility, and re-eligibility determination. Rehire is one of the most complex edge cases in participant administration; errors cascade into vesting, eligibility, and forfeiture errors.

---

## 1. Rehire Event — Data Requirements

Rehire requires the following data inputs before processing can begin:
- Rehire date (from payroll or census file)
- Prior termination date (from existing participant record)
- Prior vesting service history (from existing participant record)
- Prior forfeiture amounts (from forfeiture account records, if any were taken)
- Prior break-in-service history

**Platform requirements:**
- Upon receipt of a rehire date, identify the participant's prior record
- Do not create a new participant record — reactivate the existing record
- Link the rehire record to all prior service, vesting, and contribution history

---

## 2. Break-in-Service Analysis

A **break in service** occurs when a former employee does not complete the plan-configured minimum hours of service (or equivalent under elapsed time method) in a computation period. Break-in-service analysis determines what prior service must be restored.

### Step 1: Count Consecutive One-Year Breaks

Calculate the number of consecutive years of break in service between the termination date and the rehire date.

### Step 2: Apply the Rule of Parity (Permanent Break Determination)

A permanent break in service occurs when the number of consecutive one-year breaks equals or exceeds the greater of:
- (a) 5, or
- (b) The number of years of vesting service the employee earned before the break

**If a permanent break has occurred:** Prior service need not be restored. The rehired employee is treated as a new employee for vesting purposes. Prior forfeited amounts need not be restored.

**If no permanent break has occurred:** Prior vesting service must be restored upon rehire (see Section 3).

[EDGE CASE — break-in-service permanent break calculations require explicit acceptance criteria for every implementation]

### Elapsed Time Method Breaks

Under the elapsed time method, a break in service begins on the date of severance and ends on the rehire date. The break period is measured in months or years. Special rules apply for maternity/paternity leave and other qualifying absences.

---

## 3. Prior Service Credit Restoration

If no permanent break in service occurred, the platform must restore prior vesting service to the participant's record.

**Service restoration process:**
1. Retrieve the prior vesting service history from the participant record
2. Add the pre-break years of vesting service back to the participant's vesting service count
3. Recalculate the vesting percentage for each employer contribution source using the restored total years of service
4. If the restored vesting percentage exceeds the currently recorded vesting percentage, update the vesting record
5. Log the service restoration event with full audit trail

**Platform requirements:**
- Retrieve prior vesting service records
- Restore years of service for each source
- Recalculate vesting percentages
- Update vesting records with effective date of restoration (rehire date)
- Generate notification to plan sponsor or TPA of service restoration

---

## 4. Forfeiture Restoration Eligibility

If a rehired employee's prior unvested balance was forfeited, the forfeiture may need to be restored if:
- The employee returns before a permanent break in service has occurred, AND
- The employee repays the distribution received (if a distribution was made and the employee was subsequently rehired before permanent break) — this requirement applies only if the participant received a distribution at termination

**Restoration mechanics:**
- The restored amount comes from the plan's forfeiture account
- If the forfeiture account has insufficient funds, the employer may be required to contribute additional amounts to fund the restoration

[DATE-VERIFY — confirm current forfeiture restoration rules; IRS has issued guidance on timing and funding obligations]

**Platform requirements:**
- Identify prior forfeiture amounts from forfeiture account records
- Determine whether forfeiture restoration is required based on break-in-service analysis and distribution history
- If restoration required, calculate the restoration amount
- Fund the restoration from the forfeiture account
- Update the participant's vesting record and account balance
- Log the forfeiture restoration with full audit trail

[EDGE CASE — forfeiture restoration requires explicit acceptance criteria]

---

## 5. Re-Eligibility Determination

Upon rehire, the platform must determine whether the participant is immediately eligible to participate or must satisfy eligibility requirements again.

**Factors affecting re-eligibility:**
- Whether the participant satisfied eligibility requirements during prior employment
- Whether the break in service was permanent
- The plan document's re-eligibility rules (which are plan-configurable)

**Common re-eligibility outcomes:**
- **Immediate re-eligibility:** If the participant previously satisfied all eligibility requirements and no permanent break occurred, the participant may be immediately eligible upon rehire
- **Must re-satisfy service requirement:** If a permanent break occurred, the participant may be treated as a new employee and must re-satisfy eligibility requirements
- **Elapsed time credit:** Under elapsed time method, prior elapsed time may count toward re-eligibility

**Platform requirements:**
- Evaluate re-eligibility based on plan document rules and break-in-service analysis
- If immediately eligible, trigger enrollment workflow upon rehire
- If re-eligibility required, restart eligibility tracking from the rehire date
- Flag LTPT tracking requirements (LTPT hours history must continue for employees previously in part-time exclusion class)

---

## 6. Multiple Prior Terminations

A participant may have multiple prior periods of employment with the same employer. The platform must handle:
- Multiple sets of prior service records
- Multiple break-in-service periods
- Stacked service restoration (each rehire may restore different layers of service)
- Multiple prior forfeiture events

[EDGE CASE — multiple prior terminations require explicit acceptance criteria for service stacking and forfeiture restoration]

---

## 7. USERRA — Military Service

Under the Uniformed Services Employment and Reemployment Rights Act (USERRA), employees returning from military service have special rehire rights:
- The employee must be reemployed within specific USERRA timeframes based on the length of service
- Upon reemployment, the employee is treated as if they had been continuously employed for purposes of vesting, eligibility, and accruals
- The employer may be required to make contributions for the military service period
- The employee has the right to make elective deferrals for the period of military absence within a window period after return

[DATE-VERIFY — confirm current USERRA contribution and makeup rules]

**Platform requirements:**
- Flag military leave status on the participant record
- Apply USERRA service credit upon return from military leave
- Support elective deferral makeup contributions for the military leave period
- Calculate and process employer makeup contributions if required

[COMPLIANCE-SENSITIVE]

---

## Agent Rules

- **[EDGE CASE]** — Rehire vesting scenarios are a primary source of production defects in retirement administration systems. Every rehire implementation must include explicit acceptance criteria for break-in-service analysis, service restoration, and forfeiture restoration.
- **[EDGE CASE]** — Multiple prior terminations compound the complexity. Flag for dedicated testing scenarios.
- Never create a new participant record for a rehired employee — reactivate the existing record to preserve prior service history.
- USERRA obligations are separate from and in addition to normal plan re-eligibility rules — always check for military service flag when processing a rehire.
- Forfeiture restoration requires funding from the forfeiture account — the platform must check forfeiture account balance before committing to a restoration.

---

## Sources

- IRC Sections 410(a), 411 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL Regulations 29 CFR Part 2530 (Service for Benefit Accrual and Vesting) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- USERRA (38 U.S.C. §§ 4301–4335) | https://www.dol.gov/agencies/vets/programs/userra | Retrieved 2026-03-06
- ERISA Section 203 (Vesting) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
