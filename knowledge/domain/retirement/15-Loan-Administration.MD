# Skill: Loan Administration
**Skill-ID:** 15-Loan-Administration
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the full participant loan lifecycle — origination, repayment, default handling, deemed distribution triggers, and loan offsets at termination. Loan administration is compliance-sensitive; errors in limit calculation, repayment tracking, or deemed distribution timing create taxable events and potential penalties for participants.

---

## 1. Loan Eligibility and Plan Policy

Loans are permitted only if the plan document allows them. Loan availability is plan-configurable:
- Maximum number of outstanding loans per participant (plan-configurable; may be 1, 2, or more)
- Loan purposes permitted (general purpose, primary residence, or both)
- Primary residence loans may have longer repayment periods than general purpose loans

**Platform requirements:**
- Verify the plan document permits loans before processing any loan request
- Enforce the maximum number of outstanding loans per participant
- Distinguish loan purpose (general vs. primary residence) and apply correct repayment period

---

## 2. Maximum Loan Amount (IRC Section 72(p))

The maximum loan amount is governed by IRC Section 72(p). The limit is the lesser of:
- **(a)** A percentage of the participant's vested account balance, subject to a dollar cap — **both the percentage and the cap are plan-configurable per IRS rules**
- **(b)** The vested account balance reduced by the participant's highest outstanding loan balance in the preceding 12 months

**Do not hardcode** the maximum loan percentage or the dollar cap. Reference as plan-configurable parameters per current IRS 72(p) limits.

**Platform requirements:**
- Calculate the vested account balance dynamically at the time of loan origination
- Calculate the 12-month highest outstanding loan balance
- Apply both prongs of the 72(p) test and take the lesser
- Present the maximum available loan amount to the participant
- Reduce the maximum by any existing outstanding loan balances (if multiple loans are permitted)
- Account for multiple outstanding loans in the maximum calculation

[COMPLIANCE-SENSITIVE]

---

## 3. Loan Origination Workflow

1. Participant submits loan request (amount, purpose, proposed repayment period)
2. Platform validates eligibility (plan permits loans, participant is eligible, no outstanding loans exceed the permitted maximum)
3. Platform calculates the maximum available loan amount
4. Platform calculates the amortization schedule (level installments at least quarterly; term per plan policy and IRC limits)
5. Plan sponsor or 3(16) administrator approves (if required by plan policy)
6. Loan proceeds are funded from participant's vested account by source (source liquidation follows plan's loan collateral rules — typically pro-rata across sources)
7. Loan sub-account created; outstanding principal balance recorded
8. Promissory note and repayment schedule generated and provided to participant
9. Payroll integration activated for automatic repayment deductions starting the next payroll cycle

**Interest rate:** Must be a reasonable rate comparable to what a commercial lender would charge for a similar loan (plan-configurable basis; Prime Rate + a spread is common — do not hardcode the spread).

---

## 4. Repayment Schedule and Tracking

**Repayment requirements (IRC 72(p)):**
- Repayments must be made in **substantially level installments** at least quarterly
- General purpose loans: maximum repayment period is 5 years (60 months) — plan-configurable per IRC limit
- Primary residence loans: maximum repayment period may exceed 5 years (plan-configurable per IRC guidance) [DATE-VERIFY — confirm current primary residence loan term rules]

**Platform requirements:**
- Generate and store the amortization schedule at origination
- Track each repayment received against the scheduled payment
- Credit repayments to the participant's account by source (reversing the liquidation order at origination)
- Calculate outstanding principal and accrued interest at any point in time
- Monitor for missed payments against the scheduled repayment dates
- If the participant changes payroll provider or takes a leave of absence, track repayment status and apply cure period logic

---

## 5. Loan Delinquency and the Cure Period

If a participant misses a scheduled repayment, the loan becomes delinquent. The IRS provides a **cure period** during which the participant may make up the missed payment without triggering a deemed distribution.

**Cure period:** The cure period extends through the end of the calendar quarter following the quarter in which the first missed payment occurred. [DATE-VERIFY — confirm current IRS cure period rules]

