# Skill: Plan Types and Structures
**Skill-ID:** 02-Plan-Types
**World:** Retirement World v1.0
**Category:** Foundation
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines every retirement plan type the CORE platform may encounter. Each entry covers structure, sponsoring entity, ERISA status, architectural distinctions, and agent flags. Requirement writers must correctly identify the plan type before writing any scope.

---

## 1. 401(k)

**Structure:** Qualified cash or deferred arrangement (CODA) under IRC Section 401(k), part of a profit-sharing or stock bonus plan. Employees elect to defer compensation on a pre-tax (Traditional) or after-tax (Roth) basis. Employers may contribute matching or non-elective (profit sharing) contributions.

**Who uses it:** Private-sector for-profit employers of all sizes. The most prevalent DC plan type in the U.S.

**ERISA applicability:** Subject to ERISA (private-sector employer plans). Governmental 401(k) plans are rare — flag **[GOVERNMENT PLAN — NON-ERISA]** if encountered.

**Architectural distinctions:**
- Multiple contribution sources (employee pre-tax, Roth, employer match, employer non-elective, rollover) each with distinct vesting schedules
- Requires ADP/ACP nondiscrimination testing unless safe harbor provisions are satisfied
- Supports auto-enrollment, auto-escalation, and Roth in-plan conversion

**Agents must flag:** Contribution source segregation; annual nondiscrimination testing requirements; safe harbor election status; Roth in-plan conversion capability; auto-enrollment and auto-escalation provisions.

---

## 2. 403(b)

**Structure:** Tax-sheltered annuity plan under IRC Section 403(b). Available to employees of public schools, colleges, universities, and 501(c)(3) tax-exempt organizations. Functionally similar to a 401(k) in contribution mechanics.

**Who uses it:** Educational institutions, hospitals, charities, religious organizations.

**ERISA applicability:** ARRANGEMENT-DEPENDENT — never assume based on plan type alone.
- Public school district 403(b) = governmental plan, non-ERISA
- Private nonprofit hospital 403(b) = may be ERISA-covered
- 403(b) with minimal employer involvement meeting DOL safe harbor = may be non-ERISA even for private employer

**Universal Availability Rule:** Under IRC Section 403(b)(12), all employees must be permitted to make elective deferrals unless specifically excluded by statute. Permitted exclusion classes differ from 401(k). Platform eligibility logic must support Universal Availability Rule compliance. [COMPLIANCE-SENSITIVE]

**Architectural distinctions:**
- May include both annuity contracts and custodial accounts
- Legacy 403(b) plans may have individual annuity contracts not held in a plan trust (reconciliation complexity)
- Pre-2009 grandfathered contracts may exist outside the plan document framework

**Agents must flag:** ERISA status; Universal Availability Rule eligibility logic; contract vs. custodial account structure; pre-2009 grandfathered contracts.

---

## 3. 457(b) Governmental

**Structure:** Deferred compensation plan under IRC Section 457(b) maintained by a state or local government or agency/instrumentality. Employee deferrals reduce current taxable income. Assets must be held in trust for the exclusive benefit of participants (post-1999 requirement). [DATE-VERIFY]

**Who uses it:** State and local governments, public school districts, municipalities.

**ERISA applicability:** NOT subject to ERISA. Tag all requirements: **[GOVERNMENT PLAN — NON-ERISA]**

**Key distinction:** Contribution limits for 457(b) governmental plans run independently — a participant employed by both a governmental and a private employer may contribute the maximum to both a 457(b) governmental plan AND a 401(k)/403(b) simultaneously (plan-configurable parameter per IRS rules).

**Agents must flag:** Non-ERISA status throughout; no ERISA prohibited transaction rules apply; trust requirement post-1999; distinct RMD and distribution rules.

---

## 4. 457(b) Tax-Exempt

**Structure:** Maintained by non-governmental tax-exempt organizations (e.g., hospitals, nonprofits). Assets remain general assets of the employer — participants bear employer solvency risk. Subject to ERISA as a top-hat plan if limited to select management or HCEs.

**Key distinction from 457(b) governmental:** No trust requirement. Assets are unsecured general employer assets. Participants bear default risk.

**Agents must flag:** Employer solvency risk; top-hat plan ERISA exemption applicability; unfunded plan architecture.

---

## 5. 457(f)

**Structure:** "Ineligible" deferred compensation arrangement for tax-exempt employers that exceeds 457(b) limits. Deferred amounts subject to a substantial risk of forfeiture; taxation triggered when forfeiture risk lapses. Generally unfunded. [NEEDS-VALIDATION — confirm current IRC 457(f) treatment and platform applicability]

**Agents must flag:** Substantial risk of forfeiture timing; different tax treatment from 457(b); unfunded plan architecture; specialized recordkeeping.

---

## 6. SIMPLE IRA

**Structure:** Savings Incentive Match Plan for Employees under IRC Section 408(p). Each participant maintains an individual IRA. Employer must make either matching contributions or a fixed non-elective contribution (plan-configurable per IRS rules).

