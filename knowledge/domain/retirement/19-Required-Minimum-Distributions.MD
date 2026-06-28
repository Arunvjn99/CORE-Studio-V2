# Skill: Required Minimum Distributions (RMD)
**Skill-ID:** 19-Required-Minimum-Distributions
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the RMD rules for DC plans — required beginning dates, calculation methodology, the still-working exception, Roth exemption, beneficiary rules, and automated platform workflows. RMD compliance is a high-stakes area; failure to distribute the correct amount by the required deadline triggers an IRS excise tax on the participant.

---

## 1. What RMDs Are

A Required Minimum Distribution (RMD) is the minimum amount that a participant must withdraw from their retirement account each year after reaching the required beginning date. The purpose is to ensure that tax-deferred retirement savings are eventually distributed and taxed.

---

## 2. Required Beginning Date (RBD)

The Required Beginning Date is the deadline by which a participant must receive their first RMD.

**RBD rule:** April 1 of the calendar year following the later of:
- The calendar year in which the participant reaches the required beginning age (plan-configurable per current IRS RMD age rules — modified by SECURE 2.0; do not hardcode the age), OR
- The calendar year in which the participant retires (if the still-working exception applies — see Section 4)

**SECURE 2.0 RMD age increases:** SECURE 2.0 increased the required beginning age in stages based on the participant's birth year. The applicable age differs by birth year cohort. [DATE-VERIFY — confirm current required beginning age for each birth year cohort]

**Platform requirements:**
- Calculate the RBD for each participant using the participant's date of birth and current employment status
- Apply the correct required beginning age based on the participant's birth year
- Track participants approaching their RBD (generate alerts at a configurable look-ahead window)
- Trigger RMD processing workflow when the RBD is reached

---

## 3. RMD Amount Calculation

The annual RMD amount is calculated as:

**RMD = Account balance as of December 31 of the prior year ÷ Applicable distribution period (life expectancy factor from IRS tables)**

**IRS Life Expectancy Tables:** The applicable factor is drawn from IRS-prescribed tables (Uniform Lifetime Table for most participants; Joint Life and Last Survivor Table if sole beneficiary is a spouse more than 10 years younger). The tables are IRS-published parameters — reference as plan-configurable per current IRS life expectancy tables; do not hardcode.

**Account balance used:** The December 31 prior-year balance, adjusted for:
- Outstanding loan balances (loan balances are generally not subtracted — the full account balance is used)
- Any outstanding rollover/transfer amounts that have not yet been received by December 31

**First RMD timing:**
- The first RMD may be deferred to April 1 of the year following the year the participant reaches RBD age
- All subsequent RMDs must be distributed by December 31 of each calendar year
- Deferring the first RMD results in two RMDs in the same calendar year (one by April 1 and one by December 31) — this may push the participant into a higher tax bracket and should be disclosed

**Platform requirements:**
- Calculate December 31 prior-year balance for each participant subject to RMD
- Apply the correct IRS life expectancy factor based on the participant's age and beneficiary status
- Calculate the annual RMD amount
- Generate RMD processing request
- Track RMD amounts distributed vs. required for each plan year

---

## 4. Still-Working Exception

A participant who is still employed by the plan sponsor after reaching RMD age (other than 5%-or-greater owners) may defer RMDs from that employer's plan until they terminate employment, if the plan permits this exception.

**5% owner rule:** 5%-or-greater owners must begin RMDs at the required beginning age regardless of employment status. There is no still-working exception for 5% owners.

**Platform requirements:**
- Track employment status for participants at or above RMD age
- Apply the still-working exception to defer RMD processing for eligible active employees
- Identify 5%-or-greater owners and exclude them from the still-working exception
- Trigger RMD processing immediately upon termination of employment for participants who were previously deferred under the still-working exception

---

## 5. Designated Roth Accounts — No Lifetime RMD

Under SECURE 2.0, designated Roth accounts in employer plans (401(k), 403(b)) are exempt from lifetime RMDs for the participant. This aligns with Roth IRA treatment. [DATE-VERIFY — confirm effective year]

