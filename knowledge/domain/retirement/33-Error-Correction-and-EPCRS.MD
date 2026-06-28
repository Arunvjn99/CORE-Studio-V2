# Skill: Error Correction and EPCRS
**Skill-ID:** 33-Error-Correction-and-EPCRS
**World:** Retirement World v1.0
**Category:** Implementation & Data Integration
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines how plan operational errors are identified, corrected, and documented under the IRS Employee Plans Compliance Resolution System (EPCRS). It also covers the DOL Voluntary Fiduciary Correction Program (VFCP) for deposit timing failures. Errors that are not corrected can result in plan disqualification; errors that are corrected improperly create additional compliance exposure.

---

## 1. Why Correction Is Mission-Critical

Plan operational errors — failure to enroll an eligible employee, excess contributions, incorrect vesting, missed distributions — are qualification failures. If not corrected, they can result in:
- Plan disqualification (loss of tax-advantaged status for all participants)
- Taxation of participant account balances
- IRS penalties and assessments
- DOL civil enforcement actions

The IRS EPCRS system provides structured pathways for plans to correct errors and preserve qualified status. The platform must support these correction workflows.

---

## 2. Types of Plan Operational Errors

**Common errors requiring correction:**

| Error Type | Description |
|---|---|
| Excess contributions / deferrals | Participant contributed more than the annual limit (IRC 402(g) or 415) |
| Failed ADP/ACP test | Nondiscrimination test failed; corrective refunds or QNEC/QMAC required |
| Missed RMD | Participant did not receive the required minimum distribution |
| Incorrect vesting | Participant was given more or less vesting credit than they were entitled to |
| Failure to enroll eligible employee | Eligible employee was excluded from the plan |
| Late deposit | Employer contributions not deposited to the trust within the required timeframe |
| Loan violation | Loan exceeded IRC 72(p) limits or was not repaid on the required schedule |
| Incorrect distribution amount | Participant received more or less than they were entitled to |
| Failure to obtain QDRO procedures | Plan did not establish written QDRO procedures as required |
| Operational error vs. plan terms | Plan operated in a manner inconsistent with the plan document |

---

## 3. EPCRS — The IRS Correction Framework

The IRS Employee Plans Compliance Resolution System (EPCRS) provides three correction programs:

### SCP — Self-Correction Program

Plans may self-correct certain operational failures **without IRS submission** and without paying a user fee.

**SECURE 2.0 expanded SCP eligibility:** SECURE 2.0 significantly broadened the scope of errors that may be self-corrected, including permitting self-correction of certain plan document failures and extending the self-correction period. [DATE-VERIFY — confirm current SCP eligibility scope under SECURE 2.0]

**SCP requirements:**
- The plan must have a practice of compliance (significant failures generally cannot be self-corrected under SCP)
- Correction must be completed within the applicable correction period (significant failures: generally within 3 years; non-significant: by the end of the following plan year) [DATE-VERIFY]
- Correction must be reasonable and appropriate
- Documentation of the error and correction must be maintained

### VCP — Voluntary Correction Program

Plans submit a description of the failure and proposed correction to the IRS for review and approval. The IRS issues a compliance statement if the correction is approved.

**When VCP is appropriate:**
- The failure is significant and SCP is not available (or the plan sponsor prefers IRS approval for certainty)
- The error involves a plan document failure requiring IRS approval
- The plan sponsor wants a no-action letter for significant issues

**VCP process:**
1. Prepare a VCP submission documenting the failure, its scope, and the proposed correction
2. Submit to the IRS with the applicable user fee
3. IRS reviews and issues a compliance statement (or requests additional information)
4. Implement the approved correction

### Audit CAP — Audit Closing Agreement Program

Correction negotiated with the IRS when the failure is discovered during an IRS audit. Audit CAP involves a sanction (financial penalty). The platform's role is primarily documentation support — providing the audit trail that demonstrates the scope of the error and the correction taken.

---

## 4. Correction Methodologies

**Corrective contributions (QNEC/QMAC):**
- Used to correct ADP/ACP failures by increasing NHCE contribution percentages
- Must be 100% immediately vested
- Must be posted to the correct source (QNEC or QMAC)
- May also be used to correct failures to enroll eligible employees (make whole the excluded employee with a corrective contribution)

