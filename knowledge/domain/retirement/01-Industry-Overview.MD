# Skill: Industry Overview
**Skill-ID:** 01-Industry-Overview
**World:** Retirement World v1.0
**Category:** Foundation
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill provides foundational knowledge of the U.S. retirement plan ecosystem — why it exists, how it is structured, what regulatory bodies govern it, and why precision in this domain is non-negotiable. Every other retirement skill builds on this foundation.

---

## 1. What the U.S. Retirement Ecosystem Is and Why It Exists

The U.S. retirement plan ecosystem is a framework of tax-advantaged savings vehicles established by Congress to encourage employer-sponsored and individual retirement saving. It is built on a **deferred-taxation model**: contributions and earnings grow tax-advantaged, with taxation deferred to distribution (or, for Roth accounts, contributed after-tax with tax-free qualified distributions).

The ecosystem exists because Social Security alone is insufficient to replace pre-retirement income. Tax incentives (employer deductions, participant tax deferral) are conditional — plans must satisfy qualification, nondiscrimination, and reporting requirements to maintain tax-advantaged status.

**Dual regulatory framework:**
- **DOL (Department of Labor / EBSA):** Oversees fiduciary conduct, participant rights, and plan administration under ERISA.
- **IRS:** Administers tax qualification rules under the Internal Revenue Code (IRC).

---

## 2. Spectrum of Plan Types

| Plan Type | Sponsoring Entity | Key Characteristic |
|---|---|---|
| **401(k)** | Private-sector employer | Elective deferrals; most common DC plan |
| **403(b)** | Public schools, 501(c)(3) orgs | Similar to 401(k); ERISA status arrangement-dependent |
| **457(b) Governmental** | State/local governments | Non-ERISA; limits run independently |
| **457(b) Tax-Exempt** | Non-governmental tax-exempt orgs | ERISA; top-hat rules may apply |
| **457(f)** | Tax-exempt employers | Ineligible plan; substantial risk of forfeiture |
| **SIMPLE IRA** | Small employers | Simplified matching; lighter admin burden |
| **SEP IRA** | Any employer/self-employed | Employer-only contributions; no employee deferrals |
| **Roth 401(k)/403(b)** | Same as above | Designated Roth after-tax within qualified plan |
| **Safe Harbor 401(k)** | Private-sector employer | Satisfies ADP/ACP via required employer contributions |
| **PEP / MEP** | Pooled Plan Provider / group | Multiple unrelated employers in one plan structure |

---

## 3. ERISA vs. Non-ERISA Plans

**ERISA applicability is arrangement-dependent, not plan-type-dependent.**

| Category | ERISA Status | Notes |
|---|---|---|
| Private-sector employer-sponsored | Subject to ERISA | Default for most 401(k)/403(b) plans |
| Governmental plans (457(b) govt) | NOT subject to ERISA | State/local government employers |
| Church plans | Generally NOT subject to ERISA | May elect ERISA coverage |
| Top-hat plans | Exempt from most ERISA substantive provisions | Subject to reporting only |
| 403(b) with minimal employer involvement | May qualify as non-ERISA voluntary plan | Must meet DOL safe harbor criteria |

**Agent rule:** Never assume ERISA or non-ERISA status based on plan type alone. Verify the arrangement. Tag all government plan requirements **[GOVERNMENT PLAN — NON-ERISA]**.

---

## 4. Defined Contribution vs. Defined Benefit

| Dimension | Defined Contribution (DC) | Defined Benefit (DB) |
|---|---|---|
| Promise to participant | Account balance (contributions + returns) | Specified monthly benefit at retirement |
| Investment risk | Borne by participant | Borne by employer/plan |
| Actuarial complexity | Not required | Required for funding calculations |
| Portability | High | Lower — tied to service credit formulas |
| CORE platform scope | **In scope** | **Out of scope** |

CORE is a DC-focused recordkeeping platform. DB actuarial calculations, pension benefit formulas, and annuity valuation are out of scope unless explicitly added.

---

## 5. Bundled vs. Unbundled Service Models

**Bundled:** Single provider delivers recordkeeping, investment platform, and plan administration under one contract. Tighter integration, less flexibility.

**Unbundled:** Separate providers fill each role — recordkeeper, TPA, investment platform, custodian, and advisor are distinct entities. Requires robust data exchange standards, reconciliation workflows, and multi-party coordination.

CORE operates in both models. Requirements must specify which service model a given feature targets.

---

## 6. Why Precision Matters at Scale

The U.S. defined contribution market holds trillions of dollars across tens of millions of participants. A single payroll processing error affecting thousands of participants simultaneously illustrates why:
- Minor rounding differences aggregate into significant compliance exposure at scale
- Every requirement must account for edge cases, compliance flags, and audit trail obligations
- Errors in contribution limits, vesting, or distribution eligibility can trigger plan disqualification

---

## Agent Rules for This Domain

- **Never hardcode** annual dollar limits, compensation thresholds, or percentage caps — always reference as plan-configurable parameters sourced from IRS limit tables.
- **Tag compliance-sensitive** requirements: **[COMPLIANCE-SENSITIVE]**
- **Tag government plans:** **[GOVERNMENT PLAN — NON-ERISA]**
- **Tag unverified dates:** **[DATE-VERIFY]**
- DB actuarial scope — if a request touches DB pension formulas, flag and escalate.

---

## Sources

- U.S. Department of Labor, EBSA | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRS Retirement Plans | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- ERISA (P.L. 93-406, as amended) | https://www.dol.gov/general/topic/retirement/erisa | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 (P.L. 117-328) | https://www.congress.gov/bill/117th-congress/house-bill/2954 | Retrieved 2026-03-06
