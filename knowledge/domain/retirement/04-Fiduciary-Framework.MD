# Skill: Fiduciary Framework
**Skill-ID:** 04-Fiduciary-Framework
**World:** Retirement World v1.0
**Category:** Regulatory & Compliance
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the ERISA fiduciary framework — who is a fiduciary, what standards apply, and what the platform must do to support fiduciary obligations. Platform features that automate decisions must be evaluated against this framework to prevent unintended fiduciary assumption and legal exposure.

---

## 1. What a Fiduciary Is Under ERISA

Under ERISA Section 3(21), a person is a **fiduciary** to the extent they:
- Exercise discretionary authority or control over plan management or plan assets
- Render investment advice for a fee or other compensation with respect to plan assets, or have authority to do so
- Have discretionary authority or responsibility in plan administration

**Fiduciary status is functional** — determined by what a person actually does, not their title. A service provider performing only ministerial functions is not a fiduciary. A service provider exercising discretion crosses into fiduciary status.

**Why this matters for platform design:** A platform that automates a decision previously made by a human may inadvertently assume fiduciary status for that function. Features that automate investment changes, approve hardship requests, or calculate and distribute benefits must be designed with explicit awareness of whether the platform is acting as a fiduciary or executing the instructions of one.

**Agent rule:** Platform design must not expose Congruent Solutions to unintended fiduciary liability.

---

## 2. ERISA Section 3(16): Plan Administrator

- **Definition:** The person designated in the plan document as the plan administrator. If no designation is made, the plan sponsor is the plan administrator by default.
- **Responsibilities:** Day-to-day plan administration — distributing required notices, maintaining records, filing Form 5500, acting on participant requests.
- **Who typically holds this role:** The plan sponsor employer. In some arrangements, a TPA or outsourced provider is explicitly appointed.
- **Platform implication:** When a TPA or third party is the Section 3(16) administrator, that party's approvals and decisions must be tracked and logged. Workflows must route administrative decisions to the designated 3(16) administrator.

---

## 3. ERISA Section 3(21): Investment Advisor (Co-Fiduciary)

- **Definition:** A co-fiduciary who renders investment advice for a fee; shares fiduciary responsibility with the plan sponsor but does not have sole discretion.
- **Responsibilities:** Provide prudent investment recommendations; disclose conflicts of interest; document advice.
- **Platform implication:** The platform must present investment recommendations for plan sponsor review and approval. **The platform cannot auto-implement a 3(21)'s recommendations without plan sponsor action.** Any feature that bypasses this approval step creates fiduciary risk. [COMPLIANCE-SENSITIVE]

---

## 4. ERISA Section 3(38): Investment Manager (Full Discretion)

- **Definition:** A fiduciary with full discretionary authority to manage, acquire, and dispose of plan assets. Must be an investment advisor registered under the Investment Advisers Act, a bank, or an insurance company.
- **Responsibilities:** Makes and implements investment decisions; relieves plan sponsor of liability for those decisions.
- **Platform implication:** When a 3(38) is appointed, the platform may implement investment changes directed by the 3(38) **without requiring additional plan sponsor approval**. Requirements must verify whether a 3(38) is in place before designing auto-implementation workflows. [COMPLIANCE-SENSITIVE]

---

## 5. The Prudent Expert Standard

ERISA Section 404(a) requires fiduciaries to act:
- Solely in the interest of participants and beneficiaries
- For the exclusive purpose of providing plan benefits and defraying reasonable plan expenses
- With the care, skill, prudence, and diligence that a **prudent expert** would use under the circumstances

### Platform Implications of the Prudent Expert Standard

| Obligation | Platform Requirement |
|---|---|
| **Audit trails** | Every fiduciary decision recorded on the platform must be logged with timestamp, actor identity, and action taken. Audit trails must be immutable. |
| **Disclosures** | Fee and investment disclosures are fiduciary obligations. The platform must generate, deliver, and track delivery of required disclosures. |
| **Approval workflows** | Workflows involving fiduciary decisions (investment changes, hardship approvals, QDRO qualification) must route to the appropriate fiduciary for review and approval before execution. |

