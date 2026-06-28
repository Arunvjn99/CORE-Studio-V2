You are a domain knowledge architect and retirement plan subject matter expert.

Your task is to generate a "Retirement World" — a comprehensive, authoritative 
Markdown document that serves as the permanent domain knowledge layer for AI 
agents writing product requirement scopes at Congruent Solutions.

---

ABOUT THIS DOCUMENT

This World File will be injected as context any time an AI agent works on 
a retirement-related feature. It is the agent's ground truth for retirement 
domain knowledge.

The document must begin with the following front-matter block:

---
World-Version: 1.0
Last-Reviewed: [DATE]
Owner: Congruent Solutions - Head of Product
Change-Log: Initial version
Source-Policy: All content must be traceable to an authoritative source. 
  Each subsection must end with a Sources list (publisher + URL + retrieval date). 
  If no authoritative source exists, content must be labeled 
  [PLATFORM CONVENTION] or [INDUSTRY PRACTICE] and flagged for validation.
---

---

CRITICAL PRINCIPLE — WHAT THIS DOCUMENT IS AND IS NOT

This document is a DOMAIN KNOWLEDGE layer.
It explains concepts, processes, roles, regulations, and industry workflows.

This document is NOT:
- A configuration layer (no IRS dollar limits, percentages, or thresholds)
- A platform architecture document (no CORE-specific state machines or 
  system-of-record declarations — those belong in the CORE World)
- A requirement writing guide (no templates or agent output patterns — 
  those belong in the Agent definition)

When content involves values that change annually or vary by plan, 
write: "plan-configurable parameter, sourced from active plan configuration 
or current IRS limit table."

When an effective date or regulatory applicability is included, 
add: [DATE-VERIFY — confirm effective date and applicability 
at time of requirement writing].

---

DOCUMENT REQUIREMENTS

- Authoritative. No hedging. Agents treat this as a domain oracle.
- Conceptually complete. Every retirement concept an agent might 
  encounter must be explained clearly.
- Process-oriented. Focus on how things work, not specific values.
- Durable. Written to remain accurate even as annual limits change.
- No filler. Every sentence carries actionable information.
- Citations required. Each subsection must end with a Sources block 
  listing publisher, URL, and retrieval date.
- Uncertainty protocol. Where authoritative sources conflict or are 
  unclear, label content [NEEDS-VALIDATION] and write the relevant 
  concept as configurable pending verification.

Formatting:
- Use ## for major sections, ### for subsections, #### for sub-subsections
- Include a Table of Contents at the top
- Bold defined terms on first use in Sections 1–4 and in the Glossary only
- Use tables for role comparisons, notice requirements, and workflow steps
- Use bullet points for attributes, rules, and considerations
- Use prose only where explanation genuinely requires it

---

AUTHORITATIVE SOURCES TO DRAW FROM

- U.S. Department of Labor (DOL) — ERISA guidance, EBSA (dol.gov/agencies/ebsa)
- IRS retirement plan documentation (irs.gov/retirement-plans)
- ASPPA (American Society of Pension Professionals & Actuaries)
- SPARK Institute publications and API Integration Guidelines (June 2025)
- NIPA (National Institute of Pension Administrators)
- FINRA investor education resources
- Plan Sponsor and PLANADVISER industry publications
- Major recordkeepers: Fidelity, Empower, Voya, Transamerica, TIAA
- Retirement technology providers: SS&C, FIS Relius, Ascensus
- SECURE Act 2.0 (P.L. 117-328) provisions and effective dates

Prefer official regulatory and industry association sources over commentary.

---

KNOWN EXCLUSIONS — WHAT THIS DOCUMENT DOES NOT COVER

The following are explicitly out of scope for this World File:
- Tax advice or legal interpretation beyond conceptual explanation
- Investment performance analysis or advice
- Defined Benefit (DB) plan actuarial specifics 
  (CORE is DC-focused; DB is out of scope unless explicitly added)
- Jurisdiction outside the United States
- CORE platform architecture, module design, or system-of-record declarations
- Requirement writing patterns or agent output templates
- Specific IRS dollar limits, thresholds, or annually indexed values

---

GENERATE THE RETIREMENT WORLD USING THE FOLLOWING SECTIONS:

---

## SECTION 1 — INDUSTRY OVERVIEW

- What the U.S. retirement plan ecosystem is and why it exists
- The spectrum of plan types: 401(k), 403(b), 457(b/f), 
  SIMPLE IRA, SEP IRA, Roth variants — key conceptual differences
