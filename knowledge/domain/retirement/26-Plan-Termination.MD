# Skill: Plan Termination
**Skill-ID:** 26-Plan-Termination
**World:** Retirement World v1.0
**Category:** Plan Administration Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the plan termination workflow — required notices, vesting acceleration, final asset distribution, and the final Form 5500 filing. Plan termination is a rare but critical event that must be executed with precision to protect participant rights and satisfy regulatory obligations.

---

## 1. Decision to Terminate

A plan sponsor may terminate a plan at any time (subject to plan document terms and applicable law). Common reasons:
- Business closure, acquisition, or merger
- Transition to a new plan type
- Cost reduction
- Consolidation of multiple plans

Upon the decision to terminate, the plan sponsor must:
- Adopt a board resolution (for corporate plan sponsors) to terminate the plan
- Set the termination date
- Notify all affected parties (participants, TPA, recordkeeper, custodian)

---

## 2. Participant Notification

**Required notice content:**
- The plan is being terminated
- The termination date
- Participants' distribution options
- That all participants will become 100% vested
- Rollover rights and tax consequences
- Deadline for making distribution elections

**Timing:** Participants must be notified within a reasonable time before the termination and distribution process begins. [DATE-VERIFY — confirm current IRS/DOL required notification timing for plan terminations]

**Platform requirements:**
- Generate plan termination notice for all active and deferred vested participants
- Track notice delivery
- Log confirmation of receipt where available

---

## 3. Vesting Acceleration

Upon plan termination, **all participant accounts must become 100% vested** regardless of the participant's years of vesting service.

[COMPLIANCE-SENSITIVE]

**Platform requirements:**
- Update vesting percentage to 100% for all employer contribution sources for all participants
- Process this update on the plan termination date
- Log the vesting acceleration event for all affected participants
- Cancel any pending forfeitures (no new forfeitures should arise after termination is declared)

---

## 4. Cessation of Contributions

After the termination date:
- No new employee deferrals should be deducted from payroll
- No new employer contributions should be made (except for contributions already earned or accrued before termination)
- Final payroll contributions must be processed and posted

**Platform requirements:**
- Flag the plan as "Terminating" to prevent new contribution submissions
- Process any final payroll contributions that were in-flight at termination
- Disable future contribution processing after final cycle

---

## 5. Final Asset Reconciliation

Before distributions can be made, the plan's assets must be fully reconciled:
- Final contribution amounts posted and reconciled to trust
- All pending investment transactions settled
- All outstanding loans addressed (participants must repay or the loan becomes an offset distribution)
- Forfeiture account applied (no remaining forfeitures after termination — all must be allocated or used before final distribution)
- Final plan asset value confirmed with custodian

**Platform requirements:**
- Generate a final asset reconciliation report
- Confirm that the recordkeeping system's participant account totals equal the trust's total asset value
- Resolve any discrepancies before beginning final distributions

---

## 6. Loan Handling at Plan Termination

Outstanding loan balances at plan termination must be addressed:
- Participants may repay outstanding loans before the plan terminates
- Unpaid loan balances at termination become plan loan offset distributions (taxable)
- Generate 1099-R for loan offset distributions
- Apply mandatory 20% withholding (if applicable)

**Platform requirements:**
- Identify all outstanding loan balances
- Notify participants of outstanding loans and options (repay or accept loan offset)
- Process loan offsets as distributions for participants who do not repay

---

## 7. Final Asset Distribution

All plan assets must be distributed (or rolled over) upon termination. The plan may not retain assets after completing the distribution process.

**Distribution process for each participant:**
1. Present distribution options: lump sum (with rollover option), direct rollover, installments (if applicable)
2. Generate 402(f) Special Tax Notice
3. Collect distribution elections
4. Apply mandatory 20% federal withholding (for non-direct rollover ERDs)
5. Process distributions to participants, beneficiaries, and rollover institutions
6. Generate 1099-Rs for all distributions

**Force-out of unresponsive participants:**
- Participants who do not respond to distribution notices must have their balances distributed
- For balances below the mandatory rollover threshold: distributed to an IRA (auto-rollover) or escheated if IRA cannot be established
- For balances above the mandatory rollover threshold: distributed to an auto-rollover IRA
- [DATE-VERIFY — confirm current force-out rules and thresholds for plan termination scenarios]

**Platform requirements:**
- Process all distribution elections
- Generate all required notices
- Confirm all distributions settled and balances reduced to zero
- Close participant accounts after final distribution

---

## 8. Escheatment of Unclaimed Balances

If a participant cannot be located and an auto-rollover IRA cannot be established, the balance may need to be escheated to the state under applicable unclaimed property laws. Escheatment rules vary by state. [DATE-VERIFY — confirm applicable state law requirements]

**Platform requirements:**
- Identify unlocatable participants after reasonable search efforts
- Process escheatment distributions to the appropriate state
- Generate required documentation for state escheatment filings

---

## 9. Final Form 5500 Filing

A final Form 5500 marked as a final filing must be submitted for the plan's last plan year.

**Final 5500 requirements:**
- Mark the filing as final
- Report the plan's total distributions for the final plan year
- Report the closing participant count (should be zero after all distributions are processed)
- Include all required schedules

**Filing deadline:** [DATE-VERIFY — confirm current final 5500 deadline; same filing deadline as regular 5500 applies]

**Platform requirements:**
- Generate final 5500 data package after all distributions are complete
- Verify participant counts are zero (or flag any remaining balances)
- Deliver data to TPA for final 5500 filing

---

## 10. Plan Record Retention After Termination

ERISA requires plan records to be retained for at least 6 years after the filing date. [DATE-VERIFY — confirm current retention standards] Even after the plan terminates, the recordkeeper and plan sponsor must maintain records sufficient to determine participant rights.

**Platform requirements:**
- Archive all plan records (participant accounts, transactions, compliance testing, notices, documents) in long-term storage
- Maintain retrieval capability for the required retention period
- Ensure records are accessible for DOL audit or participant inquiry

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — 100% vesting acceleration upon plan termination is mandatory and immediate. This cannot be phased or deferred.
- **[COMPLIANCE-SENSITIVE]** — No plan assets may be retained by the employer after the plan terminates (exclusive benefit rule). All assets must be distributed to participants or rolled over.
- Plan termination involves multiple simultaneous workflows — coordination between the plan sponsor, TPA, recordkeeper, and custodian is critical. Sequence dependencies must be respected.
- Unlocatable participants at termination require documented search efforts before escheatment.
- Final 5500 filing must reflect zero remaining participant balances after distributions are complete.

---

## Sources

- IRC Section 411(d)(3) (Vesting at Plan Termination) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- ERISA Sections 4041, 4044 (Plan Termination) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRS Publication 4461 (Plan Termination) | https://www.irs.gov | Retrieved 2026-03-06
- DOL Form 5500 Final Filing Instructions | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
