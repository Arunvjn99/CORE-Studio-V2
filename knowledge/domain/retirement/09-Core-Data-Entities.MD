# Skill: Core Data Entities
**Skill-ID:** 09-Core-Data-Entities
**World:** Retirement World v1.0
**Category:** Data & Entities
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the conceptual data entities of the CORE recordkeeping platform — what each entity represents, its key attributes, its relationships, and the system events that create, update, or close it. Every feature requirement must correctly identify which entities it touches.

---

## 1. Plan

**Represents:** The legal retirement plan entity as established by the plan document. The master record governing all rules and participants.

**Key attributes (conceptual):**
- Plan name, plan type (401(k), 403(b), 457(b), etc.)
- Plan year start/end dates
- Employer identification (EIN)
- Effective date and plan document version
- Safe harbor election status
- Auto-enrollment status and type (EACA, QACA, none)
- ERISA applicability flag
- Vesting schedule(s) by source
- Eligibility rules and entry date configuration
- Contribution formula parameters
- Investment menu reference
- TPA and advisor relationships
- QDIA designation

**Relationships:** Parent to all Participant Records, Contribution Records, and Transactions within the plan. References the Plan Design / Adoption Agreement for configuration parameters.

**System events:** Created at plan setup/onboarding; updated by plan amendments; closed at plan termination.

---

## 2. Plan Design / Adoption Agreement

**Represents:** The configuration layer between regulatory domain rules and the operational participant record. Captures the plan sponsor's elections for all plan-configurable parameters.

**Key attributes (conceptual):**
- Eligibility parameters (age, service, entry dates, exclusion classes)
- Contribution formulas (employer match formula, non-elective formula)
- Vesting schedule elections per source
- Distribution options (hardship, in-service, force-out thresholds)
- Loan policy (permitted, maximum, repayment period, interest rate basis)
- Auto-enrollment parameters (default rate, QDIA designation)
- Auto-escalation parameters (increment, frequency, cap)
- Safe harbor election type (Traditional or QACA)
- Compensation definition election (W-2, 415, includible)
- LTPT tracking requirements

**Relationships:** Directly referenced by all eligibility, contribution, vesting, and distribution processing logic. One Plan has one active Adoption Agreement at a time; prior versions retained for audit.

**System events:** Created at plan setup; updated by plan amendments (version-controlled); effective date tracking is critical for retroactive recalculation scenarios.

---

## 3. Employer / Plan Sponsor Record

**Represents:** The legal entity that sponsors the plan. In controlled group and MEP/PEP contexts, multiple employer entities may be associated with a single plan.

**Key attributes (conceptual):**
- Employer name and EIN
- Plan sponsor contact information
- Payroll provider relationship
- Controlled group membership flags
- Plan sponsor portal access configuration

**Relationships:** Associated with one or more Plans; parent to Participant Records by employment relationship.

**System events:** Created at plan setup; updated for mergers, acquisitions, controlled group changes; inactivated at plan termination.

---

## 4. Participant Record

**Represents:** An individual employee or former employee who is a participant or eligible to become a participant in the plan.

**Key attributes (conceptual):**
- Name; SSN (PII — restricted access, encrypted at rest and in transit, masked in display)
- Date of birth; date of hire; date of termination (if applicable)
- Employment status (active, terminated, deceased, disabled)
- Eligibility status and entry date
- Enrollment status (enrolled, not enrolled, auto-enrolled, opted out)
- Deferral rate and type (percentage of compensation or flat dollar)
- Investment elections (by source or unified election)
- Vesting percentage by source
- Beneficiary designations
- Contact information (address, email, phone)
- LTPT tracking flag and hours history
- HCE classification for current plan year

**Relationships:** Belongs to an Employer / Plan Sponsor; has one or more Account / Sub-accounts; has Contribution Records; may have Loan records; may have Distribution records; has Vesting Records.

**System events:** Created at hire or eligibility event; updated by payroll, enrollment, life events, termination, rehire; inactivated at full distribution or death with completed beneficiary distribution.

---

## 5. Beneficiary

**Represents:** The person(s) or entity designated to receive a participant's account balance upon death.

**Key attributes (conceptual):**
- Beneficiary name (and SSN/TIN if entity)
- Relationship to participant
- Designation type (primary vs. contingent)
- Percentage allocation
- Date of designation
- Spousal consent status (if applicable — required when non-spouse primary beneficiary designated for married participant)
- Trust or estate designation flag

**Relationships:** Associated with a Participant Record; triggers Death and Beneficiary Processing workflows upon participant death.