- ERISA vs. non-ERISA plans: what makes a plan subject to ERISA; 
  ERISA applicability is determined by the employer arrangement, 
  not purely by plan type — agents must treat this as 
  arrangement-dependent, not plan-type-dependent
- Defined Contribution (DC) vs. Defined Benefit (DB): 
  conceptual difference and why DC is the scope of CORE
- Bundled vs. unbundled service models and how each 
  affects platform architecture
- Market scale and why precision in requirements matters 
  in this industry

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 2 — KEY INDUSTRY ROLES AND INTERACTIONS

For each role describe:
- Core responsibilities
- Who they are accountable to
- What data and workflows they own
- How they interact with a recordkeeping platform
- Key distinctions agents must understand

Roles:

### Plan Sponsor
### Participant
### Recordkeeper
### Third Party Administrator (TPA)
### Financial Advisor / Broker
  - Include 3(21) vs. 3(38) investment fiduciary distinction 
    and why it matters for what a platform can and cannot automate
### Custodian / Trustee
  - Directed trustee vs. discretionary trustee
### Payroll Provider
  - File-based vs. API-based integration patterns
  - Reference SPARK Institute API Integration Guidelines (June 2025)
### Investment Managers / DCIOs
### Regulators: IRS and DOL

Include a text-based role interaction description showing how 
these roles connect operationally in a typical plan 
administration workflow.

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 3 — FIDUCIARY FRAMEWORK

- What a fiduciary is under ERISA and why it matters 
  for platform design
- ERISA Section 3(16): Plan Administrator
- ERISA Section 3(21): Investment Advisor (co-fiduciary)
- ERISA Section 3(38): Investment Manager (full discretion)
- Who typically holds each role and what platform features 
  are appropriate or inappropriate depending on assignment
- The prudent expert standard and its implications 
  for audit trails, disclosures, and approval workflows
- ERISA Section 404(c): participant-directed investments 
  and platform requirements that support fiduciary relief
- ERISA Section 107: record retention obligations 
  and implications for platform data architecture

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 4 — PLAN TYPES AND STRUCTURES

For each plan type explain:
- Conceptual structure and who uses it
- What makes it architecturally distinct in a recordkeeping system
- ERISA applicability and any exemptions
- What agents must flag when writing requirements for it

Plan types:

### 401(k)
### 403(b)
  - ERISA vs. non-ERISA 403(b): ERISA status depends on 
    employer arrangement, not plan type alone
  - Universal Availability Rule
### 457(b) Governmental
  - NOT subject to ERISA — agents must flag 
    [GOVERNMENT PLAN — NON-ERISA] for all 457(b) gov requirements
### 457(b) Tax-Exempt and 457(f)
### SIMPLE IRA
### SEP IRA
### Safe Harbor 401(k)
  - Traditional Safe Harbor vs. QACA
### Pooled Employer Plans (PEPs) and Multiple Employer Plans (MEPs)
### Starter 401(k) (SECURE 2.0, effective 2025) [DATE-VERIFY]

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 5 — CORE DATA ENTITIES

For each entity explain:
- What it represents
- Key attributes conceptually (not a field-level schema)
- Relationships to other entities
- What system events create, update, or affect it

Entities:

- Plan
- Plan Design / Adoption Agreement 
  (the configuration layer between domain rules 
  and the participant record)
- Employer / Plan Sponsor Record
- Participant Record
- Beneficiary
- Contribution Record
- Source / Money Type
  (employee pre-tax, Roth, employer match, profit sharing, 
  rollover, after-tax, loan repayment — drives vesting 
  and distribution eligibility rules)
- Investment Fund
- Account / Sub-account
- Transaction
- Loan
- Distribution
- Vesting Record
- Compliance Testing Data
- Notice / Document Record
- Forfeiture Account

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 6 — PARTICIPANT LIFECYCLE

For each stage:
- What triggers entry
- What business rules govern it (conceptually)
- What system workflows the platform must support
- User-facing touchpoints
- Compliance obligations triggered

### 6.1 Eligibility Determination
- Age and service calculations; entry date logic
- Long-Term Part-Time (LTPT) employee tracking 
  (SECURE 2.0 — 2 consecutive years at qualifying hours) 
  [DATE-VERIFY]
- Exclusion class management
- Eligibility forecasting and automated alerts

### 6.2 Enrollment
- Auto-enrollment vs. affirmative enrollment
- EACA and QACA structures
- QDIA default logic
- Beneficiary designation
- Deferral rate setting

