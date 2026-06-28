# Skill: Document Management and Notices
**Skill-ID:** 30-Document-Management-and-Notices
**World:** Retirement World v1.0
**Category:** Technology & System Landscape
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the platform's document management and notice delivery capabilities — plan document version control, automated notice generation, electronic and paper delivery, audit trail requirements, and DOL e-delivery compliance. Document management is a compliance-critical function; the inability to produce a plan document or prove notice delivery creates legal exposure.

---

## 1. Plan Document Version Control

The plan document and adoption agreement must be stored with version control because:
- DOL audits may request the plan document in effect on any given date in the past 6+ years
- Plan amendments create new versions; each version has its own effective date
- Retroactive amendments require the platform to know which version was in effect at each point in time
- Participants and alternate payees have the right to receive a copy of the plan documents

**Version control requirements:**
- Each plan document version is stored with: document type, version number, adoption date, effective date, and the user who uploaded it
- When an amendment is adopted, the prior version is archived (not deleted) and a new current version is established
- The platform must be able to retrieve the plan document version in effect on any specified date
- Amendments are linked to the plan configuration changes they authorize

**Document types requiring version control:**
- Plan document (base document)
- Adoption agreement (all versions)
- Amendments (numbered and dated)
- Summary Plan Description (SPD) and all updates
- Summary of Material Modifications (SMM)
- Loan policy (if separate document)
- QDRO procedures

---

## 2. Automated Notice Generation

The platform must automatically generate required notices triggered by plan events, without requiring manual initiation for each notice.

**Trigger-based notice generation:**

| Notice | Triggering Event |
|---|---|
| Enrollment notice / Auto-enrollment notice | Participant reaches eligibility / entry date |
| QDIA notice | Participant's first QDIA investment |
| Safe harbor notice | Annually, at plan year start |
| 402(f) Special Tax Notice | Distribution request initiated |
| Blackout notice | Blackout period configured in the system |
| RMD notice | Participant approaches required beginning date |
| Force-out notice | Terminated participant balance falls below threshold |
| Plan termination notice | Plan termination event |
| SAR | Annually, after 5500 filing |
| Annual fee disclosure (404(a)(5)) | Annually and upon enrollment |
| Loan default notice | Loan enters delinquency |
| Auto-escalation notice | Before escalation date |

**Platform requirements:**
- Maintain a notice calendar that tracks all scheduled notices across all plans
- Generate notices automatically on the triggering event without manual intervention
- Allow template customization for plan-specific content within regulatory requirements
- Queue generated notices for delivery via the configured delivery method

---

## 3. Electronic Delivery (DOL Final Rule 2020)

The DOL's electronic disclosure safe harbor allows electronic delivery of required disclosures under specified conditions. [DATE-VERIFY — confirm current DOL e-delivery rule requirements]

**Safe harbor conditions (summarized):**
- The notice or disclosure is made available on a website (or delivered via email) accessible by the participant
- The participant is notified of the availability of documents and their right to request paper
- The participant is provided with a way to access the documents (website URL or email with attachment)
- The participant has the ability to request paper copies at no charge at any time

**Access persons (participants with known email):**
- Participants with an email address on file can receive notices by email

**Non-access persons (participants without known email):**
- Must receive default paper delivery unless an alternative electronic method is established

**Platform requirements:**
- Maintain delivery preference per participant (electronic or paper)
- Support email delivery with delivery tracking (delivery confirmation, open tracking)
- Support website posting with notification email
- Process paper delivery requests promptly and at no charge to the participant
- Identify "non-access persons" and route to paper delivery

---

## 4. Paper Delivery

For participants who request paper delivery or who do not have electronic delivery configured:
- Notice is printed and mailed to the participant's address on file
- Return of mail (undeliverable mail) must be handled — trigger search workflow for updated address
- Track paper delivery via mail log (date mailed, address used)

**Platform requirements:**
- Support paper delivery fulfillment (print, mail, or batch with a mailing vendor)
- Log paper delivery date and address
- Handle returned mail: flag participant record; trigger address search workflow
- Alert plan sponsor of undeliverable notices

---

## 5. Delivery Tracking and Audit Trail

Every notice delivery event must be logged:

| Event | Data to Log |
|---|---|
| Notice generated | Timestamp, notice type, participant/plan ID, document version |
| Electronic delivery attempt | Timestamp, delivery method, email address or website |
| Email delivery confirmed | Timestamp, delivery confirmation (open receipt or delivery receipt) |
| Paper delivery | Timestamp, date mailed, address |
| Delivery failure | Timestamp, failure reason, follow-up action taken |
| Participant requests paper copy | Timestamp, participant ID, paper delivery date |

**Retention:** All delivery records must be retained for the ERISA Section 107 minimum retention period (at least 6 years). [DATE-VERIFY]

---

## 6. Document Storage and Access

**Document storage requirements:**
- All plan documents (current and historical versions) stored securely with role-based access
- Participant-specific documents (distribution confirmations, loan notes, beneficiary designations) stored in the participant record
- All documents stored with retention metadata (document type, effective date, retention expiry)

**Access controls:**
- Plan sponsor portal: access to plan documents; no access to other plans' documents
- TPA portal: access to plan documents for their administered plans; no access to PII beyond what is necessary for their administrative function
- Participant portal: access to their own notices, statements, tax documents; no access to other participants' documents
- Admin/operations: role-scoped access; all access logged

**Retrieval for audits:**
- Platform must support production of any document in response to a DOL audit request within a reasonable timeframe
- Search capability: find all documents by participant, date range, notice type, or plan

---

## 7. SMM and Plan Amendment Communication

When a plan is materially amended, the plan administrator must issue a Summary of Material Modifications (SMM) within the required timeframe. [DATE-VERIFY — currently within 210 days after the end of the plan year in which the change was adopted]

**Platform workflow:**
- When a plan amendment is processed in the platform, flag whether the amendment constitutes a material modification requiring an SMM
- Generate an SMM template pre-populated with the plan's name and effective change date
- Track SMM delivery to all participants

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Notice delivery tracking is non-negotiable. The inability to prove delivery of a required notice is an ERISA compliance failure.
- Plan document version control must support retrieval of any historical version by effective date — "current version only" storage is insufficient for a DOL audit environment.
- DOL e-delivery safe harbor conditions must all be met; partial compliance does not establish the safe harbor. [DATE-VERIFY — confirm current requirements]
- Returned/undeliverable mail must trigger an active address search workflow — do not simply log and ignore.
- Access controls for documents must be role-scoped — participants should never have access to other participants' documents; TPAs should not have broader PII access than their administrative role requires.

---

## Sources

- DOL Electronic Disclosure Final Rule (2020) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ERISA Section 107 (Record Retention) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ERISA Sections 101, 104 (Disclosure Requirements) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DOL Regulation 29 CFR 2520.104b-1 (Disclosure) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
