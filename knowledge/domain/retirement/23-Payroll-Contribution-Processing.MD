# Skill: Payroll Contribution Processing
**Skill-ID:** 23-Payroll-Contribution-Processing
**World:** Retirement World v1.0
**Category:** Plan Administration Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the end-to-end payroll contribution processing workflow — from file/API receipt through validation, posting, funding, and reconciliation. It also covers deposit timeliness obligations, the VFCP late deposit correction program, and exception handling. This is the most frequent administrative operation in the platform and a primary source of compliance failures if poorly controlled.

---

## 1. Payroll File/API Receipt

Each payroll cycle, the payroll provider transmits contribution data to the platform.

**Delivery methods:**
- **File-based (SFTP):** Structured file (fixed-width, CSV/delimited, SPARK-format) delivered to a secure FTP location on the plan's payroll schedule
- **API-based:** Real-time or scheduled JSON payload per SPARK Institute API Integration Guidelines (June 2025)

**Platform requirements:**
- Monitor the SFTP location or API endpoint for incoming files/payloads
- Confirm receipt with a delivery acknowledgment
- Log the file/payload receipt timestamp, file name, and record count
- Detect and reject duplicate file submissions (duplicate detection by payroll period or file hash)

---

## 2. Format Validation

Before processing records, validate the file structure:
- File format matches the configured format for the plan
- Required header fields present and valid
- Record count matches the file trailer (if applicable)
- Field lengths and data types valid

**On format failure:** Reject the entire file; alert the plan sponsor or TPA; request resubmission.

---

## 3. Participant-Level Validation Rules

After format validation, each contribution record is validated against business rules:

| Validation Rule | Failure Action |
|---|---|
| Participant SSN/ID exists in the platform | Route record to exception queue: unmatched participant |
| Participant is eligible for the contribution source | Route to exception queue: ineligible source |
| Contribution source code is valid and mapped to a money type | Route to exception queue: invalid source code |
| Year-to-date deferral does not exceed annual deferral limit | Cap deferral at limit; alert; stop excess |
| Annual additions (415) limit not exceeded | Cap or reject; alert plan sponsor |
| Deferral rate is consistent with participant's elected rate (if applicable) | Flag for review (rate variance alert) |
| Contribution amount is positive and non-zero | Route to exception queue: invalid amount |
| Payroll period is current and expected | Flag unexpected periods for review |
| No duplicate contribution for same participant and period | Route to exception queue: duplicate detected |

---

## 4. Exception Queue Management

All failed validation records are routed to an exception queue. The exception queue must:
- Display the reason for each exception (specific rule violated)
- Allow the plan sponsor or TPA to review and resolve exceptions
- Support corrective actions: edit and resubmit, override with documentation, or exclude the record
- Track exception resolution (who resolved it, what action was taken, when)
- Generate a summary exception report per payroll cycle

**Platform requirements:**
- Exceptions must not block the posting of valid records — valid records from the same file proceed to posting while exceptions are held
- Exception resolution workflow must include audit trail

---

## 5. Contribution Allocation to Participant Accounts

After validation, contributions are allocated to participant accounts:
1. Tag each contribution with the correct money type (source)
2. Post the contribution to the participant's account for the correct source
3. Allocate the contribution across investment funds per the participant's current investment election (or QDIA if no election)
4. Update the participant's year-to-date contribution totals

**Platform requirements:**
- Post contributions in the correct source sub-accounts
- Apply investment allocation per the participant's effective election as of the processing date
- Update year-to-date totals for 402(g) and 415 monitoring
- Generate contribution transaction records with full audit trail

---

## 6. Employer Match Calculation

After employee contributions are posted, calculate the employer match:
1. Apply the plan's match formula to each participant's eligible employee deferrals
2. Verify the match does not cause a 415 limit violation for the participant
3. Post the calculated match to the employer match source
4. Allocate the employer match per the participant's investment election

**Per-payroll vs. annualized match:**
- Per-payroll: match calculated and posted each cycle
- Annualized with true-up: match calculated per cycle for timing, reconciled at year-end (see Skill 24)

---

## 7. Investment Allocation and Trade Aggregation