**Corrective distributions (excess refunds):**
- Used to correct excess deferrals (IRC 402(g) failures) by distributing the excess to the participant
- Must be completed within the required correction deadline with earnings
- 1099-R generated for the excess refund with the appropriate distribution code

**Lost earnings calculation:**
- Many corrections require payment of lost earnings on the corrective amount
- Lost earnings = the earnings the participant would have received had the error not occurred
- Calculated using the IRS EPCRS correction interest rate (or the plan's actual return, if higher) — plan-configurable per current EPCRS guidance [DATE-VERIFY]

**Make-whole contributions:**
- For eligible employees who were improperly excluded from participating, the employer makes a corrective contribution to make the employee whole for the missed deferrals and matching contributions
- Calculation: the excluded employee's missed deferral opportunity (based on their compensation and the plan's average deferral rate or a specified percentage per EPCRS) plus the employer match the employee would have received

---

## 5. VFCP — Voluntary Fiduciary Correction Program (DOL)

The VFCP is a separate DOL program for correcting certain ERISA prohibited transactions, most commonly **late deposit of participant contributions**.

**VFCP correction for late deposits:**
1. Calculate the lost earnings on the late deposit from the date the amount could reasonably have been segregated from employer assets to the date it was actually deposited
2. Calculate using the IRS Applicable Federal Rate (AFR) or the plan's actual return, whichever is higher [DATE-VERIFY — confirm current VFCP lost earnings calculation method]
3. Deposit the lost earnings to the plan
4. File a VFC Program application with the DOL for a no-action letter (or use the VFCP online calculator for qualifying transactions, which provides automatic no-action relief)

**Platform requirements:**
- Calculate late deposit lost earnings per the VFCP methodology
- Post corrective contributions (lost earnings) to the plan
- Generate VFCP documentation package (transaction timeline, lost earnings calculation, correction evidence)
- Maintain VFCP documentation for DOL audit purposes

[COMPLIANCE-SENSITIVE]

---

## 6. Platform Correction Workflow

**Correction workflow steps:**
1. **Error identification:** The error is identified through self-audit, participant inquiry, TPA review, or compliance testing
2. **Error scoping:** Determine which participants are affected, which periods are affected, and the dollar impact
3. **Correction calculation:** Calculate the corrective amount per participant (contribution, refund, or lost earnings as applicable)
4. **Review and approval:** Plan sponsor or TPA reviews and approves the correction
5. **Posting of corrective transactions:** Post the correction as new transactions in the recordkeeping system — never overwrite originals
6. **Audit trail documentation:** All correction transactions must reference the original erroneous transaction and the correction methodology
7. **1099-R generation:** If a corrective distribution is made, generate the 1099-R with the correct distribution code
8. **EPCRS documentation:** Prepare and retain documentation of the error, correction, and any IRS/DOL filings

**Platform requirements:**
- Correction workflow that supports identification, calculation, approval, and posting
- Correction transactions are clearly labeled as "corrective" in the transaction type
- Audit trail links corrective transactions to the original erroneous transactions
- Lost earnings calculation tools (IRS AFR method or plan earnings method)
- Document generation for EPCRS and VFCP submissions

---

## 7. Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Correction deadlines under EPCRS and VFCP are regulatory — missing a correction deadline elevates the correction program required (SCP → VCP → Audit CAP) and increases penalties.
- Never overwrite original transaction records in the course of a correction — corrections are new transactions linked to the originals.
- Lost earnings calculation methodologies differ between EPCRS, VFCP, and ADP/ACP correction — verify the correct methodology for each error type. [DATE-VERIFY]
- **[EDGE CASE]** — Corrections that affect prior-year 1099-R reporting require corrected 1099-R forms. Flag for explicit acceptance criteria.
- SECURE 2.0 expanded SCP eligibility significantly — [DATE-VERIFY] current SCP scope before recommending VCP for any error.

---

## Sources

- IRS Revenue Procedure — EPCRS | https://www.irs.gov/retirement-plans/correcting-plan-errors | Retrieved 2026-03-06
- SECURE 2.0 Act Section 305 (Expanded SCP) | https://www.congress.gov | Retrieved 2026-03-06
- DOL VFCP | https://www.dol.gov/agencies/ebsa/employers-and-advisers/correction-programs/vfcp | Retrieved 2026-03-06
- ASPPA EPCRS Resources | https://www.asppa.org | Retrieved 2026-03-06
