# Skill: SECURE 2.0 Act — Platform-Relevant Provisions
**Skill-ID:** 07-SECURE-2-Point-0
**World:** Retirement World v1.0
**Category:** Regulatory & Compliance
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill catalogs all SECURE 2.0 Act of 2022 (P.L. 117-328) provisions that affect the CORE recordkeeping platform. Each provision includes what it changes, whether it is mandatory or optional, effective date status, and the platform impact. All effective dates are tagged [DATE-VERIFY] — confirm against authoritative sources before writing any requirement based on a SECURE 2.0 provision.

---

## Critical Agent Rules for SECURE 2.0

- **[DATE-VERIFY]** every effective date before writing a requirement based on a SECURE 2.0 provision.
- **Mandatory vs. Optional** must be verified and stated for every provision. This distinction determines whether the platform must enforce the rule or whether it is a configurable plan design option.
- Never write a definitive requirement on an assumed effective date. If uncertain, phrase as "effective-date-configurable."
- Extended amendment deadlines: SECURE 2.0 allowed plan sponsors to operationally implement provisions before formally amending their plan documents. Requirements must account for plans that have operationally adopted provisions without yet having amended their plan document.

---

## 1. Mandatory Auto-Enrollment

**What it changes:** New 401(k) and 403(b) plans established after the applicable SECURE 2.0 effective date must include automatic enrollment with a minimum default deferral rate and auto-escalation. [DATE-VERIFY — confirm plan establishment date threshold]

**Mandatory or Optional:** Mandatory for new plans established after the effective date. Existing plans are exempt (but may voluntarily adopt).

**Platform impact:**
- Auto-enrollment engine must be available as a required feature for new plans
- EACA or QACA structure required
- Default deferral rate must meet minimum requirements (plan-configurable per IRS guidance — do not hardcode)
- Auto-escalation must function per plan configuration

---

## 2. Super Catch-Up Contributions (Ages 60–63)

**What it changes:** Participants who have attained age 60, 61, 62, or 63 (but not yet age 64) are eligible for a higher catch-up contribution limit than the standard age-50+ catch-up. The Super Catch-Up limit is plan-configurable per current IRS rules. [DATE-VERIFY]

**Mandatory or Optional:** Plans may allow but are not required to permit catch-up contributions. If catch-up contributions are permitted, the Super Catch-Up limit must be made available for ages 60–63.

**Platform impact:**
- Age tracking — identify participants in the 60–63 age window each year
- Separate limit monitoring for Super Catch-Up vs. standard catch-up
- Super Catch-Up amounts must be treated as catch-up contributions for Roth routing purposes if the Roth catch-up mandate applies to the participant
- Do not hardcode the Super Catch-Up limit — reference as plan-configurable per IRS limit table

---

## 3. LTPT Employee Eligibility — 2-Year Rule

**What it changes:** Replaces the 3-year rule from the original SECURE Act for long-term part-time (LTPT) employees. Employees who complete the plan-configurable qualifying hours threshold for **two consecutive 12-month periods** must be permitted to make elective deferrals. [DATE-VERIFY]

**Mandatory or Optional:** Mandatory.

**Platform impact:**
- Track hours of service across consecutive measurement periods for employees otherwise excluded by a part-time hours exclusion
- Generate eligibility alerts when the 2-year LTPT threshold is met
- Manage entry date processing for LTPT-eligible employees
- Maintain LTPT tracking even for employees excluded by a part-time hours exclusion class
- Plans may continue to exclude LTPT employees from employer contributions

[COMPLIANCE-SENSITIVE]

---

## 4. Roth Account RMD Exemption

**What it changes:** Eliminates lifetime RMDs for designated Roth accounts (401(k), 403(b)) in employer plans, aligning treatment with Roth IRAs. Effective for taxable years beginning after 2023. [DATE-VERIFY]

**Mandatory or Optional:** Mandatory.

