# Skill: Adjustment Processing
**Skill-ID:** 38-Adjustment-Processing
**World:** Retirement World v1.0
**Category:** Compliance Operations
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines adjustment processing — how the platform handles post-posting corrections, retroactive adjustments, late deposit corrections, corrective distributions, forfeiture adjustments, and EPCRS self-corrections. Adjustments are distinct from normal transaction processing: they correct prior events without erasing them. Audit integrity is paramount.

---

## 1. The Fundamental Rule of Adjustment Processing

**Original records are never overwritten or deleted.** Every adjustment is posted as a new corrective transaction that references the original transaction it is correcting.

This rule exists because:
- The original transaction represents what actually happened
- The adjustment represents the correction to the original
- Both must be visible in the audit trail to reconstruct the history of the participant's account
- Regulatory auditors (IRS and DOL) will look at the audit trail to understand what happened and what was done to fix it

**Platform requirement:** All adjustment transactions must:
- Have a transaction type that clearly identifies them as adjustments or corrections
- Reference the original transaction they are correcting (by transaction ID or reference number)
- Include the correction reason code
- Include the user who authorized the adjustment and the date

---

## 2. Types of Adjustments

| Adjustment Type | Trigger | Example |
|---|---|---|
| Contribution correction | Contribution was posted to wrong source, wrong amount, or wrong participant | Employee pre-tax incorrectly labeled as employer match |
| Excess contribution refund | Annual deferral limit (402(g)) or 415 limit exceeded | Participant over-contributed; excess returned with earnings |
| ADP/ACP corrective distribution | Test failed; HCE refund required | Excess aggregate contribution distributed to HCE |
| QNEC / QMAC corrective contribution | Test failed; employer corrective contribution | QNEC posted to correct ADP test failure |
| Late deposit lost earnings | Employer deposited contributions after the required deadline | Lost earnings calculated and posted as corrective contribution |
| Vesting correction | Participant was given incorrect vesting percentage | Unvested amount restored or additional amount forfeited |
| RMD correction | RMD was underdistributed | Additional distribution processed; excise tax may apply |
| Distribution correction | Distribution was processed incorrectly | Excess distribution corrected; under-distribution processed |
| Forfeiture adjustment | Forfeiture was applied incorrectly | Forfeiture reversed or re-applied |
| Retroactive plan amendment adjustment | Plan was amended retroactively; prior transactions need adjustment | Contribution formula changed retroactively; true-up calculated |
| Payroll data correction | Payroll file contained incorrect data that was already posted | Incorrect compensation data leads to match recalculation |

---

## 3. Contribution Correction Workflow

**Scenario:** A contribution was posted to the wrong source (e.g., employee pre-tax posted as employer match).

**Correction steps:**
1. Identify the erroneous contribution record
2. Create a reversal transaction (negative amount) referencing the original contribution — credits the incorrect source back to zero effect
3. Create a corrective contribution transaction (positive amount) to the correct source
4. Verify the net effect: participant's account balance is unchanged; only the source attribution changes
5. Log both transactions with the correction reason code and reference to the original
6. If the sources have different vesting schedules, recalculate vesting impact
7. If the year-to-date totals for limit monitoring were affected, recalculate limits

**Platform requirements:**
- Reversal transaction must be specifically typed as "Contribution Reversal — Correction"
- Corrective contribution must be specifically typed as "Corrective Contribution"
- Both must reference the original transaction ID
- Correction must be approved by an authorized user before posting (dual-approval workflow for corrections above a configurable dollar threshold)

---

## 4. Excess Contribution Refund (IRC 402(g) / 415 Corrections)

**Scenario:** A participant's year-to-date deferrals have exceeded the annual elective deferral limit (IRC 402(g)).

**Correction steps:**
1. Identify the excess amount: year-to-date deferrals minus the annual limit
2. Calculate earnings on the excess from the date of the excess contribution to the date of distribution
3. Distribute the excess plus earnings to the participant
4. Apply 10% early distribution penalty if the participant is under age 59½ (no exception for excess deferrals returned in the same plan year) — penalty waived if returned by April 15 of the following year [DATE-VERIFY]
5. Generate 1099-R for the corrective distribution with the correct distribution code
6. Update year-to-date totals

**For 415 violations:**
- Excess annual additions must be returned to the participant or allocated to a suspense account per EPCRS guidance
- [DATE-VERIFY — confirm current 415 correction methodology under EPCRS]

**Platform requirements:**
- Calculate excess amount per participant
- Calculate earnings on the excess using the IRS-specified methodology (IRS Notice or EPCRS guidance rate) [DATE-VERIFY]
- Generate corrective distribution transaction with correction type code
- Generate 1099-R with the correct distribution code for excess contributions

[COMPLIANCE-SENSITIVE]

---

## 5. ADP/ACP Corrective Distributions

**Scenario:** The ADP or ACP test failed; excess contributions must be distributed to HCEs.

**Correction steps:**
1. Receive corrective refund amounts per HCE from the compliance testing engine or TPA
2. Calculate earnings on the excess contributions from the end of the plan year to the date of distribution
3. Distribute the excess plus earnings to each affected HCE
4. Apply income tax withholding (subject to applicable rules — excess aggregate contributions are generally subject to 10% optional withholding; optional withholding rules differ from mandatory ERD withholding) [DATE-VERIFY]
5. Generate 1099-R for each HCE with the appropriate distribution code
6. Verify the plan passes the test after distributions are processed

**Correction deadline:** ADP/ACP corrective distributions must be made within:
- 2.5 months after the plan year end — corrective distribution is not subject to 10% excise tax on excess contributions
- 12 months after the plan year end — corrective distribution is subject to 10% excise tax
[DATE-VERIFY — confirm current ADP/ACP correction deadline and excise tax rules]