**System events:** Created or updated by participant election; may be updated by QDRO; triggered for distribution processing upon participant death notification.

---

## 6. Contribution Record

**Represents:** A single contribution transaction posting to a participant's account, attributed to a specific payroll cycle and contribution source.

**Key attributes (conceptual):**
- Participant reference; plan reference
- Payroll period (pay date and period)
- Contribution source (money type)
- Dollar amount
- Effective date; posting date
- Payroll file reference (traceability to source file)
- Status (pending, posted, corrected, rejected)

**Relationships:** Belongs to a Participant Record; classified by Source / Money Type; creates a Transaction record upon posting; aggregates to compliance testing data.

**System events:** Created upon receipt of payroll file; updated during validation; posted upon successful processing; corrected via corrective contribution records.

---

## 7. Source / Money Type

**Represents:** The classification of a contribution by its origin and regulatory treatment. Drives vesting, distribution eligibility, and tax withholding rules.

**Common sources:**
- Employee pre-tax (elective deferral) — always immediately vested; subject to annual deferral limit
- Designated Roth — after-tax employee contributions; always immediately vested; qualified distributions tax-free
- Employer match — subject to plan vesting schedule; subject to 415 limit
- Employer non-elective / profit sharing — subject to plan vesting schedule; subject to 415 limit
- Rollover (from prior plan or IRA) — immediately distributable; not subject to 415 annual additions limit
- After-tax (non-Roth) — employee after-tax; complex distribution ordering rules
- QNEC (Qualified Non-Elective Contribution) — corrective; immediately vested
- QMAC (Qualified Matching Contribution) — corrective; immediately vested
- PLESA contributions — after-tax; separate account; immediately distributable [DATE-VERIFY]
- Loan repayment — not a contribution; credits the loan sub-account

**Relationships:** Every Contribution Record, Account / Sub-account, and Transaction is tagged with a Source. Vesting Records reference source to determine applicable vesting schedule.

**System events:** Defined at plan setup; new sources may be added by plan amendment.

---

## 8. Investment Fund

**Represents:** An investment option available to participants on the plan's investment menu.

**Key attributes (conceptual):**
- Fund name; ticker symbol or CUSIP
- Fund type (mutual fund, collective investment trust (CIT), stable value, target-date fund (TDF) series)
- Expense ratio and revenue sharing rate
- Trading restrictions (blackout periods, redemption fees, excessive trading policies)
- QDIA eligibility flag
- Fund status (active, closed to new contributions, being mapped out)

**Relationships:** Referenced by participant investment elections; referenced by Account / Sub-account positions; referenced by trade instructions to Custodian/Trustee.

**System events:** Added/removed by plan sponsor or 3(38) investment manager; prices updated via daily NAV feed; blackout restrictions applied during fund mapping changes.

---

## 9. Account / Sub-account

**Represents:** The record of a participant's holdings in a specific investment fund within a specific contribution source.

**Key attributes (conceptual):**
- Participant reference; plan reference
- Source / money type
- Investment fund reference
- Unit balance; dollar value
- Vesting percentage (inherited from Vesting Record for employer sources)
- Last valued date

**Relationships:** Belongs to a Participant Record; tagged with a Source / Money Type; references an Investment Fund; aggregates to total participant account balance.

**System events:** Created upon first contribution posting; updated by contributions, distributions, investment trades, and daily valuation; closed at zero balance.

---

## 10. Transaction

**Represents:** Any financial event affecting a participant's account balance.

**Key attributes (conceptual):**
- Transaction type (contribution, distribution, loan origination, loan repayment, investment transfer, fee, correction, forfeiture)
- Transaction date and effective date
- Participant reference; source / money type; investment fund
- Dollar amount; unit quantity
- Status (pending, posted, failed, reversed)
- Reference to originating event (payroll file, distribution request, loan application)

**Relationships:** Links to Participant Record, Contribution Record (for contributions), Distribution record (for distributions), Loan record (for loans).

**System events:** Created by contribution posting, distribution processing, loan processing, investment rebalancing, fee processing, correction workflows.

---

## 11. Loan

**Represents:** A participant loan originated from the participant's vested account balance.

**Key attributes (conceptual):**
- Loan number; participant reference
- Origination date; loan amount
- Interest rate (plan-configurable per IRS reasonable rate standard — do not hardcode)
- Repayment schedule (amortization); maturity date
- Outstanding principal balance; repayment history
- Loan status (active, delinquent, defaulted, deemed distributed, offset, paid off)
- Loan purpose (general purpose vs. primary residence)