**Example concept:** If a payment is missed in February (Q1), the cure period extends through June 30 (end of Q2). If the participant does not cure the delinquency by June 30, the deemed distribution is triggered.

**Platform requirements:**
- Monitor repayment schedules daily for missed payments
- Flag delinquent loans and calculate the cure period end date
- Alert the participant and plan sponsor of delinquency and the cure deadline
- Track cure period status per loan
- Process catch-up payments within the cure period and update loan status to current

---

## 6. Deemed Distribution

If the cure period expires without the participant making up the missed payment(s), the outstanding loan balance is treated as a **deemed distribution** — a taxable event for the participant.

**Key characteristics of deemed distribution:**
- The participant receives no cash — the deemed distribution is a paper taxable event
- The outstanding loan balance remains on the books; loan repayments that subsequently occur are treated as after-tax contributions (basis in the account) [COMPLIANCE-SENSITIVE]
- The participant receives a Form 1099-R for the deemed distribution with the appropriate distribution code
- The 10% early distribution penalty applies unless an exception applies (e.g., age 59½, disability)
- The deemed distribution amount is not eligible for rollover

**Platform requirements:**
- Trigger deemed distribution processing when the cure period expires without cure
- Calculate the deemed distribution amount (outstanding principal at time of default)
- Generate 1099-R with correct distribution code
- Update loan status to "Deemed Distributed"
- Maintain the loan balance on the books (the loan is not eliminated — repayments continue as after-tax)
- Track post-deemed-distribution repayments as after-tax contributions for basis tracking purposes

[COMPLIANCE-SENSITIVE]

---

## 7. Loan Offset on Termination of Employment

When a participant terminates employment with an outstanding loan balance, the plan may require repayment or declare a loan offset.

**Loan offset:** The outstanding loan balance is treated as a **plan loan offset distribution** — a taxable distribution to the participant.

**SECURE 2.0 — Extended Rollover Deadline for Loan Offsets:** SECURE 2.0 extended the deadline for participants to roll over a qualified plan loan offset (QPLO) amount to another eligible retirement plan or IRA. The participant has until their tax return due date (including extensions) for the year of the offset. [DATE-VERIFY — confirm current SECURE 2.0 loan offset rollover deadline]

**Platform requirements:**
- Upon termination of employment, identify any outstanding loan balances
- Notify the participant of outstanding loan balance and repayment options
- If loan is not repaid within the plan's grace period after termination, process the loan offset as a distribution
- Calculate the loan offset amount (outstanding principal)
- Generate 1099-R for the loan offset distribution with the appropriate distribution code
- Include information about the SECURE 2.0 extended rollover deadline in the participant notice
- Update loan status to "Offset"

---

## 8. Loans During Leave of Absence

If a participant takes a leave of absence, different rules may apply to loan repayments:
- DOL provides a suspension of loan repayments during a qualified leave of absence (e.g., FMLA, military leave) — loan term may be extended to account for the suspension period [DATE-VERIFY]
- Military leave: special rules under USERRA may apply to loan repayments during military service [DATE-VERIFY]

**Platform requirements:**
- Support leave of absence status on the participant record
- Suspend loan repayment deductions during qualified leaves
- Extend the loan maturity date to account for the suspension period
- Resume repayments upon return from leave

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Maximum loan amount calculation must apply both prongs of the IRC 72(p) test. An oversized loan is a prohibited transaction.
- **[COMPLIANCE-SENSITIVE]** — Deemed distribution trigger logic must be precise. Early triggering or late triggering both create compliance exposure.
- Never hardcode the loan maximum percentage, dollar cap, or repayment period — all are plan-configurable per IRS rules.
- Loan origination from the participant's account reduces the invested balance — the platform must liquidate from the correct sources and update balances in real time.
- Post-deemed-distribution repayments must be tracked as after-tax basis — failure to track this creates incorrect 1099-R reporting at future distributions.

---

## Sources

- IRC Section 72(p) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL Regulation 29 CFR 2550.408b-1 (Participant Loans) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 — Qualified Plan Loan Offset | https://www.congress.gov | Retrieved 2026-03-06
- IRS Publication 560 | https://www.irs.gov/publications/p560 | Retrieved 2026-03-06