**Platform requirements:**
- Process corrective distributions from the participant's account in the correct source order
- Calculate earnings per IRS methodology
- Enforce the 2.5-month and 12-month deadline monitoring with alerts
- Generate 1099-Rs with correct distribution codes

[COMPLIANCE-SENSITIVE]

---

## 6. Late Deposit Lost Earnings (VFCP)

**Scenario:** Employer contributions were deposited to the trust after the required deadline.

**Correction steps:**
1. Calculate the deposit shortfall period: from the date contributions should have been deposited to the date they were actually deposited
2. Calculate lost earnings on the late amount using the greater of the IRS Applicable Federal Rate (AFR) or the plan's actual investment return during the period [DATE-VERIFY — confirm current VFCP calculation method]
3. Post the lost earnings as a corrective contribution to the forfeiture account or to participant accounts (per VFCP guidance)
4. File VFCP application with the DOL (or use the VFCP online calculator for qualifying transactions)
5. Retain VFCP documentation

**Platform requirements:**
- Calculate the late period and the lost earnings amount
- Post the corrective lost earnings contribution
- Generate VFCP documentation report (transaction timeline, amount, calculation methodology)

See also Skill 23 (Payroll Contribution Processing) and Skill 33 (Error Correction and EPCRS).

---

## 7. Retroactive Plan Amendment Adjustments

**Scenario:** A plan amendment has a retroactive effective date; prior transactions must be adjusted.

**Correction steps:**
1. Identify all transactions in the recordkeeping system with effective dates on or after the retroactive effective date
2. Determine the adjustment required for each affected transaction under the amended plan terms
3. Calculate the net adjustment per participant (may result in additional contributions, distributions, or vesting changes)
4. Post corrective transactions for each adjustment
5. Ensure all corrective transactions reference the plan amendment and the original transaction
6. If prior-year 1099-Rs are affected, determine whether corrected 1099-R forms are required

**Platform requirements:**
- Support batch identification of all affected transactions by date range and transaction type
- Calculate adjustments in bulk for large-scale retroactive corrections
- Post adjustments as new transactions (not overwrites)
- Generate adjustment summary report showing before/after impact per participant

[EDGE CASE — retroactive recalculation requires explicit acceptance criteria for scope, calculation methodology, and 1099-R implications]

---

## 8. Vesting Adjustment Processing

**Scenario:** A participant's vesting record was incorrect (wrong years of service, wrong schedule applied).

**Correction steps:**
1. Identify the correct vesting calculation
2. Calculate the difference: correct vested balance minus recorded vested balance
3. If vesting should be higher: restore the incorrectly forfeited amount from the forfeiture account (if available) or via employer contribution
4. If vesting was too high and unvested funds were incorrectly distributed: EPCRS correction required (potentially a make-whole contribution)
5. Update the vesting record with the correct calculation and log the correction

**Platform requirements:**
- Vesting adjustment workflow with approval gating
- Forfeiture account restoration logic (verify sufficient balance)
- Audit trail linking corrected vesting record to the original

---

## 9. Adjustment Authorization and Approval Controls

Not all adjustments should be self-service. Adjustment authorization levels:

| Adjustment Type | Minimum Approval Required |
|---|---|
| Contribution reversal and re-post (same amount, same participant) | Operations staff |
| Contribution amount correction (different amount) | Supervisor |
| EPCRS corrective contribution or distribution | TPA / Plan sponsor sign-off |
| Retroactive recalculation | Plan sponsor + TPA + legal/compliance review |
| Vesting correction | TPA or plan sponsor |
| QDRO-related adjustment | [RECOMMEND LEGAL/COMPLIANCE REVIEW] |

**Platform requirements:**
- Configurable approval workflow by adjustment type
- Dual-approval for adjustments above a configurable dollar threshold
- All adjustment approvals logged (who approved, when, what was approved)

---

## 10. Audit Trail for Adjustments

The audit trail for every adjustment must capture:
- Original transaction reference (transaction ID)
- Correction reason code (from a defined set)
- Corrective action type (reversal, refund, QNEC, VFCP, etc.)
- Dollar amount of the adjustment
- Effective date and posting date
- User who initiated the adjustment
- User(s) who approved the adjustment
- EPCRS program used (if applicable): SCP, VCP, or Audit CAP

---

## Agent Rules

- **Original records are NEVER overwritten or deleted.** Every adjustment is a new transaction. This is absolute.
- **[COMPLIANCE-SENSITIVE]** — Correction deadlines are regulatory and have consequences (excise taxes, ineligibility for SCP). [DATE-VERIFY all deadlines before finalizing correction timeline requirements]
- Adjustment processing workflows must include approval gating — at minimum, a second-level review before posting material corrections.
- 1099-R implications of prior-year corrections must be evaluated — corrective distributions in a subsequent year may require the original 1099-R to be corrected, which creates additional reporting obligations.
- **[EDGE CASE]** — Retroactive recalculations affecting a large number of participants must be planned as a batch operation with a reconciliation checkpoint before final posting.

---

## Sources

- IRS EPCRS Revenue Procedure | https://www.irs.gov/retirement-plans/correcting-plan-errors | Retrieved 2026-03-06
- DOL VFCP | https://www.dol.gov/agencies/ebsa/employers-and-advisers/correction-programs/vfcp | Retrieved 2026-03-06
- IRC Section 402(g) Excess Deferral Correction | IRS | https://www.irs.gov | Retrieved 2026-03-06
- SECURE 2.0 Act Section 305 (Expanded SCP) | https://www.congress.gov | Retrieved 2026-03-06
- ASPPA Error Correction Resources | https://www.asppa.org | Retrieved 2026-03-06