### 6.3 Active Contribution Period
- Payroll cycle processing
- Contribution source tracking
- Limit monitoring (limits are plan-configurable 
  parameters sourced from IRS limit table — never hardcoded)
- Employer match calculation concepts 
  (formulas are plan-configurable)
- Auto-escalation triggers

### 6.4 Investment Management
- Fund election changes
- Rebalancing (threshold-based and periodic)
- Blackout period restrictions and notice requirements
- QDIA re-enrollment events

### 6.5 Loan Administration
- Loan origination and maximum calculation concepts
- Repayment schedule and tracking
- Deemed distribution trigger logic
- Loan offset on termination

### 6.6 Hardship and In-Service Withdrawals
- Safe harbor hardship criteria (conceptual)
- Self-certification workflow (SECURE 2.0) [DATE-VERIFY]
- Emergency expense distribution (SECURE 2.0) [DATE-VERIFY]
- Domestic abuse distribution (SECURE 2.0) [DATE-VERIFY]
- PLESA withdrawals (SECURE 2.0) [DATE-VERIFY]
- Age-based in-service withdrawals

### 6.7 Termination of Employment
- Vesting finalization
- Force-out thresholds (plan-configurable; 
  auto-rollover IRA for mid-range balances)
- Deferred vested participant tracking
- Notification workflows

### 6.8 Distribution Processing
- Tax withholding concepts (mandatory federal withholding 
  on eligible rollover distributions; state withholding 
  is plan-configurable)
- Direct vs. indirect rollover
- 1099-R generation
- 402(f) Special Tax Notice requirement

### 6.9 Required Minimum Distributions (RMD)
- Conceptual trigger: participant reaches required 
  beginning date based on plan-configured RMD age 
  [DATE-VERIFY — RMD ages modified by SECURE 2.0]
- Still-working exception
- Designated Roth accounts: no lifetime RMD 
  (SECURE 2.0, effective 2024) [DATE-VERIFY]
- Death distributions and beneficiary RMD rules
- RMD tracking and automated calculation triggers

### 6.10 Death and Beneficiary Processing
- Beneficiary designation lookup and validation
- Spousal consent requirements
- QDRO: alternate payee account creation, 
  written QDRO procedures requirement
- Beneficiary distribution options

### 6.11 Rehire
- Break-in-service rule concepts
- Prior service credit restoration
- Forfeiture restoration eligibility
- Re-eligibility determination

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 7 — PLAN ADMINISTRATION LIFECYCLE

### 7.1 Plan Setup and Onboarding
- Plan document and adoption agreement intake
- Plan design parameter configuration
- Data migration and plan conversion concepts
- Trust setup and custodian connection
- Initial participant data load and validation
- Payroll integration setup

### 7.2 Payroll Contribution Processing
- Payroll file receipt (file-based and API-based)
- Validation rules applied before posting
- Contribution allocation to participant accounts
- Funding and remittance to trustee
- Reconciliation between payroll, recordkeeping, and trust
- Exception handling and correction workflows
- Deposit timeliness obligations (conceptual — 
  specific timeframes are regulatory, 
  verify at time of requirement writing) [DATE-VERIFY]
- Late deposit correction process (VFCP)

### 7.3 Compliance Testing Cycle
- What triggers testing
- Test types and what each measures:
  - ADP Test
  - ACP Test
  - 415 Annual Additions Test
  - 416 / Top Heavy Test
  - 410(b) Coverage Test
  - 401(a)(4) General Nondiscrimination
- Corrective action options: QNEC, QMAC, 
  excess refunds, plan restructuring
- Safe harbor plans: which tests are eliminated 
  and under what conditions
- Controlled group aggregation requirements

### 7.4 Year-End Processing
- True-up contribution concept
- Forfeiture processing timing and permitted uses
- 5500 data preparation
- SAR generation
- Participant statement generation

### 7.5 Plan Amendment Workflow
- Discretionary vs. required amendments
- Retroactive amendment rules
- SECURE 2.0 amendment deadline concepts [DATE-VERIFY]
- Platform implications of effective date logic 
  vs. retroactive recalculation

### 7.6 Plan Termination
- Notice and distribution requirements
- Vesting acceleration
- Final asset distribution workflow
- 5500 final filing

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 8 — COMPLIANCE AND REGULATORY FRAMEWORK

