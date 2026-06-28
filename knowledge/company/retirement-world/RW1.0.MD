---
World-Version: 1.0
Last-Reviewed: 2026-03-06
Owner: Congruent Solutions - Head of Product
Change-Log: Initial version
Source-Policy: All content must be traceable to an authoritative source. Each subsection must end with a Sources list (publisher + URL + retrieval date). If no authoritative source exists, content must be labeled [PLATFORM CONVENTION] or [INDUSTRY PRACTICE] and flagged for validation.
---

# Retirement World — Domain Knowledge Layer

> **Purpose:** This document is the permanent domain knowledge layer for AI agents writing product requirement scopes at Congruent Solutions. It is injected as context any time an agent works on a retirement-related feature. It is the agent's ground truth for retirement domain knowledge.
>
> **This document IS:** A domain knowledge layer explaining concepts, processes, roles, regulations, and industry workflows.
>
> **This document IS NOT:** A configuration layer, a platform architecture document, or a requirement writing guide.
>
> When content involves values that change annually or vary by plan, write: *"plan-configurable parameter, sourced from active plan configuration or current IRS limit table."*
>
> When an effective date or regulatory applicability is included, add: **[DATE-VERIFY — confirm effective date and applicability at time of requirement writing]**

---

## Table of Contents

- [Section 1 — Industry Overview](#section-1--industry-overview)
- [Section 2 — Key Industry Roles and Interactions](#section-2--key-industry-roles-and-interactions)
- [Section 3 — Fiduciary Framework](#section-3--fiduciary-framework)
- [Section 4 — Plan Types and Structures](#section-4--plan-types-and-structures)
- [Section 5 — Core Data Entities](#section-5--core-data-entities)
- [Section 6 — Participant Lifecycle](#section-6--participant-lifecycle)
- [Section 7 — Plan Administration Lifecycle](#section-7--plan-administration-lifecycle)
- [Section 8 — Compliance and Regulatory Framework](#section-8--compliance-and-regulatory-framework)
- [Section 9 — Technology and System Landscape](#section-9--technology-and-system-landscape)
- [Section 10 — Implementation and Data Integration](#section-10--implementation-and-data-integration)
- [Section 11 — Glossary](#section-11--glossary)
- [Section 12 — Agent Usage Rules](#section-12--agent-usage-rules)

---

## Section 1 — Industry Overview

### 1.1 What the U.S. Retirement Plan Ecosystem Is and Why It Exists

The U.S. retirement plan ecosystem is a framework of tax-advantaged savings vehicles established by Congress to encourage employer-sponsored and individual retirement saving. The system is built on a deferred-taxation model: contributions and earnings grow on a tax-advantaged basis, with taxation deferred to the point of distribution (or, for Roth accounts, contributed on an after-tax basis with tax-free qualified distributions).

The ecosystem exists because Social Security alone is insufficient to replace pre-retirement income. Congress created incentives — primarily tax deductions for employers and tax deferral or exclusion for participants — to encourage widespread participation. These incentives are conditional: plans must satisfy qualification, nondiscrimination, and reporting requirements to maintain their tax-advantaged status.

The Department of Labor (DOL) and Internal Revenue Service (IRS) jointly regulate the system. The DOL oversees fiduciary conduct, participant rights, and plan administration under the Employee Retirement Income Security Act of 1974 (ERISA). The IRS administers tax qualification rules under the Internal Revenue Code (IRC).

### 1.2 Spectrum of Plan Types

The U.S. retirement plan landscape spans employer-sponsored qualified plans, governmental plans, and individual-account plans:

| Plan Type | Sponsoring Entity | Key Characteristic |
|---|---|---|
| **401(k)** | Private-sector employer | Elective deferrals; most common DC plan type |
| **403(b)** | Public schools, 501(c)(3) organizations | Similar to 401(k); ERISA applicability depends on employer arrangement |
| **457(b) Governmental** | State/local governments | Non-ERISA; separate contribution limits run concurrently with other plans |
| **457(b) Tax-Exempt** | Non-governmental tax-exempt organizations | ERISA-covered; top-hat plan rules may apply |
| **457(f)** | Tax-exempt employers | Ineligible plan with substantial risk of forfeiture; different tax treatment |
| **SIMPLE IRA** | Small employers (plan-configurable size threshold) | Simplified matching or non-elective contributions; lighter administrative burden |
| **SEP IRA** | Any employer, including self-employed | Employer-only contributions; no employee deferrals |
| **Roth 401(k) / Roth 403(b)** | Same sponsoring entities as above | After-tax designated Roth contributions within a qualified plan |
| **Safe Harbor 401(k)** | Private-sector employer | Satisfies ADP/ACP testing via required employer contributions |
| **PEP / MEP** | Pooled Plan Provider / group of employers | Multiple unrelated employers participate in one plan structure |

### 1.3 ERISA vs. Non-ERISA Plans

**ERISA** (Employee Retirement Income Security Act of 1974) applies to most private-sector employer-sponsored retirement plans. ERISA applicability is **arrangement-dependent**, not plan-type-dependent.

Key factors that determine ERISA applicability:
- Whether the plan is sponsored by a private-sector employer (ERISA applies) vs. a governmental entity or church (ERISA generally does not apply)
- Whether the employer exercises sufficient involvement to create an "employee benefit plan" under ERISA
- Whether a 403(b) plan meets the DOL's safe harbor for a non-ERISA arrangement (limited employer involvement, voluntary participation, no employer contributions beyond matching of employee deferrals, no employer endorsement)

**Agents must treat ERISA applicability as arrangement-dependent for every plan.** A 403(b) plan for a public school district is non-ERISA. A 403(b) plan for a private nonprofit hospital may be ERISA-covered. A governmental 457(b) is never subject to ERISA. These distinctions drive which fiduciary, notice, and reporting obligations apply.

Non-ERISA arrangements that agents will encounter:
- **Governmental plans** — state and local government employer plans; exempt from ERISA Titles I and II
- **Church plans** — plans maintained by churches; can elect ERISA coverage or remain exempt
- **Top-hat plans** — unfunded plans maintained for select management or highly compensated employees; exempt from most ERISA substantive requirements but subject to reporting

### 1.4 Defined Contribution vs. Defined Benefit

| Dimension | Defined Contribution (DC) | Defined Benefit (DB) |
|---|---|---|
| Promise to participant | Account balance based on contributions + investment returns | Specified monthly benefit at retirement |
| Investment risk | Borne by participant | Borne by employer/plan |
| Actuarial complexity | Not required | Required for funding calculations |
| Portability | High — account balance moves with participant | Lower — tied to service credit formulas |
| CORE platform scope | In scope | Out of scope (DB actuarial specifics excluded) |

CORE is a DC-focused recordkeeping platform. DB actuarial calculations, pension benefit formulas, and annuity valuation are outside scope unless explicitly added.

### 1.5 Bundled vs. Unbundled Service Models

**Bundled model:** A single provider (typically a large insurance company or financial institution) delivers recordkeeping, investment platform, and plan administration services under one contract. Plan sponsors deal with one vendor.

**Unbundled model:** Separate providers fill each role — recordkeeper, TPA, investment platform, custodian, and advisor are distinct entities. Data flows between systems via file-based or API-based integrations.

Platform architecture is significantly affected by service model:
- Bundled environments may have tighter system integration but less flexibility
- Unbundled environments require robust data exchange standards, reconciliation workflows, and multi-party coordination
- CORE operates in both models; requirements must specify which service model a given feature targets

### 1.6 Market Scale and Why Precision Matters

The U.S. defined contribution market holds trillions of dollars in retirement assets across tens of millions of participants. Errors in recordkeeping calculations — even minor rounding differences — aggregate into significant compliance exposure and participant harm at scale. A single payroll processing error affecting thousands of participants simultaneously illustrates why precision in requirement writing is non-negotiable. Every requirement must account for edge cases, compliance flags, and audit trail obligations.

**Sources:**
- U.S. Department of Labor, Employee Benefits Security Administration | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRS Retirement Plans | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- ERISA (P.L. 93-406, as amended) | https://www.dol.gov/general/topic/retirement/erisa | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov/bill/117th-congress/house-bill/2954 | Retrieved 2026-03-06

---

## Section 2 — Key Industry Roles and Interactions

### Plan Sponsor

- **Core responsibilities:** Adopts and maintains the retirement plan; signs the plan document and adoption agreement; makes plan design decisions; selects service providers; has ultimate responsibility for plan operation
- **Accountable to:** ERISA (as plan administrator if not delegated), DOL, IRS, plan participants and beneficiaries
- **Data and workflows owned:** Plan design parameters, employer contribution decisions, eligibility and entry date rules, investment menu selection (unless delegated to a 3(38)), amendment decisions, payroll data origination
- **Platform interaction:** Accesses plan sponsor portal for reporting, approval workflows, contribution remittance initiation, compliance test results review, and document access; may delegate administrative tasks to a TPA
- **Key distinctions:** The plan sponsor is the employer entity. They are typically a named fiduciary under ERISA. In many plans, the plan sponsor also serves as the ERISA Section 3(16) plan administrator unless that role is delegated to a TPA or outsourced provider.

### Participant

- **Core responsibilities:** Enrolls in the plan; directs elective deferrals; makes investment elections; manages account (loans, withdrawals, beneficiary designations); takes distributions at qualifying events
- **Accountable to:** Responsible for accuracy of self-reported information; bound by plan terms
- **Data and workflows owned:** Deferral rate elections, investment allocations, beneficiary designations, loan requests, distribution requests, contact information updates
- **Platform interaction:** Participant portal (web and mobile) for enrollment, deferral changes, investment changes, account balance viewing, transaction history, loan origination, and distribution requests
- **Key distinctions:** Participants are the beneficial owners of their individual account balances. Their rights are protected by ERISA, including the right to plan information, fee disclosures, and statement of benefits.

### Recordkeeper

- **Core responsibilities:** Maintains individual participant account records; processes contributions, distributions, loans, and investment transactions; generates participant statements; produces compliance data; interfaces with all other parties
- **Accountable to:** Plan sponsor (contractual), DOL and IRS (regulatory), participants (disclosure obligations)
- **Data and workflows owned:** Participant account balances by source/money type, transaction history, investment positions, vesting records, compliance testing data, notice delivery records
- **Platform interaction:** The recordkeeper IS the platform; CORE is the recordkeeping system
- **Key distinctions:** The recordkeeper maintains the books and records of the plan at the individual account level. The recordkeeper does not hold plan assets (that is the custodian/trustee's role). In bundled models, the recordkeeper and custodian may be affiliated entities.

### Third Party Administrator (TPA)

- **Core responsibilities:** Performs plan administration tasks on behalf of the plan sponsor; conducts compliance testing; prepares Form 5500; manages plan document; handles distribution and loan processing; advises on plan design
- **Accountable to:** Plan sponsor (contractual); may serve as ERISA Section 3(16) plan administrator if explicitly appointed
- **Data and workflows owned:** Compliance test data, census data, plan document versions, government reporting files, correction workflows
- **Platform interaction:** TPA portal access to participant data, plan configuration, compliance testing outputs, and document generation; may initiate certain plan-level transactions
- **Key distinctions:** The TPA is a service provider, not automatically a fiduciary. If appointed as Section 3(16) administrator, they assume fiduciary responsibility for plan administration functions. TPA relationship is most prominent in unbundled service models.

### Financial Advisor / Broker

- **Core responsibilities:** Advises plan sponsor on plan design, investment menu, and service providers; may advise participants on investment elections; earns compensation disclosed under ERISA Section 408(b)(2)
- **Accountable to:** Plan sponsor (fiduciary or non-fiduciary depending on appointment); DOL; SEC or FINRA depending on registration
- **Data and workflows owned:** Investment recommendation data, fee disclosure documentation, plan benchmarking reports
- **Platform interaction:** Advisor portal access to plan-level data, investment performance reporting, fee analytics; may not have direct access to individual participant PII without plan sponsor authorization

**3(21) vs. 3(38) Investment Fiduciary Distinction:**

| Dimension | ERISA Section 3(21) | ERISA Section 3(38) |
|---|---|---|
| Role title | Investment Advisor (co-fiduciary) | Investment Manager (full discretion) |
| Authority | Provides investment recommendations; plan sponsor retains final decision | Has full discretionary authority to select, manage, and replace investments |
| Fiduciary responsibility | Shared with plan sponsor | Shifts to the 3(38) for investment decisions |
| Platform automation implication | Platform must present recommendations for plan sponsor approval; cannot auto-implement | Platform may implement investment changes directed by the 3(38) without additional plan sponsor approval |
| Key agent flag | Any feature that auto-implements investment changes must verify whether a 3(38) is appointed; if only a 3(21) is in place, an approval workflow is required | [COMPLIANCE-SENSITIVE] |

### Custodian / Trustee

- **Core responsibilities:** Holds legal title to plan assets; executes investment transactions; maintains asset-level records; ensures assets are used for exclusive benefit of participants
- **Accountable to:** Plan document, ERISA Title I (for ERISA plans), plan sponsor
- **Data and workflows owned:** Asset positions, trade confirmations, NAV data, cash management records
- **Platform interaction:** Trust accounting system receives trade instructions from recordkeeper; sends NAV/pricing feeds and confirmed trade data back; reconciliation occurs between recordkeeping system and trust system

**Directed Trustee vs. Discretionary Trustee:**

| Type | Description | Platform Implication |
|---|---|---|
| **Directed Trustee** | Acts only on instructions from a named fiduciary; does not exercise discretion over investments | Platform sends explicit trade instructions; trustee confirms execution |
| **Discretionary Trustee** | Has independent authority over investment decisions; rare in DC plans | Platform may receive investment direction from trustee rather than plan sponsor |

In most DC plans, the trustee is a directed trustee. The recordkeeper instructs trades based on participant or plan-level direction.

### Payroll Provider

- **Core responsibilities:** Calculates and processes employee payroll; produces contribution data for retirement plan remittance; provides census data for eligibility and compliance testing
- **Accountable to:** Employer (contractual); IRS for payroll tax compliance
- **Data and workflows owned:** Compensation data, hours data, employee demographics, payroll cycle outputs, contribution amounts by source
- **Platform interaction:** Sends contribution files and census data to recordkeeper via file-based or API-based integration

**File-Based vs. API-Based Integration Patterns:**

| Pattern | Description | Common Formats | Timing |
|---|---|---|---|
| **File-based** | Payroll system produces a structured file delivered via SFTP or secure transfer | Fixed-width, delimited (CSV/tab), SPARK-format | Batch; per payroll cycle |
| **API-based** | Real-time or near-real-time data exchange via RESTful APIs | JSON; SPARK Institute API Integration Guidelines (June 2025) define standard payloads | Event-driven or scheduled |

The **SPARK Institute API Integration Guidelines (June 2025)** define standard APIs for the retirement industry including Census API, Contribution API, Loan API, Distribution API, and Participant Balance API. These standards reduce custom integration work and improve data accuracy across providers.

360° integration refers to bidirectional payroll integration: payroll sends contribution and census data to the recordkeeper; the recordkeeper sends loan repayment schedules and distribution data back to payroll to ensure accurate withholding and payroll adjustments.

### Investment Managers / DCIOs

- **Core responsibilities:** Manage investment funds offered on the plan's investment menu; provide fund data (NAV, performance, fees); comply with SEC regulatory obligations
- **Accountable to:** SEC, shareholders/unitholders, plan fiduciaries who selected them
- **Data and workflows owned:** NAV pricing, fund performance data, revenue sharing rates, fund prospectuses, Rule 22c-2 shareholder data
- **Platform interaction:** Investment data feeds (NAV pricing, fund characteristics) flow into the recordkeeping system; trade orders flow out; revenue sharing and fee data flows to fee disclosure systems

### Regulators: IRS and DOL

| Regulator | Primary Jurisdiction | Key Tools |
|---|---|---|
| **IRS** | Tax qualification of retirement plans; contribution limits; distribution taxation; correction programs (EPCRS) | Revenue rulings, notices, private letter rulings, audits, EPCRS |
| **DOL / EBSA** | ERISA fiduciary standards; participant rights; fee disclosure; cybersecurity | Prohibited transaction exemptions, advisory opinions, DOL audits, civil enforcement |

### Role Interaction Summary

A typical plan administration workflow connects roles as follows:

**Plan Sponsor** adopts the plan and selects service providers. **Payroll Provider** transmits contribution and census data to the **Recordkeeper** each payroll cycle. The **Recordkeeper** allocates contributions to participant accounts, executes investment trades via the **Custodian/Trustee**, and maintains the books of record. The **TPA** uses recordkeeping data to perform compliance testing, prepare government filings, and manage the plan document. The **Financial Advisor** advises the plan sponsor on investment menu and plan design; if appointed as a 3(38), directs investment changes. **Participants** interact with the recordkeeper's participant portal to manage their accounts. **Investment Managers** provide fund data and execute trades. The **IRS** and **DOL** set the regulatory framework within which all parties operate and have audit/enforcement authority.

**Sources:**
- ERISA Sections 3(16), 3(21), 3(38) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa/laws-and-regulations/laws/erisa | Retrieved 2026-03-06
- SPARK Institute API Integration Guidelines, June 2025 | SPARK Institute | https://www.sparkinstitute.org | Retrieved 2026-03-06
- FINRA Investor Education | https://www.finra.org/investors/retirement | Retrieved 2026-03-06
- Plan Sponsor Magazine | https://www.plansponsor.com | Retrieved 2026-03-06

---

## Section 3 — Fiduciary Framework

### 3.1 What a Fiduciary Is Under ERISA

Under ERISA Section 3(21), a person is a **fiduciary** to the extent they:
- Exercise discretionary authority or control over plan management or plan assets
- Render investment advice for a fee or other compensation with respect to plan assets, or have authority to do so
- Have discretionary authority or responsibility in plan administration

Fiduciary status is functional — it is determined by what a person actually does, not solely by their title. A service provider who performs only ministerial functions is not a fiduciary. A service provider who exercises discretion crosses into fiduciary status.

**Why fiduciary status matters for platform design:** A platform that automates a decision previously made by a human may inadvertently assume fiduciary status for that function. Features that automate investment changes, approve hardship requests, or calculate and distribute benefits must be designed with an explicit view to whether the platform is acting as a fiduciary or executing the instructions of one. Platform design must not expose Congruent Solutions to unintended fiduciary liability.

### 3.2 ERISA Section 3(16): Plan Administrator

- **Definition:** The person designated in the plan document as the plan administrator. If no designation is made, the plan sponsor is the plan administrator by default.
- **Responsibilities:** Day-to-day plan administration, including distributing required notices, maintaining records, filing Form 5500, and acting on participant requests.
- **Who typically holds this role:** The plan sponsor employer. In some arrangements, a TPA or outsourced provider is explicitly appointed as the Section 3(16) administrator.
- **Platform implication:** When a TPA or third party is the Section 3(16) administrator, that party's approvals and decisions must be tracked and logged by the platform. Workflows must route administrative decisions to the designated 3(16) administrator.

### 3.3 ERISA Section 3(21): Investment Advisor (Co-Fiduciary)

- **Definition:** A co-fiduciary who renders investment advice for a fee; shares fiduciary responsibility with the plan sponsor but does not have sole discretion.
- **Responsibilities:** Provide prudent investment recommendations; disclose conflicts of interest; document advice.
- **Platform implication:** The platform must present investment recommendations for plan sponsor review and approval. The platform cannot auto-implement a 3(21)'s recommendations without plan sponsor action. Any feature that bypasses this approval step creates fiduciary risk.

### 3.4 ERISA Section 3(38): Investment Manager (Full Discretion)

- **Definition:** A fiduciary with full discretionary authority to manage, acquire, and dispose of plan assets. Must be an investment advisor registered under the Investment Advisers Act, a bank, or an insurance company.
- **Responsibilities:** Makes and implements investment decisions; relieves plan sponsor of liability for those decisions.
- **Platform implication:** When a 3(38) is appointed, the platform may implement investment changes directed by the 3(38) without requiring additional plan sponsor approval. Requirements must verify whether a 3(38) is in place before designing auto-implementation workflows. [COMPLIANCE-SENSITIVE]

### 3.5 The Prudent Expert Standard

ERISA Section 404(a) requires fiduciaries to act:
- Solely in the interest of participants and beneficiaries
- For the exclusive purpose of providing plan benefits and defraying reasonable plan expenses
- With the care, skill, prudence, and diligence that a prudent expert would use under the circumstances

**Platform implications of the prudent expert standard:**
- **Audit trails:** Every fiduciary decision or action recorded on the platform must be logged with timestamp, actor identity, and action taken. Audit trails must be immutable.
- **Disclosures:** Fee and investment disclosures are fiduciary obligations. The platform must generate, deliver, and track delivery of required disclosures.
- **Approval workflows:** Workflows involving fiduciary decisions (investment changes, hardship approvals, QDRO qualification) must route to the appropriate fiduciary for review and approval before execution.

### 3.6 ERISA Section 404(c): Participant-Directed Investments

ERISA Section 404(c) provides fiduciary relief to plan sponsors and other fiduciaries when participants exercise independent control over their investment accounts. For 404(c) protection to apply, the plan must:
- Offer a broad range of investment alternatives (at minimum, three diversified options with materially different risk and return characteristics)
- Allow participants to give investment instructions at least as frequently as market volatility requires, but no less than quarterly
- Provide participants with sufficient information to make informed investment decisions
- Implement participant investment instructions without undue delay

**Platform requirements supporting 404(c) compliance:**
- Investment change functionality must be available at the required frequency
- Participants must have access to investment information (prospectuses, fund fact sheets) through the platform
- Trade execution must occur within defined processing windows
- Confirmation of executed trades must be available to participants

### 3.7 ERISA Section 107: Record Retention

ERISA Section 107 requires that all records necessary to determine the rights of any plan participant or beneficiary be retained for a minimum of six years from the date the document was filed, or in the case of items required to be certified, from the date on which such certification was due. [DATE-VERIFY — confirm current retention standards at time of requirement writing]

**Platform implications:**
- The recordkeeping system must retain transaction-level records, plan documents, notices, and compliance data for the required period
- Data archiving and retrieval capabilities must support DOL audit requests and participant benefit claims
- Deletion or modification of historical records must be controlled and logged

**Sources:**
- ERISA Sections 3(16), 3(21), 3(38), 404(a), 404(c), 107 | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa/laws-and-regulations/laws/erisa | Retrieved 2026-03-06
- DOL Field Assistance Bulletin 2003-3 (404(c)) | https://www.dol.gov/agencies/ebsa/employers-and-advisers/guidance/field-assistance-bulletins | Retrieved 2026-03-06
- ASPPA Resources on Fiduciary Standards | https://www.asppa.org | Retrieved 2026-03-06

---

## Section 4 — Plan Types and Structures

### 401(k)

- **Structure:** A qualified cash or deferred arrangement (CODA) under IRC Section 401(k), part of a profit-sharing or stock bonus plan. Employees elect to defer a portion of their compensation on a pre-tax basis (Traditional) or after-tax basis (Roth). Employers may contribute matching or non-elective (profit sharing) contributions.
- **Who uses it:** Private-sector for-profit employers of all sizes; the most prevalent DC plan type in the U.S.
- **Architectural distinction:** Requires tracking of multiple contribution sources (employee pre-tax, Roth, employer match, employer non-elective, rollover) with distinct vesting schedules per source. Requires ADP/ACP testing unless safe harbor provisions are satisfied.
- **ERISA applicability:** Subject to ERISA (private-sector employer plans). Governmental 401(k) plans are rare and operate under different rules; agents must flag [GOVERNMENT PLAN — NON-ERISA] if encountered.
- **Agents must flag:** Contribution source segregation; annual nondiscrimination testing requirements; safe harbor election status; Roth in-plan conversion capability; auto-enrollment and auto-escalation provisions.

### 403(b)

- **Structure:** A tax-sheltered annuity plan under IRC Section 403(b), available to employees of public schools, colleges, and universities, and tax-exempt organizations under IRC Section 501(c)(3). Functionally similar to a 401(k) in contribution mechanics.
- **Who uses it:** Educational institutions, hospitals, charities, religious organizations.
- **ERISA applicability:** ERISA status depends on employer arrangement, not plan type.
  - A public school district's 403(b) is a governmental plan — non-ERISA.
  - A private university's 403(b) may be ERISA-covered or non-ERISA depending on the level of employer involvement.
  - A 403(b) with minimal employer involvement meeting the DOL safe harbor for voluntary plans may be non-ERISA even for a private employer.
  - **Agents must never assume ERISA or non-ERISA status for a 403(b) based on plan type alone. Verify the arrangement.**
- **Universal Availability Rule:** Under IRC Section 403(b)(12), all employees of the employer must be permitted to make elective deferrals unless specifically excluded by statute. The exclusion classes permitted under 403(b) differ from those in 401(k) plans. Platform eligibility logic must support Universal Availability Rule compliance. [COMPLIANCE-SENSITIVE]
- **Architectural distinction:** 403(b) plans may include both annuity contracts and custodial accounts. Legacy 403(b) plans may have individual annuity contracts not held in a plan trust, creating reconciliation complexity. The 2007 final 403(b) regulations generally require a written plan document for ERISA-covered plans; universal adoption of written plans has been an ongoing industry process.
- **Agents must flag:** ERISA status; Universal Availability Rule eligibility logic; contract vs. custodial account structure; pre-2009 grandfathered contracts; whether the plan has a universal availability tracking requirement.

### 457(b) Governmental

- **Structure:** A deferred compensation plan under IRC Section 457(b) maintained by a state or local government or an agency/instrumentality thereof. Employee deferrals reduce current taxable income; assets must be held in trust for the exclusive benefit of participants (post-1999 requirement). [DATE-VERIFY]
- **Who uses it:** State and local government employers; public school districts; municipalities.
- **ERISA applicability:** **NOT subject to ERISA.** Agents must tag all 457(b) governmental plan requirements: **[GOVERNMENT PLAN — NON-ERISA]**
- **Key distinction:** Contribution limits for 457(b) governmental plans run independently and do not aggregate with 401(k) or 403(b) limits — a participant employed by both a governmental and a private employer may contribute the maximum to both a 457(b) governmental plan and a 401(k)/403(b) simultaneously. This is a plan-configurable parameter concept; specific limit amounts are sourced from current IRS limit tables.
- **Agents must flag:** Non-ERISA status throughout; no prohibited transaction rules under ERISA apply; trust requirement post-1999; distinct RMD and distribution rules.

### 457(b) Tax-Exempt and 457(f)

- **457(b) Tax-Exempt:** Maintained by non-governmental tax-exempt organizations (e.g., hospitals, nonprofits). Eligible to defer compensation up to the annual limit. Unlike governmental 457(b), assets remain general assets of the employer and are subject to claims of creditors — participants bear employer solvency risk. Subject to ERISA as a top-hat plan if limited to select management or highly compensated employees.
- **457(f):** An "ineligible" deferred compensation arrangement for tax-exempt employers that does not meet 457(b) limits. Deferred amounts are subject to a substantial risk of forfeiture; taxation is triggered when the risk of forfeiture lapses. 457(f) arrangements are generally not funded plans and require specialized recordkeeping. [NEEDS-VALIDATION — confirm current IRC 457(f) treatment and platform applicability]
- **Agents must flag:** Employer solvency risk in 457(b) tax-exempt; substantial risk of forfeiture timing in 457(f); top-hat plan ERISA exemption applicability; unfunded plan architecture.

### SIMPLE IRA

- **Structure:** Savings Incentive Match Plan for Employees under IRC Section 408(p). Employers meeting the eligible employer criteria (plan-configurable size threshold based on IRS rules) may establish a SIMPLE IRA. Each participant maintains an individual IRA. Employer must make either matching contributions up to a plan-configurable percentage of compensation or a fixed non-elective contribution.
- **Who uses it:** Small employers seeking a low-cost retirement plan with minimal administrative burden.
- **ERISA applicability:** SIMPLE IRAs maintained by private-sector employers are generally subject to ERISA unless the DOL voluntary plan safe harbor applies.
- **Architectural distinction:** No trust — contributions go directly to individual IRAs at a financial institution. Recordkeeping is simpler than a trust-based plan. The IRA custodian holds assets, not a plan trustee. Two-year rule restricts participants from rolling out SIMPLE IRA assets during the first two years of participation.
- **Agents must flag:** IRA-based architecture (not trust-based); employer eligibility threshold (plan-configurable per IRS rules); two-year transfer restriction; SIMPLE IRA vs. SIMPLE 401(k) distinction (SIMPLE 401(k) is trust-based); no loans permitted from SIMPLE IRAs.

### SEP IRA

- **Structure:** Simplified Employee Pension under IRC Section 408(k). Employer-only contributions to individual employee IRAs. No employee salary deferral permitted (except in legacy SARSEP arrangements grandfathered prior to 1997).
- **Who uses it:** Self-employed individuals, small employers seeking minimal administrative burden.
- **ERISA applicability:** Subject to ERISA if maintained by a private-sector employer, though administrative requirements are minimal. DOL safe harbor for IRAs may apply.
- **Architectural distinction:** No trust; employer contributes directly to participant IRAs. Contribution formula is uniform percentage of compensation for all eligible employees. Very limited plan document requirements.
- **Agents must flag:** No employee deferrals in current SEP IRA; SARSEP grandfathering for pre-1997 plans; IRA-based architecture; no loans.

### Safe Harbor 401(k)

- **Structure:** A 401(k) plan that satisfies ADP and/or ACP testing requirements by making specified employer contributions and providing required notices to participants. In exchange, the plan is deemed to pass ADP and ACP tests.

**Traditional Safe Harbor vs. QACA:**

| Dimension | Traditional Safe Harbor | QACA (Qualified Automatic Contribution Arrangement) |
|---|---|---|
| Auto-enrollment required | No | Yes — automatic enrollment at a minimum default deferral rate |
| Default deferral rate | N/A | Plan-configurable minimum per IRS requirements (no specific percentage here) |
| Required employer contribution | Matching or non-elective; formulas are plan-configurable per IRS safe harbor requirements | Matching or non-elective; formulas are plan-configurable per QACA requirements |
| Vesting | Immediate for employer safe harbor contributions | Up to 2-year cliff vesting permitted for employer safe harbor contributions |
| ADP/ACP relief | Eliminates need for ADP test; if matching contributions meet requirements, also eliminates ACP test | Same |

- **Agents must flag:** Safe harbor notice requirement (annual, before plan year); mid-year amendment restrictions for safe harbor plans; QACA auto-enrollment and auto-escalation requirements; vesting schedule distinction between traditional and QACA safe harbor.

### Pooled Employer Plans (PEPs) and Multiple Employer Plans (MEPs)

- **MEP (Multiple Employer Plan):** Two or more unrelated employers participate in a single plan. The plan has one Form 5500 filing. Historically, MEPs with unrelated employers faced the "one bad apple" rule — one employer's violation could disqualify the entire plan. SECURE 2.0 and prior legislation modified the one bad apple rule for certain MEPs.
- **PEP (Pooled Employer Plan):** Created by SECURE Act of 2019. A type of MEP operated by a **Pooled Plan Provider (PPP)** registered with the DOL. Each employer adopts the PEP via a participation agreement. The PPP is the named plan administrator and a named fiduciary. PEPs dramatically reduce plan sponsor administrative burden and fiduciary liability.
- **Architectural distinction:** Both MEP and PEP structures require multi-employer data management: each employer has its own contribution rules, payroll data, and potentially its own plan design parameters within the pooled structure. The recordkeeping platform must support employer-level segmentation within a single plan.
- **Agents must flag:** PPP registration requirement for PEPs; employer-level plan design parameterization; multi-EIN data structure; one bad apple rule applicability for MEPs; Form 5500 filing at plan level (not employer level) for MEPs/PEPs.

### Starter 401(k) (SECURE 2.0, Effective 2025) [DATE-VERIFY]

- **Structure:** A new plan type created by SECURE 2.0 for employers that do not sponsor any other retirement plan. Simplified 401(k) with mandatory auto-enrollment, no employer contribution requirement, and reduced nondiscrimination testing burden. Participants may only make elective deferrals up to a plan-configurable limit per IRS rules.
- **Who uses it:** Small employers with no existing plan — designed as a low-friction entry point.
- **Agents must flag:** [DATE-VERIFY — confirm effective date and feature requirements before writing scope]; verify which compliance tests are waived; auto-enrollment default parameters per IRS guidance.

**Sources:**
- IRC Sections 401(k), 403(b), 408, 457 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL 403(b) Regulations (2007) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SECURE Act of 2019 (P.L. 116-94); SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov | Retrieved 2026-03-06
- ASPPA Plan Types Reference | https://www.asppa.org | Retrieved 2026-03-06

---

## Section 5 — Core Data Entities

### Plan

- **Represents:** The legal retirement plan entity as established by the plan document. The master record governing all rules and participants.
- **Key attributes (conceptual):** Plan name; plan type; plan year start/end; employer identification; effective date; plan document version; safe harbor election status; auto-enrollment status; ERISA applicability flag; vesting schedule(s); eligibility rules; entry dates; contribution formula parameters; investment menu; TPA and advisor relationships
- **Relationships:** Parent to all Participant Records, Contribution Records, and Transactions within the plan. References the Plan Design / Adoption Agreement for configuration parameters.
- **System events:** Created at plan setup/onboarding; updated by plan amendments; closed at plan termination.

### Plan Design / Adoption Agreement

- **Represents:** The configuration layer between regulatory domain rules and the operational participant record. Captures the plan sponsor's elections for all plan-configurable parameters.
- **Key attributes (conceptual):** Eligibility parameters (age, service, entry dates); contribution formulas (employer match, non-elective); vesting schedule elections; distribution options; loan policy; hardship withdrawal policy; auto-enrollment parameters; auto-escalation parameters; safe harbor election; QDIA designation; force-out thresholds; compensation definition election
- **Relationships:** Directly referenced by all eligibility, contribution, vesting, and distribution processing logic. One Plan has one active Adoption Agreement at a time; prior versions are retained for audit.
- **System events:** Created at plan setup; updated by plan amendments (version-controlled); effective date tracking is critical for retroactive recalculation scenarios.

### Employer / Plan Sponsor Record

- **Represents:** The legal entity that sponsors the plan. In controlled group and MEP/PEP contexts, multiple employer entities may be associated with a single plan.
- **Key attributes (conceptual):** Employer name; EIN; plan sponsor contact; payroll provider relationship; controlled group membership; plan sponsor portal access credentials
- **Relationships:** Associated with one or more Plans; parent to Participant Records (by employment relationship).
- **System events:** Created at plan setup; updated for mergers, acquisitions, controlled group changes; inactivated at plan termination.

### Participant Record

- **Represents:** An individual employee or former employee who is a participant or eligible to become a participant in the plan.
- **Key attributes (conceptual):** Name; SSN (PII — restricted access); date of birth; date of hire; date of termination (if applicable); employment status; eligibility status; enrollment status; deferral rate; investment elections; vesting percentage by source; beneficiary designations; contact information; LTPT tracking flag
- **Relationships:** Belongs to an Employer / Plan Sponsor; has one or more Account / Sub-accounts; has one or more Contribution Records; may have Loan records; may have Distribution records; has Vesting Records.
- **System events:** Created at hire or eligibility event; updated by payroll, enrollment, life events, termination, rehire; inactivated at full distribution or death with completed beneficiary distribution.

### Beneficiary

- **Represents:** The person(s) or entity designated to receive a participant's account balance upon death.
- **Key attributes (conceptual):** Beneficiary name; relationship to participant; designation type (primary vs. contingent); percentage allocation; date of designation; spousal consent status (if applicable); trust or estate designation flag
- **Relationships:** Associated with a Participant Record; may trigger Death and Beneficiary Processing workflows.
- **System events:** Created or updated by participant election; may be updated by QDRO; triggered for distribution processing upon participant death.

### Contribution Record

- **Represents:** A single contribution transaction posting to a participant's account, attributed to a specific payroll cycle and contribution source.
- **Key attributes (conceptual):** Participant reference; plan reference; payroll period; contribution source (money type); dollar amount; effective date; posting date; payroll file reference; status (pending, posted, corrected)
- **Relationships:** Belongs to a Participant Record; classified by Source / Money Type; creates a Transaction record upon posting; aggregates to compliance testing data.
- **System events:** Created upon receipt of payroll file; updated during validation; posted upon successful processing; corrected via corrective contribution records.

### Source / Money Type

- **Represents:** The classification of a contribution by its origin and regulatory treatment. Drives vesting, distribution eligibility, and tax withholding rules.
- **Common sources:**
  - Employee pre-tax (elective deferral)
  - Designated Roth (employee after-tax, in-plan Roth)
  - Employer match (subject to vesting schedule)
  - Employer non-elective / profit sharing (subject to vesting schedule)
  - Rollover (from prior plan or IRA; immediately distributable)
  - After-tax (non-Roth; non-elective employee after-tax)
  - Loan repayment (not a contribution; credits the loan sub-account)
  - QNEC / QMAC (corrective contributions; specific vesting rules)
  - PLESA contributions (if plan supports PLESA accounts) [DATE-VERIFY]
- **Relationships:** Each Contribution Record, Account / Sub-account, and Transaction is tagged with a Source. Vesting Records reference source to determine applicable vesting schedule.
- **System events:** Defined at plan setup; new sources may be added by plan amendment.

### Investment Fund

- **Represents:** An investment option available to participants on the plan's investment menu.
- **Key attributes (conceptual):** Fund name; ticker or CUSIP; fund type (mutual fund, collective investment trust, stable value, target-date fund series); expense ratio data; revenue sharing rate; trading restrictions (blackout periods, redemption fees); QDIA eligibility flag
- **Relationships:** Referenced by participant investment elections; referenced by Account / Sub-account positions; referenced by trade instructions to Custodian/Trustee.
- **System events:** Added/removed by plan sponsor or 3(38) investment manager; prices updated via daily NAV feed; blackout restrictions applied during mapping changes.

### Account / Sub-account

- **Represents:** The record of a participant's holdings in a specific investment fund within a specific contribution source.
- **Key attributes (conceptual):** Participant reference; plan reference; source/money type; investment fund reference; unit balance; dollar value; vesting percentage; last valued date
- **Relationships:** Belongs to a Participant Record; tagged with a Source / Money Type; references an Investment Fund; aggregates to total participant account balance.
- **System events:** Created upon first contribution posting; updated by contributions, distributions, investment trades, and daily valuation; closed at zero balance.

### Transaction

- **Represents:** Any financial event affecting a participant's account balance.
- **Key attributes (conceptual):** Transaction type (contribution, distribution, loan origination, loan repayment, investment transfer, fee, correction, forfeiture); transaction date; effective date; participant reference; source/money type; investment fund; dollar amount; unit quantity; status; reference to originating event
- **Relationships:** Links to Participant Record, Contribution Record (for contribution transactions), Distribution record (for distribution transactions), Loan record (for loan transactions).
- **System events:** Created by contribution posting, distribution processing, loan processing, investment rebalancing, fee processing, correction workflows.

### Loan

- **Represents:** A participant loan originated from the participant's vested account balance.
- **Key attributes (conceptual):** Loan number; participant reference; origination date; loan amount; interest rate (plan-configurable; must meet IRS reasonable rate standard); repayment schedule; maturity date; outstanding balance; repayment history; loan status (active, defaulted, deemed distributed, offset); outstanding principal
- **Relationships:** Belongs to a Participant Record; reduces vested account balance at origination; repayments credited back to participant account by source.
- **System events:** Created at loan origination; updated by repayment posting; status changed to defaulted upon missed repayments; closed at payoff or deemed distribution.

### Distribution

- **Represents:** A payment from the plan to a participant, beneficiary, or alternate payee.
- **Key attributes (conceptual):** Distribution type (hardship, RMD, termination, death, QDRO, in-service, force-out, rollover); participant or payee reference; distribution date; gross amount; tax withholding (federal mandatory and state plan-configurable); net amount; payee information; rollover election (direct vs. indirect); 1099-R data; status
- **Relationships:** Belongs to a Participant Record (or alternate payee); triggers tax withholding logic; generates 1099-R record; affects vesting finalization.
- **System events:** Initiated by participant request, plan event (RMD trigger, force-out), or court order (QDRO); approved per plan and regulatory requirements; processed and settled; 1099-R generated at tax year end.

### Vesting Record

- **Represents:** The record of a participant's vested percentage in each employer contribution source.
- **Key attributes (conceptual):** Participant reference; source/money type; vesting schedule type (immediate, cliff, graded); years of vesting service; current vested percentage; vesting service history
- **Relationships:** Belongs to a Participant Record; references the vesting schedule defined in Plan Design; affects distributable balance calculations.
- **System events:** Created upon first employer contribution; updated annually or upon triggering events (termination, rehire, amendment); finalized at termination of employment.

### Compliance Testing Data

- **Represents:** Aggregated and participant-level data collected and used for annual compliance testing.
- **Key attributes (conceptual):** Plan year; test type (ADP, ACP, 415, 416, 410(b), 401(a)(4)); participant compensation data by definition type; contribution amounts by source; HCE/NHCE classification; eligible employee list; test result; corrective action taken
- **Relationships:** Aggregates from Participant Records, Contribution Records, and Plan Design data.
- **System events:** Data collected throughout plan year; formal test runs at year-end or upon triggering events; corrections posted as Contribution Records or Distributions.

### Notice / Document Record

- **Represents:** A required notice or plan document generated and delivered to a participant, plan sponsor, or regulatory body.
- **Key attributes (conceptual):** Notice type (SPD, SAR, safe harbor notice, QDIA notice, blackout notice, 402(f) special tax notice, fee disclosure, etc.); recipient; delivery method; delivery date; delivery confirmation; document version; effective date
- **Relationships:** Associated with a Participant Record (for participant-level notices) or Plan (for plan-level documents); tracked for compliance with ERISA disclosure obligations.
- **System events:** Generated by triggering events (enrollment, plan year start, distribution request, blackout period, etc.); delivered via electronic or paper delivery channel; delivery confirmation logged.

### Forfeiture Account

- **Represents:** The plan-level account holding unvested employer contributions forfeited by terminated participants.
- **Key attributes (conceptual):** Plan reference; forfeiture balance; pending forfeitures (not yet processed); plan year forfeitures by source; permitted uses per plan document (reduce employer contributions, pay plan expenses, fund QNEC/QMAC)
- **Relationships:** Associated with a Plan; sources from terminated participant Vesting Records; affects employer contribution calculations and compliance testing.
- **System events:** Credited upon termination and vesting finalization; debited when applied per plan document rules; timing of forfeiture processing is governed by plan document and IRS guidance. [DATE-VERIFY — confirm forfeiture usage timing rules]

**Sources:**
- IRS Retirement Plans — Plan Administration | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Plan Administration Resources | https://www.asppa.org | Retrieved 2026-03-06

---

## Section 6 — Participant Lifecycle

### 6.1 Eligibility Determination

**What triggers entry:** An employee is hired or an existing employee reaches an age or service milestone defined in the plan's adoption agreement.

**Business rules (conceptual):**
- Age requirement: The plan may require a participant to reach a minimum age (plan-configurable; subject to ERISA maximums) before becoming eligible.
- Service requirement: The plan may require a period of service, measured by hours of service in a plan year (elapsed time method or hours counting method), before eligibility is met.
- Entry dates: After satisfying eligibility requirements, a participant enters the plan on the next entry date (e.g., first of the month, first of the quarter, semi-annually, or immediately upon eligibility).
- Exclusion classes: The plan may exclude certain employee classes (e.g., part-time employees below a plan-configured hours threshold, union employees covered by a collective bargaining agreement, non-resident aliens with no U.S. source income). Exclusions are plan-configurable but bounded by ERISA and IRC nondiscrimination rules.

**LTPT Employee Tracking (SECURE 2.0 — 2-Year Rule):** [DATE-VERIFY]
SECURE 2.0 modified the long-term part-time employee rules. Employees who complete the plan-configurable qualifying hours threshold for two consecutive 12-month periods must be permitted to make elective deferrals. The platform must:
- Track hours of service across consecutive measurement periods for LTPT employees
- Generate eligibility alerts when the two-year threshold is met
- Manage entry date processing for LTPT-eligible employees
- Maintain LTPT tracking even for employees otherwise excluded by a part-time exclusion class

[COMPLIANCE-SENSITIVE]

**System workflows:**
- Continuous monitoring of service and age milestones based on payroll/census data
- Automated eligibility forecasting and alerts to plan sponsor or TPA
- Enrollment invitation generation upon eligibility

**Compliance obligations triggered:** Enrollment materials must be provided to newly eligible employees within the timeframes required by ERISA.

**Sources:**
- IRC Section 410(a) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022, Section 125 (LTPT) | https://www.congress.gov | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06

---

### 6.2 Enrollment

**What triggers entry:** An employee becomes eligible to participate in the plan.

**Auto-enrollment vs. Affirmative Enrollment:**
- **Affirmative enrollment:** The participant takes an active step to enroll and elect a deferral rate. No contribution occurs unless the participant acts.
- **Auto-enrollment:** The plan automatically enrolls eligible participants at a plan-configured default deferral rate unless the participant affirmatively opts out. Auto-enrollment is required for new 401(k) and 403(b) plans under SECURE 2.0 (effective date plan-configurable per IRS guidance). [DATE-VERIFY]

**EACA and QACA Structures:**
- **EACA (Eligible Automatic Contribution Arrangement):** An automatic enrollment arrangement meeting IRS requirements. Allows a 90-day withdrawal window for participants who did not affirmatively enroll. Provides safe harbor for default investment in a QDIA.
- **QACA (Qualified Automatic Contribution Arrangement):** An EACA that also satisfies ADP/ACP safe harbor requirements. Requires plan-configurable minimum default deferral rates and auto-escalation provisions per IRS rules. Permits up to 2-year cliff vesting on safe harbor employer contributions.

**QDIA Default Logic:** If a participant does not make an investment election, contributions are defaulted to the plan's Qualified Default Investment Alternative. The platform must route default contributions to the QDIA, generate the required QDIA notice, and maintain the ability to transfer out of the QDIA upon participant election.

**Beneficiary designation:** The enrollment workflow must capture beneficiary designations. If a participant is married, spousal beneficiary rules under ERISA may apply. Plans may require spousal consent for designation of a non-spouse beneficiary. [COMPLIANCE-SENSITIVE]

**Deferral rate setting:** Participants elect a deferral rate as a percentage of compensation or flat dollar amount (plan-configurable). The platform must enforce plan-configured and IRS-limit constraints on deferral amounts.

**System workflows:** Enrollment portal or paper process; default deferral and QDIA processing for auto-enrolled participants; opt-out processing; beneficiary designation capture; payroll integration to activate deferral deductions.

**Compliance obligations triggered:** QDIA notice (if applicable); safe harbor notice (if safe harbor plan); automatic enrollment notice.

---

### 6.3 Active Contribution Period

**Payroll cycle processing:** Each payroll cycle, the payroll provider transmits contribution data to the recordkeeper. The platform validates the data, allocates contributions to participant accounts by source, and instructs the custodian to receive and invest the funds.

**Contribution source tracking:** Every contribution must be attributed to its correct source/money type. Source determines vesting schedule, distribution eligibility, and tax treatment.

**Limit monitoring:**
- Elective deferral limits, annual additions limits, and catch-up contribution limits are plan-configurable parameters sourced from current IRS limit tables. Amounts must never be hardcoded.
- The platform must monitor year-to-date deferrals and annual additions against applicable limits, generate alerts when a participant approaches a limit, and stop contributions when a limit is reached.
- [COMPLIANCE-SENSITIVE]

**Employer match calculation concepts:**
- Match formulas are plan-configurable (e.g., a percentage of employee deferrals up to a percentage of compensation). The platform evaluates the match formula each payroll cycle or on a plan-configured true-up basis.
- Match calculations may be per-payroll or annualized. Annualized match requires a year-end true-up process.

**Auto-escalation triggers:**
- For plans with auto-escalation, the platform must automatically increase participant deferral rates on a plan-configured schedule (e.g., annually on the plan anniversary or on a specified date) until the plan-configured maximum deferral rate is reached.
- Participants must receive notice of auto-escalation and have the opportunity to opt out.

---

### 6.4 Investment Management

**Fund election changes:** Participants may change their investment elections prospectively (future contributions) and transfer existing balances between available funds, subject to plan and fund trading restrictions.

**Rebalancing:**
- **Periodic rebalancing:** Participant's account is rebalanced to target allocations on a plan-configured schedule.
- **Threshold-based rebalancing:** Rebalancing is triggered when allocation drift exceeds a plan-configured threshold.
- The platform must support both approaches and ensure rebalancing trades are executed within the plan's trade execution window.

**Blackout period restrictions and notice requirements:**
- A blackout period is a period during which participant investment direction rights are temporarily suspended (e.g., during a plan conversion, fund mapping change, or trust/recordkeeper transition).
- ERISA Section 101(i) requires that participants receive at least 30 days advance notice of a blackout period. [DATE-VERIFY — confirm current notice requirement]
- The platform must restrict participant investment transactions during blackout periods, generate required blackout notices, and log the blackout period dates.
- [COMPLIANCE-SENSITIVE]

**QDIA re-enrollment events:** The plan sponsor may conduct a QDIA re-enrollment sweep, moving all participants who have not made affirmative investment elections into the QDIA. Requires notice and an opt-out window.

---

### 6.5 Loan Administration

**Loan origination and maximum calculation concepts:**
- Participants may borrow from their vested account balance subject to plan policy and IRC Section 72(p) limits.
- The maximum loan amount is a plan-configurable parameter calculated as the lesser of a percentage of vested account balance or a dollar cap, per IRS rules. The platform must calculate the maximum available loan amount dynamically based on current vested balance and outstanding loan balances.
- Plans may limit the number of outstanding loans (plan-configurable).

**Repayment schedule and tracking:**
- Loan repayments must be made in substantially level installments at least quarterly over a plan-configured repayment period (generally not exceeding five years; principal residence exception allows longer term).
- Repayments are made via payroll deduction or direct payment. The platform must track each repayment against the amortization schedule and apply repayments to the correct loan and sub-account.

**Deemed distribution trigger logic:**
- If a participant misses repayments and does not cure within the plan's cure period (through the end of the calendar quarter following the quarter in which the missed payment occurred, per IRS rules), the outstanding loan balance is treated as a **deemed distribution** — a taxable event without an actual cash payment.
- The platform must monitor repayment schedules, identify delinquent loans, apply the cure period logic, and trigger deemed distribution processing when the cure period expires.
- [COMPLIANCE-SENSITIVE]

**Loan offset on termination:**
- When a participant terminates employment with an outstanding loan balance, if the loan is not repaid, the outstanding balance is treated as a plan loan offset distribution (a taxable distribution).
- SECURE 2.0 extended the rollover deadline for qualified plan loan offset amounts. [DATE-VERIFY]
- The platform must calculate the loan offset amount, process the offset as a distribution, generate required tax reporting, and notify the participant of rollover options.

---

### 6.6 Hardship and In-Service Withdrawals

**Safe harbor hardship criteria (conceptual):**
Under IRS safe harbor rules, a hardship distribution is permissible for an immediate and heavy financial need that cannot be met from other reasonably available resources. Qualifying hardship reasons include medical expenses, purchase of principal residence, post-secondary education expenses, prevention of eviction or foreclosure, funeral expenses, casualty loss, and SECURE 2.0-added categories (domestic abuse, emergency expense). The plan document must specify which hardship reasons are permitted.

**Self-certification workflow (SECURE 2.0):** [DATE-VERIFY]
SECURE 2.0 simplified hardship verification by allowing plans to rely on participant self-certification for the existence of a qualifying hardship and the unavailability of other resources. The platform must support a self-certification workflow with an attestation requirement and document retention.

**Emergency expense distribution (SECURE 2.0):** [DATE-VERIFY]
Plans may permit a distribution for personal or family emergency expenses up to a plan-configurable limit per IRS rules, without the traditional hardship criteria. Participants may repay the distribution within three years. One distribution permitted per year unless repaid. [COMPLIANCE-SENSITIVE]

**Domestic abuse distribution (SECURE 2.0):** [DATE-VERIFY]
Plans may permit distributions to victims of domestic abuse up to a plan-configurable limit per IRS rules. Participant self-certification permitted. Early distribution penalty waived. Repayment option available within three years. [COMPLIANCE-SENSITIVE]

**PLESA withdrawals (SECURE 2.0):** [DATE-VERIFY]
**Pension-Linked Emergency Savings Accounts (PLESAs)** are short-term savings accounts linked to DC plans, allowing participants to save after-tax dollars for emergency use. PLESA balances may be withdrawn at any time without penalty. Contributions and withdrawals interact with match formulas and recordkeeping in plan-configurable ways. [COMPLIANCE-SENSITIVE]

**Age-based in-service withdrawals:**
Plans may permit in-service withdrawals after a participant reaches a plan-configured age (subject to IRC minimums). Rollover options apply to eligible rollover distributions from in-service withdrawals.

---

### 6.7 Termination of Employment

**Vesting finalization:** Upon termination, the participant's vested percentage in each employer contribution source is finalized based on years of vesting service completed. The unvested balance is forfeited to the plan's forfeiture account.

**Force-out thresholds (plan-configurable):**
- For small account balances below the plan-configured mandatory distribution threshold (subject to IRS rules), the plan may distribute the balance without the participant's consent. Dollar thresholds are plan-configurable per IRS rules.
- For balances above the mandatory distribution threshold but below the plan-configured consent threshold, the plan must obtain participant consent before distributing.
- For balances above the plan-configured mandatory rollover threshold, the plan must roll over the distribution to an IRA on the participant's behalf (**auto-rollover IRA**) if the participant does not affirmatively elect otherwise.

**Deferred vested participant tracking:** Participants who terminate with a vested balance but do not take a distribution are **deferred vested participants**. The platform must continue to track their account, apply vesting, process investment activity, and maintain their record for future distribution.

**Notification workflows:** The platform must generate required notices upon termination including distribution options, rollover rights, and 402(f) Special Tax Notice.

---

### 6.8 Distribution Processing

**Tax withholding concepts:**
- **Mandatory federal withholding:** Eligible rollover distributions (ERDs) are subject to mandatory 20% federal income tax withholding unless directly rolled over to an eligible retirement plan or IRA.
- **State withholding:** State income tax withholding requirements vary by state. Withholding for state taxes is a plan-configurable parameter; defaults and mandatory withholding rules depend on participant state of residence.
- [COMPLIANCE-SENSITIVE]

**Direct vs. indirect rollover:**
- **Direct rollover:** The distribution is paid directly to an eligible retirement plan or IRA. Mandatory 20% withholding does not apply.
- **Indirect rollover:** The distribution is paid to the participant; the participant has 60 days to roll over the amount to avoid taxation. The 20% withheld must be replaced by the participant from other funds to roll over the full gross distribution.

**1099-R generation:** The plan must issue a Form 1099-R for each taxable distribution by the IRS deadline for the tax year of the distribution. The platform must generate 1099-R data with accurate distribution codes and amounts for each distribution type.

**402(f) Special Tax Notice requirement:** Before any eligible rollover distribution, the participant must receive a 402(f) Special Tax Notice explaining rollover options, tax consequences, and withholding rules. The notice must be provided within the IRS-defined timing window. The platform must track notice delivery and confirmation. [COMPLIANCE-SENSITIVE]

---

### 6.9 Required Minimum Distributions (RMD)

**Conceptual trigger:** A participant must begin taking RMDs no later than their **Required Beginning Date (RBD)**. The RBD is determined by the participant's required beginning age (a plan-configurable parameter based on IRS RMD age rules modified by SECURE 2.0) and the calendar year in which they reach that age. [DATE-VERIFY — RMD ages modified by SECURE 2.0; confirm current required beginning age rules]

**Still-working exception:** Participants who are still employed by the plan sponsor after reaching RMD age (other than 5% owners) may defer RMDs until they terminate employment, if the plan permits. The platform must track employment status and apply the still-working exception accordingly.

**Designated Roth accounts — no lifetime RMD (SECURE 2.0, effective 2024):** [DATE-VERIFY]
SECURE 2.0 eliminated lifetime RMDs for designated Roth accounts in employer plans, aligning treatment with Roth IRAs. The platform must suppress RMD calculations and distributions for Roth source balances for living participants.

**Death distributions and beneficiary RMD rules:**
- Upon a participant's death, RMD rules governing beneficiaries vary based on the type of beneficiary (eligible designated beneficiary, non-eligible designated beneficiary, non-designated beneficiary), the participant's age at death (before or after RBD), and the SECURE Act's 10-year rule.
- [COMPLIANCE-SENSITIVE — confirm applicable rules for each beneficiary scenario; recommend legal/compliance review for edge cases]

**RMD tracking and automated calculation triggers:**
- The platform must identify participants approaching or at their RBD, calculate annual RMD amounts based on applicable IRS life expectancy tables (plan-configurable per IRS rules), generate distribution requests, and track whether the RMD has been satisfied.
- If an RMD is not distributed by the required deadline, an IRS excise tax applies (percentage of undistributed RMD; plan-configurable parameter per current IRS penalty rates). SECURE 2.0 reduced this penalty. [DATE-VERIFY]

---

### 6.10 Death and Beneficiary Processing

**Beneficiary designation lookup and validation:**
Upon notification of a participant's death, the platform must retrieve and validate the beneficiary designation on file. If no valid designation exists, the plan document's default beneficiary rules apply (typically surviving spouse, then estate).

**Spousal consent requirements:**
If a married participant has designated a non-spouse primary beneficiary, the spouse must have provided written, notarized consent for the designation to be valid under ERISA. The platform must track spousal consent status and flag designations lacking required consent. [COMPLIANCE-SENSITIVE]

**QDRO — Qualified Domestic Relations Order:**
- A **QDRO** is a domestic relations order that creates or recognizes the right of an alternate payee (current or former spouse, child, or other dependent) to receive all or a portion of a participant's plan benefits.
- **Written QDRO procedures requirement:** ERISA requires every plan to establish written QDRO determination procedures. The plan's procedures must be provided to participants and alternate payees free of charge.
- Platform must support: receipt and logging of domestic relations orders; qualification determination workflow; alternate payee account creation upon qualification; distribution processing to alternate payee.
- [RECOMMEND LEGAL/COMPLIANCE REVIEW for all QDRO processing requirements]

**Beneficiary distribution options:**
Options available to beneficiaries vary by plan type, beneficiary type (eligible designated beneficiary vs. others), and the SECURE Act 10-year rule. Options may include lump sum, systematic distributions, or rollovers to an inherited IRA. The platform must present eligible options based on beneficiary classification and plan terms.

---

### 6.11 Rehire

**Break-in-service rule concepts:**
A **break in service** occurs when a former employee does not complete the minimum hours of service in a plan year. Rules governing when a break is considered permanent affect whether prior service credit is restored upon rehire.

**Prior service credit restoration:**
If a rehired employee did not have a permanent break in service, prior service credit must be restored for vesting purposes. The plan document governs restoration rules. The platform must retrieve prior service records and recalculate vesting upon rehire.

**Forfeiture restoration eligibility:**
If a rehired employee's prior unvested balance was forfeited and the employee returns before a permanent break in service (or completes the required service to restore), the plan may be required to restore the forfeiture from the forfeiture account. [DATE-VERIFY — confirm current forfeiture restoration rules]

**Re-eligibility determination:**
A rehired employee may need to satisfy eligibility requirements again, or prior service may apply to immediate re-eligibility, depending on plan terms and the break-in-service rules. The platform must evaluate re-eligibility based on current plan design and prior service history.

**Sources (Section 6):**
- IRC Sections 72(p), 401(k)(2), 402(f), 403(b), 408, 414, 415, 416 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov | Retrieved 2026-03-06
- DOL ERISA Regulations, Part 2550 | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRS RMD Final Regulations (2024) | https://www.irs.gov | [DATE-VERIFY] | Retrieved 2026-03-06

---

## Section 7 — Plan Administration Lifecycle

### 7.1 Plan Setup and Onboarding

- **Plan document and adoption agreement intake:** The plan document and adoption agreement define all plan parameters. The platform must capture and version the adoption agreement as the configuration source of truth. Every plan design parameter in the platform must trace to an adoption agreement provision.
- **Plan design parameter configuration:** All eligibility rules, contribution formulas, vesting schedules, loan policy, distribution options, investment menu, and notice delivery preferences must be configured in the platform before the plan goes live.
- **Data migration and plan conversion concepts:** When a plan transitions from a prior recordkeeper, historical participant data (account balances by source, transaction history, vesting records, service history, loan balances) must be migrated. Conversion data must be validated against prior provider records and reconciled to the trust before going live.
- **Trust setup and custodian connection:** The new custodian relationship must be established, trust account numbers assigned, and the platform integrated with the trust accounting system before contributions can be funded.
- **Initial participant data load and validation:** Census data from the employer is loaded and validated (name, SSN, date of birth, date of hire, compensation, hours, employment status). Validation failures must be resolved before enrollment begins.
- **Payroll integration setup:** Payroll file formats, transmission methods, and field mappings must be configured and tested before the first payroll cycle.

### 7.2 Payroll Contribution Processing

- **Payroll file receipt:** The platform receives contribution data via SFTP file transfer or API call per the configured integration method each payroll cycle.
- **Validation rules applied before posting:** Before contributions are posted to participant accounts, the platform applies validation rules: participant eligibility check, contribution source validity, limit monitoring, employee existence check, deferral rate consistency check. Validation failures are routed to an exception queue.
- **Contribution allocation to participant accounts:** Validated contributions are allocated to participant accounts by source/money type and invested per the participant's current investment election.
- **Funding and remittance to trustee:** Employer remits plan assets to the trust within the deposit deadline. [DATE-VERIFY — deposit timeliness rules; specific timeframes are regulatory]
- **Reconciliation:** The contribution amounts in the recordkeeping system must reconcile to the amounts deposited to the trust account. Discrepancies must be identified and resolved before the next payroll cycle.
- **Exception handling and correction workflows:** Contribution errors are corrected via adjusting entries. The platform must provide a correction workflow that creates offsetting transactions with full audit trail.
- **Deposit timeliness obligations:** Employer contributions must be deposited to the trust as soon as reasonably segregable from employer assets, subject to regulatory safe harbor timing rules. [DATE-VERIFY — confirm current DOL deposit timing rules; specific timeframes are regulatory]
- **Late deposit correction process (VFCP):** If contributions are deposited late, the plan may self-correct under the DOL's **Voluntary Fiduciary Correction Program (VFCP)**. VFCP requires calculation of lost earnings on the late deposit. The platform must support VFCP correction workflows including lost earnings calculation. [COMPLIANCE-SENSITIVE]

### 7.3 Compliance Testing Cycle

**What triggers testing:** Annual nondiscrimination testing occurs at plan year end. Some tests (415, elective deferral limits) are monitored throughout the year. Testing may also be triggered by plan amendments or mid-year changes.

**Test types and what each measures:**

| Test | What It Measures | Who It Applies To |
|---|---|---|
| **ADP Test** (Actual Deferral Percentage) | Whether HCE elective deferral percentages are proportionate to NHCE deferral percentages | 401(k) plans not using safe harbor |
| **ACP Test** (Actual Contribution Percentage) | Whether HCE matching and after-tax contributions are proportionate to NHCE contributions | 401(k) plans with matching/after-tax; not using safe harbor |
| **415 Annual Additions Test** | Whether total annual additions to a participant's account exceed the IRC 415 limit | All qualified plans; limit is plan-configurable per IRS |
| **416 / Top Heavy Test** | Whether the plan is top-heavy (key employees hold more than a threshold percentage of plan assets); triggers minimum contribution requirements | All qualified plans |
| **410(b) Coverage Test** | Whether the plan covers a sufficient percentage of non-highly compensated employees | All qualified plans |
| **401(a)(4) General Nondiscrimination** | Whether contributions or benefits do not discriminate in favor of HCEs | All qualified plans |

**Corrective action options:**
- **QNEC (Qualified Non-Elective Contribution):** Employer makes a non-elective contribution to NHCEs to correct a failed ADP or ACP test.
- **QMAC (Qualified Matching Contribution):** Employer makes a matching contribution to NHCEs for correction purposes.
- **Excess refunds:** Excess contributions of HCEs are distributed back to correct ADP/ACP failures.
- **Plan restructuring:** The plan may be restructured into component plans that each satisfy testing independently.

**Safe harbor plans:** A safe harbor 401(k) (Traditional or QACA) eliminates the need for ADP testing and, if the employer matching contributions meet safe harbor requirements, ACP testing as well. Top-heavy testing may be simplified for safe harbor plans.

**Controlled group aggregation requirements:** All members of a controlled group or affiliated service group must be aggregated for compliance testing purposes. The platform must support multi-EIN controlled group data management and aggregated testing.

### 7.4 Year-End Processing

- **True-up contribution:** If the employer match formula is calculated on an annual basis but funded per payroll, a year-end true-up may be required to ensure each participant receives the correct total match amount. The platform must calculate the true-up amount and process it as a contribution.
- **Forfeiture processing timing:** Forfeitures must be used within the plan year they arise or the following plan year (plan-configurable per plan document and IRS guidance). [DATE-VERIFY] Permitted uses include reducing employer contributions, paying plan expenses, or funding QNEC/QMAC.
- **5500 data preparation:** The recordkeeper prepares plan-level financial and participant data required for Form 5500 filing by the TPA or plan sponsor.
- **SAR generation:** The Summary Annual Report summarizes plan financial information from the 5500 and must be distributed to participants annually.
- **Participant statement generation:** Annual (or more frequent) participant statements must be generated and delivered showing account balances, contributions, investment activity, and fees.

### 7.5 Plan Amendment Workflow

- **Discretionary vs. required amendments:** Plan sponsors may amend a plan at their discretion to change plan design. Required amendments are mandated by law (e.g., SECURE 2.0 provisions becoming effective).
- **Retroactive amendment rules:** Certain plan amendments may be made retroactively to a prior plan year if adopted by the plan's amendment deadline. Retroactive amendments may require recalculation of contributions, vesting, or benefits.
- **SECURE 2.0 amendment deadline concepts:** [DATE-VERIFY] SECURE 2.0 provided extended deadlines for plan sponsors to formally adopt plan amendments reflecting provisions they operationally implemented. Confirm current amendment deadlines for each SECURE 2.0 provision before writing requirements.
- **Platform implications of effective date logic vs. retroactive recalculation:** When an amendment has a retroactive effective date, the platform must recalculate and correct all affected transactions from the retroactive date forward. This is a complex, high-risk workflow requiring complete audit trail and reconciliation.

### 7.6 Plan Termination

- **Notice and distribution requirements:** The plan sponsor must notify participants of plan termination and their distribution options. After plan termination, all participants must become 100% vested.
- **Vesting acceleration:** Upon plan termination, all participant accounts must be fully vested regardless of the participant's years of service.
- **Final asset distribution workflow:** All plan assets must be distributed to participants (or rolled over) upon termination. Termination distributions are eligible rollover distributions.
- **5500 final filing:** A final Form 5500 marked as a final filing must be submitted for the plan's last plan year.

**Sources (Section 7):**
- IRC Section 415 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL Voluntary Fiduciary Correction Program | https://www.dol.gov/agencies/ebsa/employers-and-advisers/correction-programs/vfcp | Retrieved 2026-03-06
- IRS Employee Plans Compliance Resolution System (EPCRS) | https://www.irs.gov/retirement-plans/correcting-plan-errors | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov | Retrieved 2026-03-06
- ASPPA Compliance Testing Resources | https://www.asppa.org | Retrieved 2026-03-06

---

## Section 8 — Compliance and Regulatory Framework

> No specific dollar thresholds or indexed values appear in this section. All thresholds are plan-configurable parameters sourced from the current IRS limit table.

### 8.1 ERISA Overview

**Title I vs. Title II scope:**
- **ERISA Title I** (Labor Department jurisdiction): Covers fiduciary duties, participant rights, reporting and disclosure, and enforcement. Applies to ERISA-covered employee benefit plans.
- **ERISA Title II** (Treasury/IRS jurisdiction): Amended the IRC to coordinate pension plan tax rules with ERISA's minimum standards. Most practitioners discuss Title I obligations when referring to "ERISA compliance."

**Who ERISA applies to:** Private-sector employer-sponsored plans. Governmental plans, church plans (unless electing coverage), and non-ERISA voluntary IRA-based arrangements are exempt from most ERISA requirements. Applicability is arrangement-dependent, not plan-type-dependent.

**Why every product decision must be evaluated against ERISA:**
ERISA establishes mandatory fiduciary standards, participant rights, and disclosure obligations that cannot be waived by plan design. A product feature that undermines a fiduciary's ability to meet ERISA obligations — or that fails to deliver required disclosures, maintain required records, or support required participant rights — creates legal exposure for the plan sponsor, fiduciaries, and potentially the service provider.

### 8.2 IRS Qualification Rules

**What makes a plan "qualified" under IRC 401(a):**
A qualified plan meets a comprehensive set of IRC requirements including: written plan document; exclusive benefit rule (assets held for participants only); nondiscrimination in contributions and benefits; minimum participation and coverage standards; vesting schedules within IRC limits; contribution limits; distribution restrictions; plan document availability; and operation in accordance with plan terms.

**Consequences of disqualification:**
Plan disqualification is catastrophic: employer contribution deductions are lost, trust income becomes taxable, and participants may face immediate taxation of vested amounts. Disqualification risk underscores why compliance testing, plan document integrity, and operational accuracy are mission-critical platform functions.

**Key IRC sections agents will encounter:**

| IRC Section | Subject |
|---|---|
| 401(a) | General qualification requirements for qualified plans |
| 401(k) | Cash or deferred arrangement rules; ADP test |
| 402(g) | Annual elective deferral limit |
| 403(b) | Tax-sheltered annuity plan rules |
| 408 | Individual Retirement Accounts and Annuities (IRA rules) |
| 414 | Definitions: controlled group, affiliated service group, compensation |
| 415 | Annual additions limit |
| 416 | Top-heavy plan rules |

**The plan document requirement:** A qualified plan must have a written plan document that is available to participants and regulatory authorities. All plan operations must comply with the written plan document. Operating contrary to plan terms is itself a qualification failure.

### 8.3 Nondiscrimination Framework

**Conceptual purpose:** Nondiscrimination rules exist to ensure that tax-qualified plans provide proportionate benefits to rank-and-file employees, not just owners and executives. Congress conditions the tax advantages of qualified plans on genuine broad-based employee benefit.

**HCE and Key Employee definitions (conceptual):**
- **Highly Compensated Employee (HCE):** An employee who meets IRS-defined ownership or compensation criteria (thresholds are IRS-indexed configurable parameters). HCE classification determines whose contributions are tested under ADP/ACP.
- **Key Employee:** An employee who meets IRS-defined officer, ownership, or compensation criteria (thresholds are IRS-indexed configurable parameters). Key Employee classification drives top-heavy testing.

**ADP and ACP testing concepts:**
- The ADP test compares the average elective deferral percentage of HCEs to that of NHCEs. HCE average may not exceed NHCE average by more than specified permitted ratios (per IRS rules).
- The ACP test applies the same proportionality concept to matching and after-tax contributions.
- Testing failure requires corrective action (refunds to HCEs, or QNEC/QMAC contributions to NHCEs) within IRS correction deadlines.

**Safe harbor alternatives:** Safe harbor 401(k) plans (Traditional and QACA) satisfy ADP and potentially ACP testing by design, eliminating the need for annual testing.

**Controlled group rules:** IRC Section 414 requires that all employers in a controlled group (parent-subsidiary or brother-sister relationships defined by ownership thresholds) be treated as a single employer for qualified plan testing purposes. Affiliated service groups follow similar rules. The platform must support multi-EIN controlled group configurations and aggregated census data for testing.

### 8.4 Vesting Framework

**Vesting types:**
- **Immediate vesting:** The participant is 100% vested in employer contributions from the date contributed. Elective deferrals are always immediately vested.
- **Cliff vesting:** The participant becomes 100% vested after completing a plan-configured number of years of service; no vesting accrues before that point.
- **Graded vesting:** The participant vests incrementally (a plan-configured percentage per year of service) until reaching 100%.

**Elective deferrals:** Always 100% vested immediately. This is a statutory rule, not a plan design choice. [COMPLIANCE-SENSITIVE]

**Service calculation methods:**
- **Hours of service method:** Years of vesting service are counted based on hours worked in a computation period.
- **Elapsed time method:** Vesting service is measured by the period of time elapsed between hire and termination, regardless of hours worked.

**Break in service and rehire effects:** A break in service can pause vesting accrual. Upon rehire before a permanent break, prior service is generally restored. Agents must treat break-in-service and rehire vesting as edge cases requiring explicit acceptance criteria. [EDGE CASE — confirm break-in-service and service restoration rules for each implementation]

### 8.5 Required Notices and Disclosures

| Notice | What It Is | When Required | Who Delivers | Platform Role |
|---|---|---|---|---|
| **404(a)(5) Participant Fee Disclosure** | Discloses plan fees and investment-related information to participants | Annually and upon enrollment; updated when material changes occur | Plan Administrator (via Recordkeeper) | Generate, deliver, and log delivery; support e-delivery |
| **408(b)(2) Service Provider Fee Disclosure** | Discloses fees and services of covered service providers to the plan fiduciary | Before entering or renewing a service contract; when changes occur | Covered service provider | Recordkeeper provides to plan sponsor; platform tracks receipt |
| **Safe Harbor Notice** | Notifies participants of employer safe harbor contribution obligation and their rights | Annually, at least 30 days before plan year start [DATE-VERIFY] | Plan Administrator | Generate and track delivery annually |
| **QDIA Notice** | Notifies participants of the plan's default investment and their right to change | Annually and before first automatic contribution | Plan Administrator | Generate and track delivery; link to QDIA fund information |
| **Blackout Notice (ERISA 101(i))** | Notifies participants of upcoming period when investment direction is suspended | At least 30 days before blackout period begins [DATE-VERIFY] | Plan Administrator | Generate at blackout setup; track delivery and blackout dates |
| **Summary Plan Description (SPD)** | Plain-language description of plan terms and participant rights | Within 90 days of plan eligibility; within 120 days of new plan; every 5 years if amended, 10 years if not [DATE-VERIFY] | Plan Administrator | Store and version-control; deliver upon eligibility |
| **Summary of Material Modifications (SMM)** | Describes material changes to the plan | Within 210 days after end of plan year in which change was adopted [DATE-VERIFY] | Plan Administrator | Generate when plan amendments are processed |
| **Summary Annual Report (SAR)** | Summary of Form 5500 financial information | Within 9 months after plan year end (or 2 months after 5500 due date if extended) [DATE-VERIFY] | Plan Administrator | Generate from year-end financial data; distribute to participants |
| **402(f) Special Tax Notice** | Explains rollover options, withholding, and tax consequences of eligible rollover distributions | At least 30 days before a distribution [DATE-VERIFY] | Plan Administrator | Generate and deliver before distribution processing; track confirmation |
| **Annual Lifetime Income Statement (SECURE 2.0)** | Periodic statement showing projected lifetime income from account balance | At least annually [DATE-VERIFY] | Plan Administrator / Recordkeeper | Generate using IRS-prescribed assumptions; deliver with participant statement |

[COMPLIANCE-SENSITIVE for all notices]

### 8.6 SECURE Act 2.0 — Platform-Relevant Provisions

All effective dates tagged [DATE-VERIFY]. Mandatory vs. optional must be verified at time of requirement writing.

| Provision | What It Changes | Effective Date | Mandatory or Optional | Platform Impact |
|---|---|---|---|---|
| **Mandatory Auto-Enrollment** | New 401(k) and 403(b) plans must include automatic enrollment with minimum default deferral and auto-escalation | Plan years beginning after a date established by SECURE 2.0 [DATE-VERIFY] | Mandatory for new plans | Auto-enrollment engine; QACA or EACA structure required |
| **Super Catch-Up (Ages 60–63)** | Higher catch-up contribution limit for participants aged 60–63 (plan-configurable per IRS rules; no amounts here) | Taxable years beginning after a SECURE 2.0 date [DATE-VERIFY] | Optional for plans to allow | Age-based catch-up limit logic; participant age tracking |
| **LTPT Employee Eligibility — 2-Year Rule** | Replaces 3-year rule for long-term part-time employees | Plan years beginning after a SECURE 2.0 date [DATE-VERIFY] | Mandatory | LTPT hours tracking; eligibility logic update |
| **Roth Account RMD Exemption** | Eliminates lifetime RMDs for designated Roth accounts in employer plans | Taxable years beginning after 2023 [DATE-VERIFY] | Mandatory | Suppress Roth RMD calculation for living participants |
| **Emergency Expense Distributions** | Permits plan distributions for personal/family emergency expenses up to IRS limit | Plan years beginning after a SECURE 2.0 date [DATE-VERIFY] | Optional for plans | New distribution type; self-certification workflow; repayment tracking |
| **Domestic Abuse Distributions** | Permits distributions to domestic abuse victims up to IRS limit; penalty waived | Plan years beginning after a SECURE 2.0 date [DATE-VERIFY] | Optional for plans | New distribution type; self-certification; repayment option |
| **Student Loan Payment Matching** | Permits employer match on qualified student loan payments as if they were plan deferrals | Plan years beginning after 2023 [DATE-VERIFY] | Optional for plans | Loan payment verification; match calculation on QSLPs; contribution source tracking |
| **Roth Employer Contribution Option** | Plans may allow employer contributions to be made as Roth (after-tax) contributions | Plan years beginning after 2023 [DATE-VERIFY] | Optional for plans | New contribution source type (employer Roth); vesting and tax tracking |
| **Roth Catch-Up Requirement for Higher Earners** | Catch-up contributions for participants above IRS compensation threshold must be Roth | Plan years beginning after a SECURE 2.0 date [DATE-VERIFY] | Mandatory for applicable participants | Compensation monitoring; mandatory Roth routing for catch-up of higher earners |
| **RMD Age Increases** | Increases the RMD required beginning age in stages (ages are plan-configurable per IRS rules; no amounts here) | Phased effective dates per SECURE 2.0 [DATE-VERIFY] | Mandatory | Required beginning date recalculation; participant RMD schedule updates |
| **DOL Lost and Found Database Reporting** | Plans must report terminated vested participants to DOL lost and found database | Effective date per DOL rulemaking [DATE-VERIFY] | Mandatory (when effective) | Reporting workflow for deferred vested participants to DOL database |
| **PLESA** | Pension-linked emergency savings accounts linked to DC plans | Plan years beginning after a SECURE 2.0 date [DATE-VERIFY] | Optional for plans | PLESA account type; contribution limits; withdrawal processing; match interaction |
| **Auto-Portability Services** | Facilitates automatic transfer of small balances for job changers to new employer plans | Enabled/encouraged by SECURE 2.0; not a uniform plan requirement [DATE-VERIFY] | Optional; platform capability | Auto-rollover IRA to new plan transfer capability; ERISA safe harbor compliance |
| **Starter 401(k) Plans** | New simplified 401(k) plan type for small employers without existing plans | Plan years beginning after a SECURE 2.0 date [DATE-VERIFY] | Optional (new plan type available) | Support for Starter 401(k) plan structure with simplified compliance |
| **Expanded EPCRS Self-Correction** | Expands eligibility for self-correction of plan errors without IRS submission | Effective upon SECURE 2.0 enactment [DATE-VERIFY] | Available to all plans | Self-correction workflows; error documentation; audit trail |

**Sources (Section 8):**
- ERISA Title I and Title II | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa/laws-and-regulations/laws/erisa | Retrieved 2026-03-06
- IRS Retirement Plans — Qualification | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov/bill/117th-congress/house-bill/2954 | Retrieved 2026-03-06
- DOL Reg. 29 CFR Part 2550 (ERISA fiduciary regulations) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Nondiscrimination Testing Resources | https://www.asppa.org | Retrieved 2026-03-06

---

## Section 9 — Technology and System Landscape

### 9.1 Recordkeeping Systems

**What a recordkeeping system does at its core:**
A recordkeeping system maintains the individual account records of every plan participant. It tracks contributions, investment activity, distributions, loans, fees, and the resulting account balances by contribution source and investment fund. It is the system of record for participant-level plan data.

**Daily valuation vs. balance forward plans:**
- **Daily valuation:** Account balances are updated daily based on current investment fund NAV prices. Most modern DC plans are daily-valued. Participants can view current account values and transact on business days.
- **Balance forward:** Account balances are updated only at defined valuation dates (e.g., quarterly). Less common in current market; legacy plans may still operate this way. Platform architecture for balance-forward plans is simpler but limits participant self-service capability.

**Key functional modules of a recordkeeping system:**
- Participant record management
- Contribution processing and allocation
- Investment election and trade execution
- Loan origination and administration
- Distribution processing
- Vesting calculation
- Compliance testing data collection
- Notice generation and delivery
- Participant and plan sponsor portal
- Reporting and statement generation
- Trust/custodian interface
- Payroll integration

### 9.2 Plan Administration Systems

**Compliance testing engines:** Standalone or integrated systems that calculate ADP, ACP, 415, 416, 410(b), and 401(a)(4) test results from recordkeeping data. Some recordkeepers provide integrated testing; others rely on TPA systems fed by recordkeeper exports.

**Plan document systems:** Document drafting and management systems (e.g., FIS Relius, Pension Pro) used by TPAs to maintain and amend plan documents and adoption agreements. These systems may interface with the recordkeeping platform to confirm plan design parameters are consistent with the plan document.

**Government reporting (5500 preparation):** Systems or modules that aggregate plan-level financial, participant count, and service provider data required for Form 5500 filing. May be integrated with the recordkeeper or operated by the TPA using recordkeeper data exports.

### 9.3 Participant and Sponsor Portals

**Self-service capabilities participants expect:**
- Account balance viewing (by source, by fund)
- Transaction history
- Deferral rate changes
- Investment election changes (fund-to-fund transfers, future contribution allocation)
- Loan modeling and origination
- Distribution requests
- Beneficiary designation updates
- Document and notice access (SPD, statements, tax documents)
- Contribution history and year-to-date amounts
- Projected retirement income modeling

**Plan sponsor management and monitoring needs:**
- Participant census data management
- Contribution submission and approval workflows
- Payroll file upload and exception review
- Compliance test result access
- Employee enrollment status monitoring
- Reporting (participation rates, contribution totals, fund allocations)
- Notice delivery confirmation
- Forfeiture account management

**TPA portal data access patterns:** TPA users require access to plan-level and participant-level data for compliance testing, plan administration, and client reporting. TPA access must be role-scoped and audited. TPAs must not have access to participant PII beyond what is necessary for their administrative function.

**Mobile and accessibility considerations:** Participant portals must meet accessibility standards (WCAG 2.1 or successor) [INDUSTRY PRACTICE — confirm specific standards applicable]. Mobile-responsive design or native mobile application support is expected for participant portals.

### 9.4 Payroll System Integration

**File-based integration patterns and common formats:**
- Fixed-width files: Legacy format with positional field definitions; common in older payroll systems
- Delimited files (CSV, tab-delimited): More flexible; field order defined by header or mapping
- SPARK Institute standard file formats: Industry-standard field definitions for contribution data, census data, and loan/distribution data

**API-based integration — SPARK Institute API Integration Guidelines (June 2025):**
The SPARK Institute has defined RESTful API standards for retirement industry data exchange. Key APIs include:
- **Census API:** Employee demographic and eligibility data
- **Contribution API:** Payroll contribution amounts by employee and source
- **Loan API:** Loan origination, repayment schedule, and payoff data
- **Distribution API:** Distribution requests and status
- **Participant Balance API:** Account balance data for payroll integration (loan repayment, benefit calculations)

API integration enables real-time validation, reduced manual data entry errors, and faster contribution processing compared to batch file delivery.

**360° integration concept:** Bidirectional payroll integration where data flows both from payroll to recordkeeper (contributions, census) and from recordkeeper to payroll (loan repayment amounts, distribution events, vesting data). Ensures payroll deductions and plan records remain synchronized.

**Common failure modes and exception handling:**
- Missing or unmatched participant records
- Invalid or out-of-range contribution amounts
- Limit violations (deferral, annual additions)
- Duplicate payroll file submissions
- Incorrect source/money type codes
- Missing or invalid SSNs

All failures must be routed to an exception queue with sufficient detail for the plan sponsor or TPA to investigate and resolve.

### 9.5 Investment Platform Integration

**Trust accounting and NAV pricing feeds:** Daily NAV prices for all funds on the investment menu are received from the fund company or a pricing aggregator and applied to participant account valuations. The trust accounting system reconciles its asset positions to the recordkeeper's unit holdings daily.

**Trade execution and confirmation flows:** The recordkeeper aggregates net participant trade instructions and submits them to the custodian/trustee for execution at end-of-day NAV. Trade confirmations are returned to the recordkeeper for posting to participant accounts.

**Revenue sharing and fee data feeds:** Investment managers may pay revenue sharing to the recordkeeper or plan based on assets under management. Revenue sharing rates must be disclosed under ERISA fee disclosure rules and may be used to offset plan expenses. The platform must track revenue sharing credits and apply them per plan policy.

**Rule 22c-2 shareholder data reporting:** SEC Rule 22c-2 requires recordkeepers to report participant-level transaction data to fund companies upon request to assist in detecting market timing. The platform must support production of this data within required timeframes.

### 9.6 Document Management and Notices

**Plan document storage and version control:** The current plan document, adoption agreement, and all prior versions must be stored with effective dates. Amendments must be tracked and linked to their effective dates. Regulatory audit requests require the ability to produce the plan document in effect on any given date.

**Automated notice generation and delivery tracking:**
- The platform must generate required notices triggered by plan events (enrollment, distribution, blackout, plan year start, plan amendment).
- Delivery must be tracked and confirmed (email open tracking, return receipt, or positive confirmation depending on delivery method).
- Failed deliveries must generate alerts for follow-up.

**E-delivery standards and DOL electronic disclosure rules:** The DOL's electronic disclosure safe harbor rules (Final Rule 2020) allow electronic delivery of required disclosures with appropriate notice and access. [DATE-VERIFY — confirm current DOL e-delivery rule requirements] Participants must have the ability to opt for paper delivery. The platform must support both electronic and paper delivery workflows.

**Audit trail requirements:** All notice generation, delivery attempts, confirmations, and failures must be logged with timestamps and actor identity. Logs must be retained per ERISA Section 107 requirements.

### 9.7 Data Security and Cybersecurity

**SPARK Institute Data Security Oversight Board standards:** The SPARK Institute's DSOB has published cybersecurity standards for retirement industry data handlers covering access controls, encryption, incident response, vendor management, and audit. [INDUSTRY PRACTICE — reference SPARK DSOB standards for current requirements]

**PII handling:** Participant data includes highly sensitive PII including Social Security Numbers, dates of birth, compensation, and account balances. Access must be role-scoped and audited. SSNs must be encrypted at rest and in transit. Display of SSNs must be masked except for authorized users in defined contexts.

**DOL cybersecurity guidance (2021):** The DOL issued guidance (Tips for Hiring a Service Provider with Strong Cybersecurity Practices, Cybersecurity Program Best Practices, Online Security Tips for Participants) establishing baseline cybersecurity expectations for plan sponsors and service providers. [DATE-VERIFY — confirm current DOL cybersecurity guidance in effect]

**Authentication standards for participant portals:** Multi-factor authentication (MFA) is the industry standard for participant portal access. Single-factor authentication (username/password only) is insufficient given the sensitivity of retirement account data and the prevalence of credential stuffing attacks. [INDUSTRY PRACTICE]

**Sources (Section 9):**
- SPARK Institute API Integration Guidelines, June 2025 | https://www.sparkinstitute.org | Retrieved 2026-03-06
- SPARK Institute DSOB Cybersecurity Standards | https://www.sparkinstitute.org | Retrieved 2026-03-06
- DOL Cybersecurity Guidance (2021) | https://www.dol.gov/agencies/ebsa/employers-and-advisers/plan-administration-and-compliance/cybersecurity | Retrieved 2026-03-06
- SEC Rule 22c-2 | https://www.sec.gov | Retrieved 2026-03-06
- DOL Electronic Disclosure Final Rule (2020) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06

---

## Section 10 — Implementation and Data Integration

### Plan Conversion and Data Migration

A plan conversion occurs when a plan transitions from one recordkeeper to another. The conversion involves migrating participant-level data including account balances by source and investment fund, transaction history, loan data, vesting service records, beneficiary designations, and compliance testing history. Conversion data must be validated against the prior provider's data and reconciled to the trust before the new platform goes live. Blackout periods are typically required during conversion.

### Census Data Quality and Common Validation Failures

Census data from the employer is the foundation for eligibility determination, vesting calculation, and compliance testing. Common data quality issues include:
- Missing or invalid SSNs
- Incorrect dates of birth or hire (affects eligibility and vesting)
- Missing hours data (required for eligibility and vesting under hours-based methods)
- Incorrect employment status (active vs. terminated affects contribution processing and distribution eligibility)
- Inconsistent compensation data across payroll periods
- Missing rehire dates

All census data must pass validation before being applied to participant records. Failures must be reported to the plan sponsor or TPA for resolution.

### Payroll Data Mapping Challenges

Payroll systems encode contribution data using their own field structures and source codes. Mapping payroll source codes to the recordkeeper's money types is a critical integration task. Common challenges:
- Multiple payroll deduction codes mapping to the same money type
- Catch-up contributions not differentiated from regular deferrals in payroll export
- Roth contributions not clearly distinguished from pre-tax deferrals
- Loan repayments included in contribution files without clear labeling
- Partial payroll periods and off-cycle payrolls requiring manual mapping

### Contribution Reconciliation Concepts

Contribution reconciliation ensures that the amounts received in the trust match the amounts recorded in the recordkeeping system. Reconciliation occurs between: payroll file amounts, funding wire amount, trust receipt, and posted contribution amounts. Discrepancies must be investigated and resolved. Common causes: wire timing differences, payroll adjustments processed after file submission, and rounding at the record level.

### Provider File Formats

- **SPARK Institute standard formats:** Define field layouts for contribution, census, loan, and distribution files. Using SPARK-standard formats reduces custom integration work.
- **Fixed-width files:** Fields at defined character positions; common in legacy payroll systems; error-prone if field definitions change.
- **Delimited files:** Fields separated by a delimiter (comma, tab, pipe); more flexible; require header validation.
- **API:** JSON-based RESTful APIs per SPARK Institute June 2025 guidelines; real-time or scheduled; support bidirectional integration.

### Exception Handling and Correction Workflows

Plan operational errors must be corrected promptly to maintain plan qualification. The platform must support:
- Identification of errors (contribution over-limits, incorrect vesting, missed distributions)
- Calculation of correction amounts including lost earnings where required
- Posting of corrective transactions with complete audit trail
- Documentation of the correction for compliance records

### EPCRS and Self-Correction

The IRS **Employee Plans Compliance Resolution System (EPCRS)** provides a framework for correcting plan qualification failures:
- **SCP (Self-Correction Program):** Plans may self-correct certain operational failures without IRS submission, within specified timeframes. SECURE 2.0 significantly expanded SCP eligibility. [DATE-VERIFY]
- **VCP (Voluntary Correction Program):** Plans submit the failure and proposed correction to the IRS for approval and a compliance statement.
- **Audit CAP:** Correction negotiated with IRS when the failure is discovered during an audit.

### Plan Mergers and Spinoffs

Plan mergers (combining two plans into one) and spinoffs (splitting one plan into two) are complex events requiring:
- Asset transfers and reconciliation
- Participant data migration
- Compliance testing on the combined or successor plan
- Possible short plan year filings
- Anti-cutback analysis (benefits cannot be reduced by a merger or spinoff)
- [EDGE CASE — mergers and spinoffs require explicit acceptance criteria for data integrity, testing, and anti-cutback compliance]

### Controlled Group Data — Multi-EIN Structure Requirements

When a controlled group of employers participates in a single plan or in plans that must be aggregated for testing, the platform must:
- Maintain separate employer records for each EIN
- Track employee compensation and service across all controlled group members
- Aggregate census data for compliance testing purposes
- Support allocation of employer contributions across participating employers

**Sources (Section 10):**
- IRS EPCRS Revenue Procedure | https://www.irs.gov/retirement-plans/correcting-plan-errors | Retrieved 2026-03-06
- SECURE 2.0 Act Section 305 (Expanded SCP) | https://www.congress.gov | Retrieved 2026-03-06
- SPARK Institute File Format Standards | https://www.sparkinstitute.org | Retrieved 2026-03-06
- DOL VFCP | https://www.dol.gov/agencies/ebsa/employers-and-advisers/correction-programs/vfcp | Retrieved 2026-03-06
- ASPPA Plan Merger and Spinoff Resources | https://www.asppa.org | Retrieved 2026-03-06

---

## Section 11 — Glossary

**ACP Test (Actual Contribution Percentage Test):** Annual nondiscrimination test comparing the average contribution percentage of HCEs (employer matching and employee after-tax contributions) to that of NHCEs. Failure requires corrective action. *System context:* Driven by contribution data by source; applies to plans with matching or after-tax contributions not using ACP safe harbor.

**ADP Test (Actual Deferral Percentage Test):** Annual nondiscrimination test comparing the average elective deferral percentage of HCEs to that of NHCEs. Failure requires refunds to HCEs or QNEC/QMAC contributions to NHCEs. *System context:* Applies to 401(k) plans not using ADP safe harbor; requires HCE/NHCE classification of all eligible employees.

**Auto-Enrollment:** A plan design feature where eligible employees are automatically enrolled at a default deferral rate unless they affirmatively opt out. Required for new 401(k) and 403(b) plans under SECURE 2.0 (effective date configurable). *System context:* Default deferral rate and QDIA must be configured; opt-out workflow required; notice delivery required.

**Auto-Escalation:** A plan feature that automatically increases a participant's deferral rate by a plan-configured increment on a plan-configured schedule until a plan-configured maximum is reached. *System context:* Scheduled trigger logic; opt-out capability; notice requirement.

**Beneficiary:** A person or entity designated by the participant to receive the account balance upon the participant's death. May be primary or contingent; spousal consent rules may apply. *System context:* Beneficiary record tied to participant; triggers death distribution workflow upon participant death.

**Blackout Period:** A period during which participant rights to direct investments or obtain loans or distributions are temporarily suspended, typically during a plan conversion or fund mapping change. *System context:* Requires advance notice (ERISA 101(i)); investment and transaction restrictions enforced by platform; blackout dates logged.

**Break in Service:** A plan year (or computation period) in which an employee fails to complete a minimum number of hours of service (or equivalent under elapsed time method), potentially interrupting vesting service accrual or triggering forfeiture. *System context:* Tracked in participant service record; affects vesting and eligibility upon rehire.

**Catch-Up Contribution:** An additional elective deferral permitted for participants who have reached a plan-configurable age threshold (per IRS rules), allowing them to contribute above the standard annual deferral limit. Super Catch-Up for ages 60–63 introduced by SECURE 2.0. *System context:* Age-based eligibility flag; separate limit monitoring from standard deferrals; mandatory Roth for higher earners per SECURE 2.0 [DATE-VERIFY].

**Compensation (415, W-2, Includible — types and purposes):**
- **415 Compensation:** Compensation as defined under IRC Section 415(c)(3), used as the basis for annual additions limits.
- **W-2 Compensation:** Wages reported on Form W-2; a common compensation definition in plan documents.
- **Includible Compensation:** Compensation definition used in 403(b) plans; generally W-2 compensation from the employer.
*System context:* The compensation definition used by a plan is a plan-configurable parameter in the adoption agreement. The platform must apply the correct compensation definition for contribution formulas, limit calculations, and nondiscrimination testing.

**Controlled Group:** Two or more business entities under common ownership (parent-subsidiary or brother-sister) treated as a single employer for retirement plan qualification purposes under IRC Section 414. *System context:* Multi-EIN configuration; aggregated testing data; shared employee tracking.

**Deemed Distribution:** The tax event that occurs when a participant loan is treated as distributed due to failure to repay, without an actual cash payment. Taxable but the loan balance remains on the books. *System context:* Triggered after cure period expiration; generates 1099-R with appropriate distribution code; loan status updated.

**Designated Roth Account:** A separately accounted portion of an employee's account in a 401(k) or 403(b) plan representing the employee's designated Roth contributions (after-tax) and their earnings. Qualified distributions are tax-free. No lifetime RMDs under SECURE 2.0. *System context:* Separate source tracking from pre-tax deferrals; distinct tax treatment for distributions; Roth ordering rules apply.

**EACA (Eligible Automatic Contribution Arrangement):** An automatic enrollment plan arrangement meeting IRS requirements, including a permissive 90-day withdrawal right and default investment in a QDIA. *System context:* 90-day withdrawal window must be enforced; QDIA notice required; required notice timing.

**EPCRS (Employee Plans Compliance Resolution System):** The IRS framework for correcting retirement plan qualification failures through self-correction (SCP), voluntary correction (VCP), or audit correction (Audit CAP). *System context:* Correction workflows must support EPCRS documentation; audit trail required.

**Eligible Rollover Distribution (ERD):** A distribution from a qualified plan that is eligible to be rolled over to another eligible retirement plan or IRA. Subject to mandatory 20% federal withholding unless directly rolled over. *System context:* Triggers 402(f) Special Tax Notice; withholding logic; rollover election capture.

**Elective Deferral:** A contribution made by an employee from their compensation to a qualified plan on a pre-tax (Traditional) or after-tax (Roth) basis pursuant to a salary reduction agreement. Always 100% vested immediately. *System context:* Subject to annual limit (plan-configurable per IRS table); tracked as separate source from employer contributions.

**Entry Date:** The date on which a newly eligible employee is permitted to begin participation in the plan. Entry dates are plan-configurable (e.g., immediate, first of month, semi-annually). *System context:* Eligibility engine calculates projected entry date; enrollment workflow triggered on entry date.

**Fiduciary:** Under ERISA, any person who exercises discretionary authority or control over plan management or assets, renders investment advice for a fee, or has discretionary responsibility in plan administration. *System context:* Fiduciary actions must be logged with audit trail; platform must not assume fiduciary functions without explicit design authorization.

**Force-Out Distribution:** An involuntary distribution of a terminated participant's small balance when it falls below the plan-configured mandatory distribution threshold (subject to IRS rules). Balances in the mid-range must be rolled over to an auto-rollover IRA. *System context:* Balance threshold monitoring; automatic rollover IRA processing; participant notification workflow.

**Forfeiture:** The unvested portion of an employer contribution account that a participant loses upon termination of employment before satisfying the plan's vesting schedule. *System context:* Credited to forfeiture account; used per plan document (reduce contributions, pay expenses, fund QNEC/QMAC); timing governed by plan document and IRS rules.

**Form 5500:** Annual information return filed by most ERISA-covered plans with the DOL and IRS reporting plan financial condition, investments, and operations. *System context:* Recordkeeper provides financial and participant data to plan sponsor or TPA for 5500 preparation; filing deadlines are regulatory.

**Form 1099-R:** IRS tax form reporting distributions from retirement plans, IRAs, and annuities. Issued to distributees and filed with the IRS by the plan. *System context:* Generated from distribution records; distribution codes must be accurate; delivery and IRS filing are time-sensitive.

**Hardship Withdrawal:** A distribution from a 401(k) or 403(b) plan due to an immediate and heavy financial need that cannot be satisfied from other reasonably available resources. Subject to income tax; early distribution penalty applies unless an exception applies. *System context:* Qualifying reason validation; self-certification workflow (SECURE 2.0); documentation and audit trail.

**HCE (Highly Compensated Employee):** An employee who meets IRS-defined ownership or prior-year compensation criteria (thresholds are IRS-indexed configurable parameters). HCE classification affects ADP/ACP testing. *System context:* Annual HCE determination workflow; prior-year compensation lookback required; plan-level HCE list used in testing.

**Hours of Service:** A measure of employee service used for eligibility and vesting calculations. An employee earns hours of service for each hour for which they are paid or entitled to be paid. *System context:* Hours must be tracked per computation period; source data is payroll or HR system; used in eligibility engine and vesting service calculation.

**In-Service Withdrawal:** A distribution from a plan while the participant is still employed. Permitted only if the plan document allows it and applicable IRC requirements are met (e.g., age-based, hardship, PLESA). *System context:* In-service distribution type must be authorized in plan design; age eligibility check; applicable tax and withholding rules apply.

**Key Employee:** An employee who meets IRS-defined officer, ownership, or compensation criteria (thresholds are IRS-indexed configurable parameters). Key Employee classification is used in top-heavy testing. *System context:* Annual Key Employee determination; used in 416 top-heavy test; minimum contribution obligations if plan is top-heavy.

**Loan (Plan Loan):** A loan made to a participant from their vested account balance, governed by IRC Section 72(p) and the plan's loan policy. Must meet IRS requirements for amount, repayment, and interest rate. *System context:* Loan origination, repayment, deemed distribution, and offset workflows; balance tracking; loan limit calculation.

**LTPT Employee (Long-Term Part-Time Employee):** Under SECURE Act and SECURE 2.0, a part-time employee who meets consecutive-year qualifying hours thresholds must be permitted to make elective deferrals. The plan may exclude LTPT employees from employer contributions. *System context:* Multi-year hours tracking; eligibility flag; separate treatment from standard eligibility.

**Match True-Up:** A year-end corrective employer matching contribution for participants whose match formula, calculated annually, exceeds the match actually funded on a per-payroll basis. *System context:* Year-end match recalculation; corrective contribution processing; interaction with contribution limits.

**Money Type / Contribution Source:** The classification of a contribution or balance by its origin and regulatory characteristics (employee pre-tax, Roth, employer match, profit sharing, rollover, after-tax, loan repayment, QNEC, QMAC, PLESA). Drives vesting, distribution eligibility, and tax treatment. *System context:* Every transaction tagged by source; vesting and distribution logic driven by source.

**NHCE (Non-Highly Compensated Employee):** Any employee who is not an HCE. NHCEs are the comparison group in ADP/ACP nondiscrimination testing. *System context:* NHCE list determined as complement of HCE list for each plan year.

**Normal Retirement Age (NRA):** The age specified in the plan document at which a participant is entitled to an unreduced retirement benefit or distribution. *System context:* Plan-configurable parameter; triggers in-service withdrawal eligibility if plan allows; affects distribution processing.

**Participant-Directed Investment:** A plan design where participants control the investment of their own account balances among plan investment options. Enables ERISA Section 404(c) fiduciary relief. *System context:* Investment election capture; fund transfer processing; QDIA default logic.

**PLESA (Pension-Linked Emergency Savings Account):** A short-term savings account linked to a DC plan (authorized by SECURE 2.0) allowing non-HCE participants to save after-tax dollars for emergency use with flexible withdrawal rights. *System context:* New account/source type; contribution limit monitoring; employer match interaction; withdrawal processing without penalty.

**Plan Document:** The legal document establishing and governing the retirement plan, including all terms, eligibility rules, contribution formulas, vesting schedules, and participant rights. *System context:* All platform configuration must align with the plan document; version controlled in document management system.

**Plan Sponsor:** The employer (or employee organization) that establishes and maintains the retirement plan. Holds ultimate responsibility for plan operation. *System context:* Plan sponsor portal access; approval workflows for plan-level decisions; amendment authority.

**Plan Year:** The 12-month period designated in the plan document for plan operations and compliance testing. Most plans use the calendar year, but any 12-month period may be elected. *System context:* Drives all annual calculation periods, testing cycles, and filing deadlines.

**Pooled Employer Plan (PEP):** A type of multiple employer plan operated by a registered Pooled Plan Provider, allowing unrelated employers to participate in a single plan structure with the PPP serving as plan administrator and named fiduciary. *System context:* Multi-employer data structure; PPP as administrative fiduciary; employer-level plan design segmentation.

**Profit Sharing:** A discretionary employer contribution to a DC plan not tied to a specific matching formula. The employer decides the contribution amount each year. *System context:* Allocated per plan document formula (pro-rata, integrated, or new comparability); subject to 415 limit; vesting schedule applies.

**QACA (Qualified Automatic Contribution Arrangement):** An automatic enrollment arrangement meeting QACA requirements under IRC Section 401(k)(13), including minimum default deferral rates, auto-escalation, and required employer contributions. Provides ADP/ACP safe harbor. *System context:* Auto-enrollment engine with QACA minimums; up to 2-year cliff vesting on safe harbor contributions; QACA notice required.

**QDRO (Qualified Domestic Relations Order):** A domestic relations order creating or recognizing the right of an alternate payee to plan benefits. Must meet specific requirements under ERISA and IRC. *System context:* Written QDRO procedures required; qualification determination workflow; alternate payee account creation; [RECOMMEND LEGAL/COMPLIANCE REVIEW].

**QDIA (Qualified Default Investment Alternative):** An investment alternative designated as the default investment for participants who do not make an affirmative investment election. Provides fiduciary relief when QDIA requirements are met. *System context:* QDIA designation in plan configuration; default routing of unapplied contributions; QDIA notice generation.

**Qualified Plan:** A retirement plan that meets the requirements of IRC Section 401(a) or other applicable IRC qualification sections, entitling the employer to a tax deduction and participants to tax-deferred growth. *System context:* Platform must enforce all qualification requirements through configuration and processing controls.

**Recordkeeper:** The service provider that maintains individual participant account records, processes transactions, and serves as the technology platform for plan administration. *System context:* CORE is the recordkeeping system.

**Rehire:** The re-employment of a former employee. Triggers re-evaluation of eligibility, vesting service restoration, forfeiture restoration, and break-in-service rules. *System context:* Rehire date required in participant record; prior service retrieval; re-eligibility determination.

**Required Beginning Date (RBD):** The date by which a participant must begin receiving Required Minimum Distributions. Determined by the participant's required beginning age (plan-configurable per IRS rules, modified by SECURE 2.0) and employment status. *System context:* Automated RBD calculation; RMD trigger event; [DATE-VERIFY — confirm current RMD age rules].

**RMD (Required Minimum Distribution):** The minimum amount that must be distributed from a retirement account each year after the participant reaches the required beginning date. Calculated based on account balance and IRS life expectancy tables. No lifetime RMD for Roth accounts in employer plans under SECURE 2.0. *System context:* Annual RMD calculation; automated distribution trigger; penalty tracking if underdistributed; Roth exemption logic.

**Rollover (Direct vs. Indirect):**
- **Direct rollover:** Distribution paid directly to an eligible retirement plan or IRA; avoids mandatory 20% withholding.
- **Indirect rollover:** Distribution paid to the participant; must be re-contributed within 60 days; subject to 20% mandatory withholding.
*System context:* Rollover election capture at distribution; withholding logic differs; rollover-in processing from other plans.

**Safe Harbor Plan:** A 401(k) plan meeting safe harbor requirements (Traditional or QACA) that is deemed to pass ADP and, in some cases, ACP nondiscrimination testing. Requires required employer contributions and advance notice to participants. *System context:* Safe harbor flag in plan design; notice generation; employer contribution formula enforcement.

**SAR (Summary Annual Report):** A summary of the Form 5500 annual report distributed to plan participants. Must be provided within regulatory deadlines after Form 5500 filing. *System context:* Generated from year-end financial data; delivery tracked.

**Short Plan Year:** A plan year of less than 12 months, occurring at plan establishment, termination, or change of plan year. Affects compliance testing, contribution limits, and filing requirements. *System context:* [EDGE CASE — short plan year logic must be explicitly addressed in acceptance criteria for any affected feature].

**SPD (Summary Plan Description):** A plain-language document explaining plan terms, participant rights, and claims procedures. Required to be provided to all plan participants within regulatory deadlines. *System context:* Document management and delivery; version control; delivery tracking.

**Top-Heavy Plan:** A plan in which the account balances of key employees exceed a regulatory threshold percentage of total plan assets (plan-configurable per IRS rules). Triggers minimum employer contribution requirements for non-key employees. *System context:* Annual top-heavy determination; minimum contribution calculation and posting if top-heavy.

**TPA (Third Party Administrator):** A service provider that performs plan administration functions (compliance testing, 5500 preparation, plan document maintenance, distribution processing) on behalf of the plan sponsor. May be appointed as Section 3(16) plan administrator. *System context:* TPA portal access; data exchange; 3(16) appointment tracking.

**Trustee:** The legal holder of plan assets. May be a directed trustee (acts on instructions) or discretionary trustee (exercises independent judgment). In most DC plans, a directed corporate trustee. *System context:* Trust accounting system integration; trade instruction flow; asset reconciliation.

**Universal Availability Rule (403(b)):** Under IRC Section 403(b)(12), all employees of a 403(b) plan sponsor must be permitted to make elective deferrals unless specifically excluded by statute. The permitted exclusions are different from and more limited than those in 401(k) plans. *System context:* Eligibility logic must enforce Universal Availability for 403(b) plans; exclusion class validation.

**Valuation Date:** The date on which plan assets are valued and participant account balances are updated. For daily-valued plans, every business day is a valuation date. *System context:* NAV pricing feed; daily valuation processing; balance-forward valuation schedule if applicable.

**Vesting:** The process by which a participant acquires a non-forfeitable right to employer contributions in their account. Elective deferrals are always 100% vested immediately. Employer contributions vest per the plan's vesting schedule (immediate, cliff, or graded). *System context:* Vesting record tracking; service calculation; vested balance calculation drives distribution and loan eligibility.

**Vesting Service:** Service credited toward the participant's vesting schedule. May be measured by hours of service or elapsed time, as specified in the plan document. *System context:* Service tracking from hire date; break-in-service monitoring; vesting percentage calculation engine.

**VFCP (Voluntary Fiduciary Correction Program):** A DOL program allowing plan fiduciaries to self-correct certain prohibited transactions (including late deposits) and obtain a no-action letter from DOL. Requires calculation and payment of lost earnings. *System context:* Late deposit correction workflow; lost earnings calculation; DOL submission support.

**Year of Service:** A 12-month computation period in which an employee completes a plan-configured minimum number of hours of service, earning credit for eligibility or vesting purposes. *System context:* Hours tracking; computation period determination; year-of-service credit in eligibility and vesting engines.

**Sources (Section 11):**
- IRS Retirement Plans Glossary | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL ERISA Glossary | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Retirement Dictionary | https://www.asppa.org | Retrieved 2026-03-06
- NIPA Retirement Plan Terminology | https://www.nipa.org | Retrieved 2026-03-06

---

## Section 12 — Agent Usage Rules

These are binding instructions for any agent consuming this World File.

### Rule 1 — Domain Knowledge Only

This file explains concepts and processes. Specific dollar limits, percentages, thresholds, and IRS-indexed values are not in this file by design. Write requirements as:

> *"system-configurable parameter per current plan configuration or IRS limit table."*

Never hardcode annual dollar limits, compensation thresholds, or percentage caps in requirements derived from this document.

### Rule 2 — Compliance Flags

Tag any requirement touching contribution limits, testing, distributions, RMDs, notices, fiduciary actions, or plan amendments:

> **[COMPLIANCE-SENSITIVE]**

This tag signals that the requirement must be reviewed against current regulatory requirements before finalization.

### Rule 3 — Plan-Level Configurability

Distinguish between three dimensions in every requirement:

| Dimension | Definition |
|---|---|
| **(a) Platform behavior** | What the system does (logic, workflow, calculation) |
| **(b) Plan configuration** | How the plan sets it up (adoption agreement parameters) |
| **(c) Regulatory floor/ceiling** | IRS/DOL minimums and maximums that constrain plan configuration |

Requirements must reflect all three dimensions. A requirement that describes only platform behavior without acknowledging plan configuration is incomplete.

### Rule 4 — DATE-VERIFY Protocol

Any content tagged **[DATE-VERIFY]** requires the agent to confirm the effective date and applicability in authoritative sources before writing the requirement. If uncertain, phrase as:

> *"effective-date-configurable."*

Do not write a requirement based on an assumed effective date for any SECURE 2.0 or other legislative provision without verification.

### Rule 5 — Mandatory vs. Optional

SECURE 2.0 provisions vary — some are mandatory for plans, some are optional plan design choices. Always verify and state which before writing scope. The distinction affects whether the platform must enforce the rule or whether it is a plan design option that must be configurable.

### Rule 6 — Government Plan Flag

457(b) governmental plans are exempt from ERISA. Tag all government plan requirements:

> **[GOVERNMENT PLAN — NON-ERISA]**

and scope separately. ERISA fiduciary, reporting, and disclosure requirements do not apply to governmental plans. Requirements written for ERISA-covered plans must not be applied to governmental plans without explicit adaptation.

### Rule 7 — Legal Review Flag

Requirements involving fiduciary responsibility boundaries, QDRO processing, plan document interpretation, or novel regulatory provisions must include:

> **[RECOMMEND LEGAL/COMPLIANCE REVIEW]**

This flag indicates the requirement has dimensions that should not be finalized without subject matter expert or legal review.

### Rule 8 — Edge Case Surfacing

Requirements touching any of the following must explicitly call out the edge case and recommend it be addressed in acceptance criteria:
- Controlled groups
- Mid-year amendments
- Rehire scenarios
- QDROs
- Plan mergers / spinoffs
- Short plan years
- Correction workflows

Failure to surface edge cases in requirements is a primary cause of production defects in retirement administration systems.

### Rule 9 — Data Privacy

All requirements involving PII (Social Security Numbers, dates of birth, compensation data, account balances) must reference applicable data privacy, security, and ERISA cybersecurity standards. Requirements must specify:
- Access control (role-scoped)
- Encryption expectations (at rest and in transit)
- Display masking requirements
- Audit logging of PII access

### Rule 10 — NEEDS-VALIDATION Protocol

Where authoritative sources conflict or are unclear, label content:

> **[NEEDS-VALIDATION]**

Write the requirement as configurable pending verification, and create a verification task before the requirement is finalized. Do not write a definitive requirement on an unresolved regulatory question.

### Rule 11 — Out-of-Scope Boundary

Do not attempt to write requirements for:
- DB actuarial calculations (pension benefit formulas, pension funding)
- Tax or legal advice
- Non-U.S. retirement plans
- Investment performance recommendations

If a feature request touches these areas, flag it and escalate to the appropriate subject matter expert. Attempting to write requirements outside the DC recordkeeping domain without expertise will produce unacceptable quality.

---

*End of Retirement World — RW1.0*

---

*Document integrity note: All [DATE-VERIFY] tags must be resolved against current authoritative sources before any tagged content is used as the basis for a finalized product requirement. All [COMPLIANCE-SENSITIVE] tags require compliance review. All [NEEDS-VALIDATION] tags require verification before requirement finalization.*
