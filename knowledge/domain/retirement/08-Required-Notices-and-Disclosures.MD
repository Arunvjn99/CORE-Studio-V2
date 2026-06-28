# Skill: Required Notices and Disclosures
**Skill-ID:** 08-Required-Notices-and-Disclosures
**World:** Retirement World v1.0
**Category:** Regulatory & Compliance
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines every required notice and disclosure obligation applicable to qualified DC plans, who must deliver it, when it is required, and what the platform must do to generate, deliver, and track it. Failure to deliver required notices is itself an ERISA violation. [COMPLIANCE-SENSITIVE for all notices]

---

## 1. Notice Delivery — General Rules

### Electronic Delivery (DOL Final Rule 2020)

The DOL's electronic disclosure safe harbor allows electronic delivery of required disclosures provided:
- Participants are notified of the availability of documents in electronic form and their right to request paper copies
- Documents are made accessible on a website or delivered via email
- Participants have the ability to opt for paper delivery at no charge
- Certain participants (e.g., non-email employees) may require default paper delivery

[DATE-VERIFY — confirm current DOL e-delivery rule requirements in effect]

The platform must support **both** electronic and paper delivery workflows for all required notices.

### Audit Trail Requirements

For every notice:
- Log generation timestamp
- Log delivery method, delivery timestamp, and recipient
- Track delivery confirmation (email open, return receipt, positive confirmation)
- Log failed delivery attempts and generate alerts for follow-up
- Retain delivery logs per ERISA Section 107 (minimum 6 years)

---

## 2. Required Notice Reference Table

| Notice | What It Is | When Required | Who Delivers | Timing | Platform Role |
|---|---|---|---|---|---|
| **404(a)(5) Participant Fee Disclosure** | Discloses plan fees and investment-related information to participants | Annually and upon enrollment; updated when material changes occur | Plan Administrator (via Recordkeeper) | Annually; within 30 days of material change [DATE-VERIFY] | Generate, deliver, and log delivery; support e-delivery |
| **408(b)(2) Service Provider Fee Disclosure** | Discloses fees and services of covered service providers to the plan fiduciary | Before entering or renewing a service contract; when changes occur | Covered service provider | Before service contract start or renewal | Recordkeeper provides to plan sponsor; platform tracks receipt |
| **Safe Harbor Notice** | Notifies participants of employer safe harbor contribution obligation and their rights | Annually, before plan year start | Plan Administrator | At least 30 days before plan year start [DATE-VERIFY] | Generate and track delivery annually |
| **QDIA Notice** | Notifies participants of the plan's default investment and their right to change | Annually and before first automatic contribution | Plan Administrator | At least 30 days before first automatic investment in QDIA; annually thereafter [DATE-VERIFY] | Generate and track delivery; link to QDIA fund information |
| **Blackout Notice (ERISA 101(i))** | Notifies participants of upcoming period when investment direction is suspended | Before any blackout period | Plan Administrator | At least 30 days before blackout period begins [DATE-VERIFY] | Generate at blackout setup; track delivery and blackout dates |
| **Summary Plan Description (SPD)** | Plain-language description of plan terms and participant rights | New participants; new plans; plan updates | Plan Administrator | Within 90 days of plan eligibility; within 120 days of new plan; every 5 years if amended, 10 years if not [DATE-VERIFY] | Store and version-control; deliver upon eligibility; track delivery |
| **Summary of Material Modifications (SMM)** | Describes material changes to the plan | After material plan amendments | Plan Administrator | Within 210 days after end of plan year in which change was adopted [DATE-VERIFY] | Generate when plan amendments are processed |
| **Summary Annual Report (SAR)** | Summary of Form 5500 financial information | Annually after Form 5500 filing | Plan Administrator | Within 9 months after plan year end (or 2 months after 5500 due date if extended) [DATE-VERIFY] | Generate from year-end financial data; distribute to participants |
| **402(f) Special Tax Notice** | Explains rollover options, withholding, and tax consequences of eligible rollover distributions | Before any eligible rollover distribution | Plan Administrator | At least 30 days before distribution; participant may waive the waiting period [DATE-VERIFY] | Generate and deliver before distribution processing; track confirmation |
| **Annual Lifetime Income Statement (SECURE 2.0)** | Periodic statement showing projected lifetime income from account balance | At least annually [DATE-VERIFY] | Plan Administrator / Recordkeeper | With annual participant statement | Generate using IRS-prescribed assumptions; deliver with statement |
| **EACA 90-Day Withdrawal Notice** | Informs automatically enrolled participants of their right to withdraw contributions within 90 days | At auto-enrollment | Plan Administrator | Before or concurrent with first automatic deferral | Generate at auto-enrollment; track delivery and 90-day window |
| **QACA Notice** | Notifies participants of QACA structure including default deferral, auto-escalation, and employer contributions | Annually and before plan year start | Plan Administrator | Same timing as safe harbor notice [DATE-VERIFY] | Generate and deliver; combined with safe harbor notice if applicable |
| **Automatic Enrollment Notice** | Notifies participants of automatic enrollment and their right to change or opt out | Before automatic enrollment takes effect | Plan Administrator | Sufficiently in advance to allow opt-out before first deferral [DATE-VERIFY] | Generate at eligibility; track opt-out deadline |