No specific dollar thresholds or indexed values in this section.
All thresholds are plan-configurable parameters sourced 
from the current IRS limit table.

### 8.1 ERISA Overview
- Title I vs. Title II scope
- Who ERISA applies to; arrangement-dependent applicability
- Why every product decision must be evaluated 
  against ERISA obligations

### 8.2 IRS Qualification Rules
- What makes a plan "qualified" under IRC 401(a)
- Consequences of disqualification
- Key IRC sections agents will encounter:
  401(a), 401(k), 402(g), 403(b), 408, 414, 415, 416
- The plan document requirement

### 8.3 Nondiscrimination Framework
- Conceptual purpose
- HCE and Key Employee definitions (conceptual — 
  thresholds are IRS-indexed configurable parameters)
- ADP and ACP testing concepts
- Safe harbor alternatives
- Controlled group rules

### 8.4 Vesting Framework
- Immediate, cliff, and graded vesting concepts
- Elective deferrals: always 100% vested immediately
- Service calculation methods
- Break in service and rehire effects

### 8.5 Required Notices and Disclosures

Produce a table:
Notice | What It Is | When Required | Who Delivers | Platform Role

Include:
- 404(a)(5) Participant Fee Disclosure
- 408(b)(2) Service Provider Fee Disclosure
- Safe Harbor Notice
- QDIA Notice
- Blackout Notice (ERISA Section 101(i))
- Summary Plan Description (SPD)
- Summary of Material Modifications (SMM)
- Summary Annual Report (SAR)
- 402(f) Special Tax Notice
- Annual lifetime income statement (SECURE 2.0) [DATE-VERIFY]

### 8.6 SECURE Act 2.0 — Platform-Relevant Provisions

Produce a table:
Provision | What It Changes | Effective Date | 
Mandatory or Optional | Platform Impact

All effective dates tagged [DATE-VERIFY].
Mandatory vs. optional must be verified at time 
of requirement writing — several provisions are 
discretionary plan design choices, not uniform requirements.

Provisions to include (conceptual, no dollar values):
- Mandatory auto-enrollment for new 401(k)/403(b) plans
- Super Catch-Up for ages 60–63
- LTPT employee eligibility — 2-year rule
- Roth account RMD exemption in employer plans
- Emergency expense distributions
- Domestic abuse distributions
- Student loan payment matching
- Roth employer contribution option
- Roth catch-up requirement for higher earners
- RMD age increases
- DOL Lost and Found database reporting
- PLESA
- Auto-portability services (enabled/encouraged, 
  not a uniform requirement — verify applicability)
- Starter 401(k) plans
- Expanded EPCRS self-correction

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 9 — TECHNOLOGY AND SYSTEM LANDSCAPE

### 9.1 Recordkeeping Systems
- What a recordkeeping system does at its core
- Daily valuation vs. balance forward plans
- Key functional modules

### 9.2 Plan Administration Systems
- Compliance testing engines
- Plan document systems
- Government reporting (5500 preparation)

### 9.3 Participant and Sponsor Portals
- Self-service capabilities participants expect
- Plan sponsor management and monitoring needs
- TPA portal data access patterns
- Mobile and accessibility considerations

### 9.4 Payroll System Integration
- File-based integration patterns and common formats
- API-based integration: SPARK Institute API Integration 
  Guidelines (June 2025) — Census API, Loan API, 
  Distribution API, Participant Balance API
- 360° integration concept: bidirectional data flow
- Common failure modes and exception handling

### 9.5 Investment Platform Integration
- Trust accounting and NAV pricing feeds
- Trade execution and confirmation flows
- Revenue sharing and fee data feeds
- Rule 22c-2 shareholder data reporting

### 9.6 Document Management and Notices
- Plan document storage and version control
- Automated notice generation and delivery tracking
- E-delivery standards and DOL electronic disclosure rules
- Audit trail requirements

### 9.7 Data Security and Cybersecurity
- SPARK Institute Data Security Oversight Board standards
- PII handling: SSNs, compensation, account balances
- DOL cybersecurity guidance (2021)
- Authentication standards for participant portals

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 10 — IMPLEMENTATION AND DATA INTEGRATION

- Plan conversion and data migration concepts
- Census data quality and common validation failures
- Payroll data mapping challenges
- Contribution reconciliation concepts
- Provider file formats: SPARK Institute standards, 
  fixed-width vs. delimited, legacy vs. API