**Platform requirements:**
- Exclude designated Roth source balances from the RMD calculation base for living participants
- Suppress RMD distribution triggers for Roth source balances
- Note: RMD rules DO apply to Roth balances inherited by beneficiaries after the participant's death

[COMPLIANCE-SENSITIVE]

---

## 6. Death Distributions and Beneficiary RMD Rules

Upon a participant's death, the RMD rules for beneficiaries depend on:
- Type of beneficiary (eligible designated beneficiary vs. designated beneficiary vs. non-designated beneficiary)
- Whether the participant died before or after their required beginning date
- The SECURE Act 10-year rule for non-eligible designated beneficiaries

### Eligible Designated Beneficiaries (EDBs)

EDBs may use their own life expectancy for distributions (not subject to the 10-year rule):
- Surviving spouse
- Minor child of the participant (until reaching majority)
- Disabled individual
- Chronically ill individual
- Individual not more than 10 years younger than the participant

### Designated Beneficiaries (Non-EDB)

Subject to the SECURE Act 10-year rule: the entire account must be distributed by December 31 of the 10th year following the participant's death. Annual distributions are not required within the 10-year period (for participants who died before their RBD). [DATE-VERIFY — IRS has issued regulations on the 10-year rule; confirm current interpretation]

### Non-Designated Beneficiaries (Estates, Charities, Non-Qualifying Trusts)

- If the participant died before RBD: 5-year rule — entire account must be distributed within 5 years
- If the participant died after RBD: distributions based on the participant's remaining life expectancy

[COMPLIANCE-SENSITIVE — recommend legal/compliance review for all beneficiary RMD scenarios]

**Platform requirements:**
- Determine beneficiary type upon death notification
- Apply the correct RMD distribution rule based on beneficiary type and participant's RBD status
- Track annual RMD requirements for beneficiary accounts
- Generate beneficiary RMD processing requests

---

## 7. RMD Excise Tax for Underdistribution

If a participant fails to receive the full RMD by the required deadline, the undistributed amount is subject to an IRS excise tax. SECURE 2.0 reduced this penalty rate (plan-configurable parameter per current IRS penalty rules — do not hardcode the rate). [DATE-VERIFY — confirm current penalty rate]

**Platform requirements:**
- Track RMD compliance per participant per year
- Identify undistributed RMD amounts after the deadline
- Generate alert for plan sponsor and/or participant
- Support correction of RMD shortfall as part of IRS correction procedures

---

## 8. Aggregation Across Plans

RMDs from multiple qualified plans of the same employer may generally not be aggregated — each plan must separately satisfy its RMD requirement. However, IRAs may be aggregated for RMD purposes.

**Platform requirement:** The platform calculates and tracks RMDs at the plan level. Do not aggregate with other plans or IRAs in the RMD calculation.

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — RMD rules are mandatory. Failure to distribute the RMD amount by the deadline triggers an IRS excise tax on the participant.
- **[DATE-VERIFY]** — Required beginning age has been modified multiple times. Always verify the correct age for each participant's birth year before writing requirements.
- Never hardcode RMD ages, life expectancy factors, or penalty rates — these are IRS-published parameters that change.
- Roth balances of living participants are excluded from RMD calculations under SECURE 2.0 — this is a mandatory rule, not a plan design choice.
- **[RECOMMEND LEGAL/COMPLIANCE REVIEW]** — Beneficiary RMD rules are complex and have been subject to ongoing IRS regulatory interpretation. Flag all beneficiary RMD scenarios for legal review.

---

## Sources

- IRC Section 401(a)(9) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- IRS RMD Final Regulations (2024) | https://www.irs.gov | [DATE-VERIFY] | Retrieved 2026-03-06
- SECURE Act of 2019 (10-Year Rule) | https://www.congress.gov | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (RMD Age Increases, Roth Exemption, Penalty Reduction) | https://www.congress.gov | Retrieved 2026-03-06
- IRS Life Expectancy Tables (Publication 590-B) | https://www.irs.gov/publications/p590b | Retrieved 2026-03-06