---

## 3. Notice Detail — Critical Notices

### 402(f) Special Tax Notice

The 402(f) Special Tax Notice is one of the most important participant-facing notices. It must be provided before any eligible rollover distribution (ERD) and must explain:
- The participant's right to a direct rollover to an eligible retirement plan or IRA
- The mandatory 20% federal income tax withholding on ERDs not directly rolled over
- The 10% early distribution penalty (and exceptions)
- State withholding rules
- RMD amounts not eligible for rollover

**Platform requirements:**
- Generate the 402(f) notice before initiating any distribution processing that may be an ERD
- Track the date the notice was provided
- Enforce the minimum waiting period (at least 30 days) unless the participant affirmatively waives it [DATE-VERIFY]
- Participant waiver of the waiting period must be captured and logged

[COMPLIANCE-SENSITIVE]

### Blackout Notice (ERISA Section 101(i))

Required whenever participant rights to direct investments, take loans, or obtain distributions are temporarily suspended for more than three consecutive business days during a blackout period.

**Platform requirements:**
- Identify and initiate blackout notice generation when a blackout period is set up
- Enforce the minimum 30-day advance notice requirement [DATE-VERIFY]
- Restrict participant investment transactions during the blackout period
- Log blackout start and end dates
- Exception: blackout notice not required if the blackout is caused by extraordinary circumstances outside the plan's control [DATE-VERIFY]

**Insider trading implication:** ERISA 101(i) also prohibits plan insiders (directors, officers, and 10% shareholders) from trading in company stock during a blackout period. This is a separate obligation but requires blackout period dates to be accurately maintained.

[COMPLIANCE-SENSITIVE]

### 404(a)(5) Fee Disclosure

Annual fee disclosure to participants covering:
- Plan-level administrative fees and how they are charged
- Individual-level fees and when they are triggered (e.g., loan origination, QDRO processing)
- Investment-related information for each investment option (expense ratio, performance data, benchmark comparison)

**Platform requirements:**
- Generate the 404(a)(5) disclosure at least annually
- Update and re-deliver when material changes occur
- Deliver to participants in a form they can keep
- Track delivery

---

## 4. SPD — Version Control Requirements

The SPD must accurately describe the plan as it currently operates. When a plan is amended, either the SPD must be updated or an SMM issued.

**Platform requirements:**
- Maintain version-controlled SPD documents with effective dates
- Link each SPD version to the corresponding plan document/adoption agreement version
- Deliver the current SPD to new participants within required deadlines
- Produce any historical SPD version on request (for audit or participant inquiries)

---

## 5. Annual Lifetime Income Statement (SECURE 2.0)

Plans must include a lifetime income illustration in at least one participant statement per year, showing the projected monthly income that the participant's account balance could generate at retirement.

**Platform requirements:**
- Use IRS-prescribed assumptions for the lifetime income projection (do not create custom assumptions)
- Generate the illustration using the participant's current vested account balance
- Deliver with the annual participant statement
- Provide a safe harbor explanation that the illustration is a projection, not a guarantee

[DATE-VERIFY — confirm current IRS model disclosure and required assumptions]

---

## 6. Notice Delivery Failure Handling

When a notice delivery fails (undeliverable email, returned mail):
- Log the failed delivery attempt with timestamp and error
- Generate an alert for the plan sponsor or administrator to resolve
- Document follow-up action taken
- Maintain the failed delivery record for audit purposes

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — All notice requirements. Failure to deliver required notices is an ERISA violation.
- Always **[DATE-VERIFY]** timing requirements before finalizing any notice delivery requirement — regulatory deadlines shift with legislation and rulemaking.
- Notice delivery tracking is non-negotiable — the platform must log every generation, delivery, confirmation, and failure.
- The platform must support both electronic and paper delivery for all required notices.
- 402(f) notice is a prerequisite to distribution processing — no ERD may be initiated without confirmed notice delivery or participant waiver.

---

## Sources

- ERISA Sections 101, 104, 105, 204 | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DOL Regulation 29 CFR 2550.404a-5 (Fee Disclosure) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DOL Electronic Disclosure Final Rule (2020) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRC Section 402(f) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (P.L. 117-328) — Lifetime Income Statement provisions | https://www.congress.gov | Retrieved 2026-03-06