**Who uses it:** Small employers meeting eligible employer criteria (plan-configurable size threshold per IRS rules) seeking low-cost retirement savings with minimal administrative burden.

**ERISA applicability:** Generally subject to ERISA for private-sector employers unless DOL voluntary plan safe harbor applies.

**Architectural distinction:** No trust — contributions go directly to individual IRAs at a financial institution. The IRA custodian holds assets, not a plan trustee. Two-year rule restricts participants from rolling out SIMPLE IRA assets during the first two years of participation.

**Agents must flag:** IRA-based architecture (not trust-based); employer eligibility threshold (plan-configurable per IRS rules); two-year transfer restriction; SIMPLE IRA vs. SIMPLE 401(k) distinction (SIMPLE 401(k) is trust-based); no loans permitted from SIMPLE IRAs.

---

## 7. SEP IRA

**Structure:** Simplified Employee Pension under IRC Section 408(k). Employer-only contributions to individual employee IRAs. No employee salary deferral permitted (except in legacy SARSEP arrangements grandfathered prior to 1997).

**Who uses it:** Self-employed individuals, small employers seeking minimal administrative burden.

**ERISA applicability:** Subject to ERISA if maintained by a private-sector employer (administrative requirements minimal); DOL safe harbor for IRAs may apply.

**Architectural distinction:** No trust. Employer contributes directly to participant IRAs. Contribution formula is uniform percentage of compensation for all eligible employees.

**Agents must flag:** No employee deferrals in current SEP IRA; SARSEP grandfathering for pre-1997 plans; IRA-based architecture; no loans.

---

## 8. Safe Harbor 401(k)

**Structure:** A 401(k) plan that satisfies ADP and/or ACP testing by making specified employer contributions and providing required notices. In exchange, the plan is deemed to pass ADP and ACP tests.

**Traditional Safe Harbor vs. QACA:**

| Dimension | Traditional Safe Harbor | QACA |
|---|---|---|
| Auto-enrollment required | No | Yes — at minimum default deferral rate |
| Required employer contribution | Matching or non-elective per IRS safe harbor formulas | Matching or non-elective per QACA requirements |
| Vesting | Immediate for safe harbor contributions | Up to 2-year cliff vesting for safe harbor contributions |
| ADP/ACP relief | Eliminates ADP; may eliminate ACP | Same |

**Agents must flag:** Safe harbor notice requirement (annual, before plan year start); mid-year amendment restrictions; QACA auto-enrollment and auto-escalation requirements; vesting schedule distinction between Traditional and QACA safe harbor.

---

## 9. Pooled Employer Plans (PEPs) and Multiple Employer Plans (MEPs)

**MEP (Multiple Employer Plan):** Two or more unrelated employers in a single plan with one Form 5500 filing. Historically subject to "one bad apple" rule (one employer's violation could disqualify the entire plan) — modified by SECURE 2.0 and prior legislation.

**PEP (Pooled Employer Plan):** Created by SECURE Act of 2019. A type of MEP operated by a registered Pooled Plan Provider (PPP). The PPP is the named plan administrator and a named fiduciary. Each employer adopts via a participation agreement. Dramatically reduces plan sponsor administrative burden and fiduciary liability.

**Architectural distinction:** Both MEP and PEP structures require multi-employer data management — each employer has its own contribution rules, payroll data, and potentially its own plan design parameters. The recordkeeping platform must support employer-level segmentation within a single plan.

**Agents must flag:** PPP registration requirement for PEPs; employer-level plan design parameterization; multi-EIN data structure; one bad apple rule applicability for MEPs; Form 5500 filing at plan level (not employer level).

---

## 10. Starter 401(k) (SECURE 2.0) [DATE-VERIFY]

**Structure:** New plan type created by SECURE 2.0 for employers that do not sponsor any other retirement plan. Simplified 401(k) with mandatory auto-enrollment, no employer contribution requirement, and reduced nondiscrimination testing burden.

**Who uses it:** Small employers with no existing plan — designed as a low-friction entry point.

**Agents must flag:** [DATE-VERIFY — confirm effective date and feature requirements before writing scope]; verify which compliance tests are waived; auto-enrollment default parameters per IRS guidance.

---

## Key Cross-Plan Rules

- **Never hardcode** plan type characteristics — always verify the specific plan document and adoption agreement.
- **ERISA status** must be determined by arrangement, not plan type.
- **Contribution limits** are always plan-configurable parameters sourced from current IRS limit tables.
- **403(b) Universal Availability** logic is distinct from 401(k) eligibility — do not copy 401(k) eligibility rules to 403(b) without adjustment.

---

## Sources

- IRC Sections 401(k), 403(b), 408, 457 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL 403(b) Regulations (2007) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SECURE Act of 2019 (P.L. 116-94); SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov | Retrieved 2026-03-06
- ASPPA Plan Types Reference | https://www.asppa.org | Retrieved 2026-03-06