**Platform impact:**
- Suppress RMD calculation and automated distribution triggers for Roth source balances for living participants
- Roth balances must not be included in RMD calculation base
- Note: RMD rules for Roth balances still apply to beneficiaries after participant death

[COMPLIANCE-SENSITIVE]

---

## 5. Emergency Expense Distributions

**What it changes:** Plans may permit a distribution for personal or family emergency expenses up to a plan-configurable limit per IRS rules, without meeting traditional hardship criteria. Participants may repay the distribution within three years. One distribution permitted per year unless repaid. [DATE-VERIFY]

**Mandatory or Optional:** Optional for plans.

**Platform impact:**
- New distribution type: Emergency Expense
- Self-certification workflow with attestation requirement
- Repayment tracking (3-year window; repayment credited back to account)
- One-per-year limit enforcement (reset if prior distribution repaid)
- Early distribution penalty waived for qualifying distributions
- Do not hardcode the distribution limit — plan-configurable per IRS rules

[COMPLIANCE-SENSITIVE]

---

## 6. Domestic Abuse Distributions

**What it changes:** Plans may permit distributions to participants who self-certify as victims of domestic abuse, up to a plan-configurable limit per IRS rules. Early distribution penalty waived. Repayment option available within three years. [DATE-VERIFY]

**Mandatory or Optional:** Optional for plans.

**Platform impact:**
- New distribution type: Domestic Abuse
- Self-certification workflow (platform relies on participant attestation; no independent verification required)
- Repayment tracking (3-year window)
- Penalty waiver must be flagged in tax reporting (1099-R distribution code)
- Do not hardcode the distribution limit

[COMPLIANCE-SENSITIVE]

---

## 7. Student Loan Payment Matching (SLPM)

**What it changes:** Plans may permit employer matching contributions on qualified student loan payments (QSLPs) as if those payments were participant deferrals. Enables participants paying student loans to still receive employer match without contributing to the plan. [DATE-VERIFY — effective for plan years beginning after 2023]

**Mandatory or Optional:** Optional for plans.

**Platform impact:**
- Loan payment verification workflow (participant certifies QLSP amount; employer may optionally verify)
- Match calculation on QSLPs using the plan's matching formula
- New contribution source tracking: employer match on QLSP
- ADP/ACP testing implications: QSLPs and the match thereon must be properly classified for testing
- Annual limit monitoring: QLSP match counts toward the participant's annual additions limit

---

## 8. Roth Employer Contribution Option

**What it changes:** Plans may allow employer contributions (match, non-elective) to be designated by the participant as Roth (after-tax) contributions rather than pre-tax. [DATE-VERIFY — effective for plan years beginning after 2023]

**Mandatory or Optional:** Optional for plans.

**Platform impact:**
- New contribution source type: Employer Roth (after-tax employer contributions)
- Separate source tracking from pre-tax employer contributions
- Tax withholding at time of Roth employer contribution (employer Roth contributions are includible in participant income in the year made)
- Vesting schedule still applies to employer Roth contributions
- W-2 reporting implications

---

## 9. Roth Catch-Up Requirement for Higher Earners

**What it changes:** Catch-up contributions for participants whose prior-year compensation exceeds the IRS-defined threshold (plan-configurable per IRS rules) must be made as designated Roth contributions (after-tax) — pre-tax catch-up is not permitted for these participants. [DATE-VERIFY — confirm current effective date and compensation threshold]

**Mandatory or Optional:** Mandatory for applicable participants (those above the compensation threshold in plans that permit catch-up contributions).

**Platform impact:**
- Prior-year compensation monitoring to identify participants subject to mandatory Roth catch-up
- Automatic routing of catch-up contributions to Roth source for identified participants
- Pre-tax catch-up contributions must be rejected/rerouted for these participants
- Plan must have Roth feature in place for this requirement to be satisfied
- [COMPLIANCE-SENSITIVE] — If a plan does not have a Roth feature, it may need to be added or catch-up contributions blocked for affected participants

[COMPLIANCE-SENSITIVE]