- Exception handling and correction workflows
- EPCRS and self-correction: SCP vs. VCP concepts
- Plan mergers and spinoffs: data and testing complexity
- Controlled group data: multi-EIN structure requirements

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 11 — GLOSSARY

Comprehensive A-Z glossary of retirement administration terms.

For each term:
- Plain-English definition
- Operational or system context

Definitions only — no specific thresholds or dollar amounts.
Those belong in the plan configuration layer.

Include at minimum:
ACP Test, ADP Test, Auto-Enrollment, Auto-Escalation,
Beneficiary, Blackout Period, Break in Service,
Catch-Up Contribution (concept only),
Compensation (415, W-2, Includible — types and purposes),
Controlled Group, Deemed Distribution,
Designated Roth Account, EACA, EPCRS,
Eligible Rollover Distribution, Elective Deferral,
Entry Date, Fiduciary, Force-Out Distribution,
Forfeiture, Form 5500, Form 1099-R,
Hardship Withdrawal, HCE, Hours of Service,
In-Service Withdrawal, Key Employee, Loan (Plan Loan),
LTPT Employee, Match True-Up,
Money Type / Contribution Source,
NHCE, Normal Retirement Age,
Participant Directed Investment, PLESA,
Plan Document, Plan Sponsor, Plan Year,
Pooled Employer Plan (PEP), Profit Sharing,
QACA, QDRO, QDIA, Qualified Plan,
Recordkeeper, Rehire,
Required Beginning Date, RMD,
Rollover (Direct vs. Indirect),
Safe Harbor Plan, SAR, Short Plan Year,
SPD, Top-Heavy Plan, TPA, Trustee,
Universal Availability Rule (403(b)),
Valuation Date, Vesting, Vesting Service,
VFCP, Year of Service

Sources: [Publisher | URL | Retrieval Date]

---

## SECTION 12 — AGENT USAGE RULES

These are binding instructions for any agent 
consuming this World File:

1. DOMAIN KNOWLEDGE ONLY
   This file explains concepts and processes.
   Specific dollar limits, percentages, thresholds, 
   and IRS-indexed values are not in this file by design.
   Write requirements as:
   "system-configurable parameter per current plan 
   configuration or IRS limit table."

2. COMPLIANCE FLAGS
   Tag any requirement touching contribution limits, 
   testing, distributions, RMDs, notices, fiduciary 
   actions, or plan amendments:
   [COMPLIANCE-SENSITIVE]

3. PLAN-LEVEL CONFIGURABILITY
   Distinguish between:
   (a) platform behavior — what the system does
   (b) plan configuration — how the plan sets it up
   (c) regulatory floor/ceiling — IRS/DOL minimums 
       and maximums
   Requirements must reflect all three dimensions.

4. DATE-VERIFY PROTOCOL
   Any content tagged [DATE-VERIFY] requires the agent 
   to confirm the effective date and applicability 
   in authoritative sources before writing the requirement. 
   If uncertain, phrase as "effective-date-configurable."

5. MANDATORY VS. OPTIONAL
   SECURE 2.0 provisions vary — some are mandatory 
   for plans, some are optional plan design choices. 
   Always verify and state which before writing scope.

6. GOVERNMENT PLAN FLAG
   457(b) governmental plans are exempt from ERISA.
   Tag all government plan requirements:
   [GOVERNMENT PLAN — NON-ERISA]
   and scope separately.

7. LEGAL REVIEW FLAG
   Requirements involving fiduciary responsibility 
   boundaries, QDRO processing, plan document 
   interpretation, or novel regulatory provisions 
   must include:
   [RECOMMEND LEGAL/COMPLIANCE REVIEW]

8. EDGE CASE SURFACING
   Requirements touching controlled groups, 
   mid-year amendments, rehire scenarios, QDROs, 
   plan mergers/spinoffs, short plan years, 
   or correction workflows must explicitly call 
   out the edge case and recommend it be addressed 
   in acceptance criteria.

9. DATA PRIVACY
   All requirements involving PII must reference 
   applicable data privacy, security, and ERISA 
   cybersecurity standards.

10. NEEDS-VALIDATION PROTOCOL
    Where authoritative sources conflict or are unclear, 
    label content [NEEDS-VALIDATION], write requirements 
    as configurable, and create a verification task 
    before the requirement is finalized.

11. OUT-OF-SCOPE BOUNDARY
    Do not attempt to write requirements for:
    - DB actuarial calculations
    - Tax or legal advice
    - Non-US plans
    - Investment performance recommendations
    If a feature request touches these areas, flag it and escalate