After all contributions are posted and allocated:
1. Aggregate net fund flows across all participant contributions (net buys per fund)
2. Combine with any other day's participant-directed transfers
3. Generate net trade instructions by fund
4. Submit trade instructions to the custodian/trustee for end-of-day NAV execution

---

## 8. Funding and Deposit Timeliness

**Employer's obligation:** Contribution assets must be deposited to the plan trust as soon as they can reasonably be segregated from the employer's general assets. DOL regulations establish timing safe harbors.

**DOL deposit timing rules:** [DATE-VERIFY — confirm current DOL deposit timing rules and safe harbor periods; specific timeframes are regulatory and change with rulemaking]

**Platform requirements:**
- Record the payroll date and the funding (wire/ACH) receipt date for each payroll cycle
- Calculate the elapsed time between payroll date and funding receipt
- Alert the plan sponsor if the elapsed time approaches or exceeds regulatory limits
- Flag potential late deposits for VFCP consideration

[COMPLIANCE-SENSITIVE]

---

## 9. Contribution Reconciliation

After contributions are posted and funding is received from the employer, reconcile:
- **Posted contribution amounts** (sum of all contributions posted in the recordkeeping system) vs.
- **Funding wire amount** (amount received in the trust) vs.
- **Payroll file total** (sum of all records in the payroll file)

**Reconciliation process:**
1. Sum posted contributions by payroll cycle in the recordkeeping system
2. Verify the funding wire amount matches the posted contribution total
3. Investigate any discrepancy before the next payroll cycle
4. Common causes: rounding at the record level, payroll adjustments processed after file submission, wire timing differences

**Platform requirements:**
- Generate a contribution reconciliation report per payroll cycle
- Flag unresolved discrepancies for escalation
- Require discrepancy resolution before accepting the next payroll cycle's contributions
- Maintain reconciliation records for audit trail

---

## 10. Late Deposit Correction — VFCP

If contributions are deposited to the trust after the required deadline, the plan may self-correct under the DOL's **Voluntary Fiduciary Correction Program (VFCP)**.

**VFCP correction requirements:**
1. Calculate the lost earnings on the late deposit (using the IRS Applicable Federal Rate or the plan's earnings rate, depending on which is higher — per current VFCP guidelines [DATE-VERIFY])
2. Deposit the lost earnings to the plan as additional contributions
3. Document the correction with the calculation methodology and amount
4. File for DOL no-action relief (VFC application) — or use the VFCP online calculator for qualifying transactions

**Platform requirements:**
- Identify late deposits based on payroll date vs. deposit date tracking
- Calculate lost earnings on late deposit amounts
- Post corrective lost earnings contributions
- Generate VFCP documentation (transaction summary, lost earnings calculation)
- Maintain documentation for DOL audit purposes

[COMPLIANCE-SENSITIVE]

---

## 11. Off-Cycle and Corrective Payrolls

Off-cycle payrolls (supplemental pay, retroactive pay adjustments, bonus runs) require special handling:
- Verify the payroll period is appropriate
- Apply the same validation rules as regular payroll cycles
- Flag for plan sponsor or TPA review before posting
- Retroactive pay may affect prior-period contribution amounts and limit calculations

**Platform requirements:**
- Support off-cycle payroll file processing
- Flag off-cycle files for human review before posting
- Handle retroactive pay adjustments through the correction workflow (see Skill 38)

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Deposit timeliness is a fiduciary obligation. Late deposits require VFCP correction. Late deposits that are not corrected are prohibited transactions.
- **[COMPLIANCE-SENSITIVE]** — Contribution limit monitoring must run at every payroll cycle, not just year-end.
- Exception queue management is not optional — every exception must be resolvable with full audit trail. An unresolved exception that is silently dropped is a participant harm risk.
- Contribution reconciliation must occur every payroll cycle. Carry-forward unreconciled amounts are a financial and audit risk.
- Never allow a payroll file format change to bypass validation rules — format changes require integration reconfiguration and re-testing.

---

## Sources

- DOL Regulation 29 CFR 2510.3-102 (Deposit Timing) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DOL VFCP | https://www.dol.gov/agencies/ebsa/employers-and-advisers/correction-programs/vfcp | Retrieved 2026-03-06
- IRC Sections 402(g), 415 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SPARK Institute API Integration Guidelines, June 2025 | https://www.sparkinstitute.org | Retrieved 2026-03-06