---

## 10. RMD Age Increases

**What it changes:** SECURE 2.0 increased the required beginning age for RMDs in stages. The required beginning age is plan-configurable per current IRS rules. [DATE-VERIFY — confirm current RMD age for each cohort based on birth year]

**Mandatory or Optional:** Mandatory.

**Platform impact:**
- Required beginning date (RBD) calculation must use the correct age for each participant based on birth year and applicable law
- Participants who previously started RMDs under the old age may continue; those not yet at RMD age must use the updated age
- RMD calculation schedule updates for all affected participants
- Communication workflows for participants whose RMD start date has changed

---

## 11. DOL Lost and Found Database Reporting

**What it changes:** Plans must report terminated vested participants to the DOL's Retirement Savings Lost and Found database to help participants locate lost benefits. [DATE-VERIFY — confirm effective date per DOL rulemaking]

**Mandatory or Optional:** Mandatory when effective.

**Platform impact:**
- Reporting workflow to identify deferred vested participants meeting reporting criteria
- File generation and submission to DOL database
- Tracking of submitted records and status
- Integration with existing terminated participant/deferred vested tracking

---

## 12. PLESA (Pension-Linked Emergency Savings Accounts)

**What it changes:** Plans may establish PLESAs — short-term savings accounts linked to DC plans allowing non-HCE participants to save after-tax dollars for emergency use. PLESA balances may be withdrawn at any time without penalty. [DATE-VERIFY]

**Mandatory or Optional:** Optional for plans.

**Platform impact:**
- New account/source type: PLESA
- Contribution limit monitoring (plan-configurable per IRS rules — do not hardcode)
- Only non-HCE participants may contribute to PLESAs
- PLESA balances are in the participant's account; match interaction depends on plan design
- Withdrawal processing: at any time without penalty; subject to frequency limits (plan-configurable per IRS rules)
- Investment of PLESA balances: default investment rules apply; participant may have limited investment options

[COMPLIANCE-SENSITIVE]

---

## 13. Auto-Portability Services

**What it changes:** Facilitates automatic transfer of small balances from auto-rollover IRAs to a new employer's plan when a participant changes jobs. Authorized and encouraged by SECURE 2.0. [DATE-VERIFY]

**Mandatory or Optional:** Optional platform capability.

**Platform impact:**
- Auto-rollover IRA to new plan transfer capability
- ERISA safe harbor compliance for auto-portability transfers
- Data matching to identify eligible participants
- Integration with auto-portability network providers

---

## 14. Starter 401(k) Plans

**What it changes:** Creates a new simplified 401(k) plan type for employers that do not sponsor any other retirement plan. Mandatory auto-enrollment; no employer contribution requirement; reduced nondiscrimination testing burden. [DATE-VERIFY]

**Mandatory or Optional:** New optional plan type available to eligible employers.

**Platform impact:**
- Support for Starter 401(k) plan structure
- Auto-enrollment with simplified defaults
- Reduced compliance testing configuration
- Verify which specific compliance tests are waived or simplified

---

## 15. Expanded EPCRS Self-Correction (SCP)

**What it changes:** SECURE 2.0 significantly expanded eligibility for self-correction of plan errors under the IRS Self-Correction Program (SCP) without formal IRS submission. [DATE-VERIFY — confirm effective upon SECURE 2.0 enactment]

**Mandatory or Optional:** Available to all plans; not mandatory.

**Platform impact:**
- Self-correction workflows with error documentation
- Lost earnings calculation tools
- Complete audit trail for self-corrected errors
- Support for expanded SCP eligibility criteria

---

## Sources

- SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov/bill/117th-congress/house-bill/2954 | Retrieved 2026-03-06
- IRS Notice 2024-2 (SECURE 2.0 guidance) | https://www.irs.gov | Retrieved 2026-03-06
- DOL SECURE 2.0 Regulatory Actions | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA SECURE 2.0 Resources | https://www.asppa.org | Retrieved 2026-03-06