---

## 6. ERISA Section 404(c): Participant-Directed Investments

ERISA Section 404(c) provides **fiduciary relief** to plan sponsors and other fiduciaries when participants exercise independent control over their investment accounts.

**Requirements for 404(c) protection:**
- Offer a broad range of investment alternatives (minimum: three diversified options with materially different risk and return characteristics)
- Allow participants to give investment instructions at least as frequently as market volatility requires, but no less than quarterly
- Provide participants with sufficient information to make informed investment decisions
- Implement participant investment instructions without undue delay

**Platform requirements supporting 404(c) compliance:**
- Investment change functionality must be available at the required frequency
- Participants must have access to investment information (prospectuses, fund fact sheets) through the platform
- Trade execution must occur within defined processing windows
- Confirmation of executed trades must be available to participants

---

## 7. ERISA Section 107: Record Retention

ERISA Section 107 requires all records necessary to determine the rights of any plan participant or beneficiary be retained for a minimum of six years from the date the document was filed (or certification due date). [DATE-VERIFY — confirm current retention standards at time of requirement writing]

**Platform implications:**
- The recordkeeping system must retain transaction-level records, plan documents, notices, and compliance data for the required period
- Data archiving and retrieval capabilities must support DOL audit requests and participant benefit claims
- Deletion or modification of historical records must be controlled and logged

---

## 8. Prohibited Transactions

Under ERISA Section 406, certain transactions between a plan and "parties in interest" are prohibited unless a statutory or DOL exemption applies. Common prohibited transactions relevant to platform design:
- A fiduciary dealing with plan assets in their own interest
- Extension of credit between the plan and a party in interest (except participant loans meeting IRC 72(p))
- Receipt of consideration by a fiduciary from a party dealing with the plan in a transaction involving plan assets

**Platform implication:** Revenue sharing arrangements, service provider fees, and any transactions between the plan and affiliated entities must be evaluated against prohibited transaction rules. ERISA Section 408(b)(2) provides an exemption for necessary services at reasonable compensation with adequate disclosure.

---

## 9. Fiduciary Responsibility Boundaries — Decision Matrix

| Action | Who Decides | Platform Role | Fiduciary Risk Flag |
|---|---|---|---|
| Investment menu selection (3(21) in place) | Plan sponsor (must approve advisor recommendations) | Present for approval; do not auto-implement | High — auto-implementation without approval is a fiduciary breach |
| Investment menu selection (3(38) in place) | 3(38) Investment Manager | May auto-implement upon 3(38) direction | Low if 3(38) properly appointed |
| Hardship withdrawal approval | Plan administrator (3(16)) | Route for approval; do not auto-approve | High — platform cannot substitute for fiduciary judgment |
| QDRO qualification | Plan administrator | Workflow support; [RECOMMEND LEGAL/COMPLIANCE REVIEW] | Very high — incorrect QDRO determination has legal consequences |
| RMD calculation and distribution | Platform (ministerial) | Automated calculation and processing | Moderate — calculation must be accurate; methodology must be documented |
| Contribution limit enforcement | Platform (ministerial) | Automated monitoring and stopping | Moderate — errors create compliance exposure |

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Tag all features that involve fiduciary decisions, investment changes, hardship approvals, or QDRO processing.
- **[RECOMMEND LEGAL/COMPLIANCE REVIEW]** — Tag all QDRO-related requirements and any features that could inadvertently create fiduciary status for the platform.
- Always verify 3(21) vs. 3(38) appointment status before designing any auto-implementation workflow for investment changes.
- Audit trail requirements are non-negotiable for all fiduciary actions — timestamp, actor identity, and action taken.
- Do not design platform features that substitute platform automation for required fiduciary judgment.

---

## Sources

- ERISA Sections 3(16), 3(21), 3(38), 404(a), 404(c), 406, 407, 107 | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DOL Field Assistance Bulletin 2003-3 (404(c)) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Resources on Fiduciary Standards | https://www.asppa.org | Retrieved 2026-03-06