**Relationships:** Belongs to a Participant Record; reduces vested account balance at origination; repayments credited back to participant account by source.

**System events:** Created at loan origination; updated by repayment posting; status changed upon missed repayments; closed at payoff or deemed distribution.

---

## 12. Distribution

**Represents:** A payment from the plan to a participant, beneficiary, or alternate payee.

**Key attributes (conceptual):**
- Distribution type (hardship, RMD, termination, death, QDRO, in-service, force-out, rollover, emergency expense, domestic abuse)
- Participant or payee reference; distribution date
- Gross amount; federal tax withholding; state tax withholding; net amount
- Payee information (direct rollover institution details or participant payment details)
- Rollover election (direct vs. indirect)
- 1099-R data (distribution code, taxable amount)
- Status (requested, approved, processing, settled, 1099-R generated)

**Relationships:** Belongs to a Participant Record (or alternate payee); triggers tax withholding logic; generates 1099-R record; affects vesting finalization.

**System events:** Initiated by participant request, plan event (RMD trigger, force-out), or court order (QDRO); approved per plan and regulatory requirements; processed and settled; 1099-R generated at tax year end.

---

## 13. Vesting Record

**Represents:** The record of a participant's vested percentage in each employer contribution source.

**Key attributes (conceptual):**
- Participant reference; source / money type
- Vesting schedule type (immediate, cliff, graded) and version
- Years of vesting service (by computation method)
- Current vested percentage
- Vesting service history (year-by-year service record)

**Relationships:** Belongs to a Participant Record; references the vesting schedule in Plan Design; affects distributable balance calculations.

**System events:** Created upon first employer contribution; updated annually or upon triggering events (termination, rehire, amendment); finalized at termination of employment; 100% vested at plan termination.

---

## 14. Compliance Testing Data

**Represents:** Aggregated and participant-level data collected for annual compliance testing.

**Key attributes (conceptual):**
- Plan year; test type (ADP, ACP, 415, 416, 410(b), 401(a)(4))
- Participant compensation data by definition type (W-2, 415, includible)
- Contribution amounts by source
- HCE / NHCE classification
- Eligible employee list; excluded employee list
- Test result (pass/fail); corrective action taken

**Relationships:** Aggregates from Participant Records, Contribution Records, and Plan Design data.

**System events:** Data collected throughout plan year; formal test runs at year-end; corrections posted as Contribution Records or Distributions.

---

## 15. Notice / Document Record

**Represents:** A required notice or plan document generated and delivered to a participant, plan sponsor, or regulatory body.

**Key attributes (conceptual):**
- Notice type (SPD, SAR, safe harbor notice, QDIA notice, blackout notice, 402(f) Special Tax Notice, fee disclosure, etc.)
- Recipient; delivery method (electronic, paper)
- Delivery date; delivery confirmation status
- Document version; effective date

**Relationships:** Associated with a Participant Record (participant-level notices) or Plan (plan-level documents); tracked for ERISA disclosure compliance.

**System events:** Generated by triggering events (enrollment, plan year start, distribution request, blackout period); delivered via electronic or paper channel; delivery confirmation logged.

---

## 16. Forfeiture Account

**Represents:** The plan-level account holding unvested employer contributions forfeited by terminated participants.

**Key attributes (conceptual):**
- Plan reference; forfeiture balance
- Pending forfeitures (not yet processed)
- Plan year forfeitures by source
- Permitted uses per plan document
- Usage history (reduction of contributions, payment of expenses, funding of QNEC/QMAC)

**Relationships:** Associated with a Plan; sourced from terminated participant Vesting Records; affects employer contribution calculations and compliance testing.

**System events:** Credited upon termination and vesting finalization; debited when applied per plan document rules; timing governed by plan document and IRS guidance. [DATE-VERIFY — confirm forfeiture usage timing rules]

---

## Agent Rules

- Every feature requirement must identify which entities it creates, reads, updates, or closes.
- SSNs and other PII must always be referenced with access control, encryption, and masking requirements. **[COMPLIANCE-SENSITIVE]**
- Source / Money Type is foundational — every contribution and transaction must be correctly tagged to drive vesting, distribution, and tax logic.
- Adoption Agreement / Plan Design is the configuration source of truth — platform behavior must always trace to an adoption agreement provision.
- Audit trail is required for all entity state changes — timestamp, actor, and action.

---

## Sources

- IRS Retirement Plans — Plan Administration | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Plan Administration Resources | https://www.asppa.org | Retrieved 2026-03-06
