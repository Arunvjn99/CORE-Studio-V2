# Skill: Hardship and In-Service Withdrawals
**Skill-ID:** 16-Hardship-and-In-Service-Withdrawals
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill covers all forms of in-service distributions — hardship withdrawals, SECURE 2.0 emergency distributions, domestic abuse distributions, PLESA withdrawals, and age-based in-service withdrawals. These distributions occur while the participant is still employed and are subject to specific eligibility criteria, self-certification requirements, and tax treatment.

---

## 1. Hardship Withdrawals

### Qualifying Conditions

A hardship distribution is permissible for an immediate and heavy financial need that cannot be reasonably met from other available resources. Under IRS safe harbor rules, qualifying hardship reasons include:

- Medical expenses (participant, spouse, dependents, or plan beneficiary)
- Purchase of a principal residence (not mortgage payments)
- Payment of post-secondary education expenses (tuition, fees, room, board — plan-configurable covered expenses)
- Prevention of eviction from or foreclosure on principal residence
- Funeral or burial expenses (participant, spouse, dependents, or plan beneficiary)
- Casualty loss on principal residence (Federally declared disaster)
- **SECURE 2.0 additions:**
  - Emergency personal or family expenses (see Section 2 below)
  - Domestic abuse expenses (see Section 3 below)

The plan document must specify which hardship reasons are permitted.

### Self-Certification Workflow (SECURE 2.0)

[DATE-VERIFY — confirm effective date for self-certification rules]

SECURE 2.0 simplified hardship verification by allowing plans to rely on participant self-certification for:
- The existence of a qualifying hardship
- The unavailability of other reasonably available resources to meet the need

The plan may accept the participant's written certification without requiring third-party documentation (e.g., medical bills, letters from lenders). However, the plan should retain the self-certification record.

**Platform requirements:**
- Self-certification workflow with required attestation fields (nature of hardship, amount needed, certification that other resources are unavailable)
- Document retention of self-certification for audit trail
- Plan sponsor may retain the right to require documentation — support both documentation and self-certification workflows per plan design
- Flag hardship request for plan sponsor or 3(16) administrator review if plan requires approval

### Distribution Amount

The amount of a hardship distribution is limited to:
- The amount necessary to satisfy the immediate financial need, including estimated taxes and penalties
- The participant's available vested account balance in hardship-eligible sources

**Eligible sources for hardship:** Plan-configurable. Generally, elective deferrals (pre-tax and Roth) and rollover balances. Earnings on 401(k) elective deferrals may not be available for hardship in some cases depending on when the plan was established. [DATE-VERIFY]

**Tax treatment:**
- Subject to ordinary income tax
- Subject to 10% early distribution penalty unless an exception applies (e.g., age 59½)
- Subject to mandatory 20% federal withholding if an eligible rollover distribution; however, hardship distributions are generally NOT eligible rollover distributions (20% mandatory withholding does not apply; 10% optional withholding may apply)

[COMPLIANCE-SENSITIVE]

### Six-Month Suspension (Pre-SECURE 2.0)

Prior to SECURE 2.0, plans were required to suspend participant contributions for 6 months following a hardship distribution. **SECURE 2.0 eliminated the mandatory 6-month suspension.** [DATE-VERIFY — confirm complete elimination]

---

## 2. Emergency Expense Distributions (SECURE 2.0)

[DATE-VERIFY — confirm effective date]

Plans may permit a distribution for personal or family emergency expenses without meeting the traditional hardship criteria.

**Key rules:**
- One distribution per year (resets if prior distribution was repaid)
- Maximum distribution amount: plan-configurable per IRS rules — do not hardcode
- Participant self-certification is the sole verification required
- Early distribution penalty waived
- Repayment: participant may repay within 3 years; repaid amounts are treated as rollover contributions
- If not repaid, no further emergency expense distribution is permitted until the 3-year window closes (unless the one-per-year limit resets sooner)

**Platform requirements:**
- New distribution type: Emergency Expense
- One-per-year limit enforcement (with reset logic for repaid distributions)
- Repayment tracking (3-year window; credit repayments back to account)
- Self-certification attestation workflow
- 1099-R with appropriate distribution code (penalty waiver)
- Do not hardcode the distribution limit

[COMPLIANCE-SENSITIVE]

---

## 3. Domestic Abuse Distributions (SECURE 2.0)

