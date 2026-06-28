# Skill: Payroll System Integration
**Skill-ID:** 28-Payroll-System-Integration
**World:** Retirement World v1.0
**Category:** Technology & System Landscape
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines payroll system integration patterns, data formats, common failure modes, and the 360° bidirectional integration concept. Payroll integration is the primary data input channel for the recordkeeping platform — errors here propagate into participant accounts, compliance testing, and financial records.

---

## 1. Integration Patterns

### File-Based Integration

**Description:** The payroll system produces a structured data file delivered via SFTP (Secure File Transfer Protocol) or other secure transfer method on the plan's payroll schedule.

**Common formats:**
- **Fixed-width:** Fields at defined character positions. Legacy format; common in older payroll systems. Error-prone if field definitions shift. Requires precise positional mapping.
- **CSV / Delimited:** Fields separated by a delimiter (comma, pipe, tab). More flexible than fixed-width; requires header validation and delimiter consistency.
- **SPARK Institute Standard Formats:** Industry-standard field layouts for contribution, census, loan, and distribution data. Using SPARK-standard formats reduces custom integration work.

**Timing:** Batch delivery per payroll cycle (daily, weekly, bi-weekly, semi-monthly, monthly).

**Platform requirements:**
- Monitor SFTP location for incoming files
- Validate file format on receipt before processing
- Detect and reject duplicate file submissions (file hash or payroll period header comparison)
- Log file receipt, record count, and processing status

### API-Based Integration (SPARK Institute June 2025 Standards)

**Description:** Real-time or scheduled data exchange via RESTful APIs, per SPARK Institute API Integration Guidelines (June 2025).

**Key APIs defined by SPARK June 2025:**
| API | Purpose |
|---|---|
| **Census API** | Employee demographic and eligibility data |
| **Contribution API** | Payroll contribution amounts by employee and source |
| **Loan API** | Loan origination, repayment schedule, and payoff data |
| **Distribution API** | Distribution requests and status |
| **Participant Balance API** | Account balance data for payroll use (loan repayment, benefit calculations) |

**Payload format:** JSON.

**Timing:** Event-driven or scheduled; supports real-time validation and faster contribution processing compared to batch file delivery.

**Platform requirements:**
- Implement SPARK June 2025 API endpoints as the standard for new payroll integrations
- Authenticate API connections with industry-standard security (OAuth 2.0 or equivalent)
- Handle API timeouts, retry logic, and error responses
- Return validation results synchronously or via callback per SPARK API specification

---

## 2. 360° Integration (Bidirectional)

360° integration refers to bidirectional data exchange between the payroll system and the recordkeeper.

**Payroll → Recordkeeper (inbound):**
- Contribution amounts by participant and source
- Census updates (new hires, terminations, demographic changes, hours)
- Compensation data for limit monitoring and testing

**Recordkeeper → Payroll (outbound):**
- Loan repayment schedule amounts (so payroll can set up deduction)
- Loan payoff confirmations (so payroll can stop loan deduction)
- Loan default notifications (so payroll can stop deduction)
- Distribution events (so payroll can adjust withholding)
- Vesting data (for benefit calculations)

**Platform requirements:**
- Support outbound data delivery to payroll systems via file or API
- Generate loan repayment schedule files/API responses upon loan origination
- Generate loan payoff and default notifications for payroll integration
- Deliver distribution and termination events to payroll

---

## 3. Payroll Source Code Mapping

Payroll systems encode contribution data using their own deduction codes. Mapping payroll deduction codes to the recordkeeper's money types is a critical integration configuration step.

**Common mapping challenges:**
- Multiple payroll deduction codes mapping to the same money type (e.g., two separate payroll codes for pre-tax deferral — regular and catch-up)
- Catch-up contributions not differentiated from regular deferrals in the payroll export
- Roth contributions not clearly distinguished from pre-tax deferrals (same deduction bucket in payroll)
- Loan repayments included in contribution files without clear labeling
- Partial payroll periods and off-cycle payrolls requiring manual mapping
- New deduction codes added by payroll system after initial integration setup

**Platform requirements:**
- Maintain a payroll source code mapping table per plan (payroll code → money type)
- Alert when an unrecognized payroll code is received — do not silently assign to a default money type
- Support multiple payroll codes mapping to the same money type
- Log mapping table changes with effective dates

---

## 4. Common Failure Modes and Exception Handling

| Failure Mode | Description | Handling |
|---|---|---|
| Unmatched participant | SSN or ID in payroll file does not match any participant record | Route to exception queue; alert plan sponsor |
| Invalid source code | Payroll deduction code not in the mapping table | Route to exception queue; alert for mapping update |
| Limit violation | Contribution would exceed deferral or 415 limit | Cap the contribution; alert participant and plan sponsor |
| Duplicate submission | Same payroll period file received twice | Reject duplicate; alert; require confirmation to resubmit |
| Invalid amounts | Zero, negative, or non-numeric contribution amount | Route to exception queue |
| Missing required fields | SSN, amount, or source missing | Route to exception queue |
| Incorrect payroll period | Payroll period date does not match expected schedule | Flag for review; do not auto-reject |
| Wrong file format | File format does not match configured format | Reject file; alert |
| Wire mismatch | Funding wire amount does not match posted contributions | Hold; alert for reconciliation |

---

## 5. Integration Testing Requirements

Before activating a payroll integration, the following testing must be performed:

1. **Format validation test:** Submit a sample file and verify the platform correctly parses all fields
2. **Mapping validation test:** Verify all payroll source codes are correctly mapped to money types
3. **Participant matching test:** Verify all participant SSNs/IDs match records in the platform
4. **Limit monitoring test:** Verify the platform correctly identifies and handles contributions approaching limits
5. **Exception handling test:** Submit records with known errors and verify correct exception queue routing
6. **End-to-end test:** Full payroll cycle test including posting, investment allocation, and trust reconciliation

---

## 6. Handling Payroll System Changes

When a plan sponsor changes payroll providers or when the payroll system changes its output format:
- New integration must be configured and tested before the old integration is deactivated
- Run both integrations in parallel for at least one payroll cycle
- Verify the new integration produces identical results to the old integration for the same input data
- Update payroll source code mapping table for the new system's codes
- Do not go live with the new integration without sign-off from the plan sponsor and TPA

---

## Agent Rules

- **SPARK Institute API Integration Guidelines (June 2025)** is the industry standard for new API-based integrations. Requirements for API integrations must reference these guidelines.
- Payroll source code mapping is plan-specific — there is no universal mapping. Every plan requires its own mapping configuration.
- An unrecognized payroll source code must never be silently assigned to a default money type — it must route to the exception queue.
- 360° integration is bidirectional — requirements for payroll integration must include outbound data flows (loan repayments, distribution events) as well as inbound contribution data.
- Duplicate payroll file detection is mandatory — double-posting a payroll cycle creates over-contributions and potential 415 violations.

---

## Sources

- SPARK Institute API Integration Guidelines, June 2025 | https://www.sparkinstitute.org | Retrieved 2026-03-06
- SPARK Institute Standard File Formats | https://www.sparkinstitute.org | Retrieved 2026-03-06
- DOL Contribution Deposit Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Payroll Integration Resources | https://www.asppa.org | Retrieved 2026-03-06