[DATE-VERIFY — confirm effective date]

Plans may permit distributions to participants who self-certify as victims of domestic abuse.

**Key rules:**
- Maximum distribution amount: plan-configurable per IRS rules — do not hardcode
- Participant self-certification required (platform relies on attestation; no independent verification required)
- Early distribution penalty waived
- Repayment: participant may repay within 3 years; repaid amounts treated as rollover contributions
- Income tax applies in the year of distribution; no penalty

**Platform requirements:**
- New distribution type: Domestic Abuse
- Self-certification workflow (sensitive — protect participant privacy in the workflow design)
- Repayment tracking (3-year window)
- 1099-R with appropriate distribution code (penalty waiver)
- Do not hardcode the distribution limit

[COMPLIANCE-SENSITIVE]

---

## 4. PLESA Withdrawals (SECURE 2.0)

[DATE-VERIFY — confirm effective date]

Pension-Linked Emergency Savings Accounts (PLESAs) are short-term savings accounts linked to DC plans. PLESA balances may be withdrawn at any time without penalty.

**Key rules:**
- Only non-HCE participants may contribute to PLESAs
- PLESA balances are after-tax; withdrawals are not subject to tax on return of basis
- Withdrawal frequency may be limited (plan-configurable per IRS rules — do not hardcode frequency restriction)
- PLESA balances interact with employer match formulas if the plan treats PLESA contributions as deferrals for match purposes (plan-configurable)

**Platform requirements:**
- PLESA withdrawals processed without early distribution penalty
- Maintain after-tax basis tracking for PLESA balances
- Apply plan-configured withdrawal frequency limit
- If match is paid on PLESA contributions, ensure match source interaction is correctly configured

[COMPLIANCE-SENSITIVE]

---

## 5. Age-Based In-Service Withdrawals

Plans may permit in-service withdrawals after a participant reaches a plan-configured age.

**Key rules:**
- Minimum age for in-service withdrawals is a plan-configurable parameter subject to IRC minimums
- The withdrawal is an eligible rollover distribution — subject to 402(f) notice requirement and participant's right to a direct rollover
- Mandatory 20% federal withholding applies unless directly rolled over
- Not subject to 10% early distribution penalty if the participant has reached age 59½

**Platform requirements:**
- Verify participant age against the plan-configured in-service age threshold
- Identify the withdrawal as an eligible rollover distribution
- Generate 402(f) Special Tax Notice before processing
- Offer direct rollover option
- Apply mandatory 20% withholding if not directly rolled over

---

## 6. Source Restrictions on In-Service Distributions

Not all contribution sources are available for in-service distributions. The availability of each source for in-service withdrawal depends on the plan document and IRC rules:

| Source | In-Service Withdrawal Availability |
|---|---|
| Elective deferrals (pre-tax, Roth) | Available for hardship; available after age 59½ (or other plan-configured age) |
| Employer match | Generally not available before age 59½ unless plan permits; subject to vesting |
| Employer non-elective / profit sharing | Available if participant has met the plan-configured in-service age; subject to vesting |
| Rollover | Generally available at any time (plan-configurable) |
| After-tax (non-Roth) | Generally available at any time (plan-configurable) |
| PLESA | Available at any time without penalty |

---

## 7. Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Tax withholding rules differ by distribution type. Hardship distributions are generally not ERDs (no mandatory 20% withholding). Age-based in-service withdrawals are ERDs (mandatory 20% withholding applies unless directly rolled over).
- **[COMPLIANCE-SENSITIVE]** — Self-certification documentation must be retained for audit trail. SECURE 2.0 allows reliance on self-certification but does not eliminate the record retention obligation.
- Never hardcode distribution limits for emergency expense or domestic abuse distributions — plan-configurable per IRS rules.
- Source eligibility for hardship and in-service withdrawals must trace to the plan document — do not assume all sources are available.
- SECURE 2.0 eliminated the mandatory 6-month contribution suspension after hardship — [DATE-VERIFY] before writing any requirement that references this suspension.

---

## Sources

- IRC Section 401(k)(2)(B) (Hardship) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- IRS Revenue Procedure 2019-19 (Hardship Safe Harbor) | https://www.irs.gov | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 — Emergency Expense, Domestic Abuse, PLESA provisions | https://www.congress.gov | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
