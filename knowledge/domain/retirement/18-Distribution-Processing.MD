# Skill: Distribution Processing
**Skill-ID:** 18-Distribution-Processing
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the mechanics of distribution processing — tax withholding rules, direct vs. indirect rollover elections, 1099-R generation, the 402(f) Special Tax Notice requirement, and source-level liquidation order. Distribution processing is among the most compliance-sensitive functions in the recordkeeping platform.

---

## 1. Eligible Rollover Distribution (ERD) vs. Non-ERD

The distinction between an eligible rollover distribution (ERD) and a non-ERD determines which tax withholding rules apply.

### Eligible Rollover Distribution (ERD)

A distribution from a qualified plan that is eligible to be rolled over to another eligible retirement plan or IRA.

**ERD includes:**
- Lump sum distributions at termination
- In-service distributions (age-based) that meet rollover eligibility rules
- Death distributions to spousal beneficiaries
- Loan offsets (including qualified plan loan offsets)

**ERD excludes (not eligible for rollover):**
- Required Minimum Distributions (RMDs)
- Hardship distributions
- Series of substantially equal periodic payments over 10+ years
- Corrective distributions of excess contributions
- Deemed distributions from loan defaults

**Tax withholding for ERDs:**
- **Mandatory 20% federal income tax withholding** applies to any ERD paid directly to the participant (not directly rolled over)
- Participant may elect to have additional withholding above the 20% mandatory amount
- The 20% mandatory withholding does NOT apply to amounts directly rolled over

### Non-ERD

Non-ERDs (hardship distributions, RMDs, periodic payments) have different withholding rules:
- Optional 10% withholding by default (participant may elect out or increase)
- No mandatory 20% withholding

[COMPLIANCE-SENSITIVE]

---

## 2. Direct vs. Indirect Rollover

### Direct Rollover

The distribution is paid directly from the plan to an eligible retirement plan or IRA. The participant never receives the funds.

**Key characteristics:**
- Mandatory 20% federal withholding does NOT apply
- No 60-day rollover deadline risk
- The full gross distribution amount is transferred, preserving full tax-deferred status

**Platform requirements:**
- Capture rollover destination (receiving institution name, account type, account number, ABA routing number)
- Generate the distribution check or wire payable to the receiving institution FBO the participant
- Record the rollover as a direct rollover distribution
- Generate 1099-R with the direct rollover distribution code

### Indirect Rollover

The distribution is paid to the participant in cash. The participant has 60 days to re-contribute the funds to an eligible retirement plan or IRA to avoid taxation.

**Key characteristics:**
- Mandatory 20% federal withholding applies to the gross distribution
- The participant must replace the 20% withheld from other funds to roll over the full gross amount; if only the net amount is contributed, the withheld 20% is taxable income
- Risk of failing the 60-day rollover deadline (results in taxable distribution)

**Platform requirements:**
- Apply mandatory 20% federal withholding
- Generate distribution check or ACH payable to the participant
- Provide written explanation of the 60-day rollover option and the withholding impact
- Generate 1099-R with the distribution amount and withholding amount

---

## 3. Tax Withholding — Federal

| Distribution Type | Withholding Rule | Participant Override |
|---|---|---|
| ERD — not directly rolled over | Mandatory 20% federal withholding | May elect additional withholding above 20%; may not waive |
| ERD — direct rollover | No withholding | N/A |
| Non-ERD (hardship, RMD) | Default 10% optional withholding | May opt out of withholding or increase |
| Non-U.S. resident (NRA) | 30% withholding (or treaty rate) | Per applicable treaty |

[COMPLIANCE-SENSITIVE]

---

## 4. Tax Withholding — State

State income tax withholding requirements vary by participant state of residence. Key rules:
- Some states have mandatory withholding on retirement plan distributions
- Some states follow the participant's withholding election (opt in/opt out)
- Some states have no income tax on retirement distributions
- State withholding defaults and mandatory rates are plan-configurable parameters per participant state of residence

**Platform requirements:**
- Maintain state withholding rules by state (updated at least annually for regulatory changes)
- Apply the correct state withholding treatment based on participant's state of residence at distribution
- Allow participant to elect state withholding within the applicable state rules
- Include state withholding on 1099-R

[COMPLIANCE-SENSITIVE]

---

## 5. 402(f) Special Tax Notice

The 402(f) Special Tax Notice is a mandatory disclosure that must be provided to the participant **before** any eligible rollover distribution is processed.

**Required content:**
- Right to a direct rollover
- Available eligible retirement plans and IRAs for rollover
- Mandatory 20% withholding if not directly rolled over
- Tax consequences of the distribution
- 10% early distribution penalty (and exceptions)
- State withholding rules (if applicable)
- Special rules for Roth and after-tax amounts
- SECURE Act changes to rollover rules (if applicable)

**Timing:**
- Must be provided no more than 180 days before the distribution, and no less than 30 days before the distribution
- Participant may waive the 30-day waiting period to receive the distribution sooner — waiver must be captured and logged
- [DATE-VERIFY — confirm current 402(f) notice timing requirements]

**Platform requirements:**
- Generate 402(f) notice when a distribution request is initiated that may result in an ERD
- Track the date the notice was provided
- Enforce the 30-day waiting period before processing, or capture participant waiver
- Log notice delivery confirmation

[COMPLIANCE-SENSITIVE]

---

## 6. Source Liquidation Order for Distributions

When a distribution is processed, the platform must liquidate the participant's account in the correct source order. The liquidation order is determined by the plan document and IRC rules:

**General principles:**
- Rollover balances are generally immediately distributable from any source at any time
- Elective deferrals (pre-tax, Roth) are generally distributable upon triggering events (termination, age, hardship, RMD)
- Employer match and non-elective sources require vesting — only the vested portion is distributable
- After-tax (non-Roth) amounts are generally distributable at any time

**Within each source:** Distributions are allocated pro-rata across investment funds (unless the plan document specifies otherwise).

---

## 7. 1099-R Generation

The plan must issue a Form 1099-R for each taxable distribution by the IRS deadline for the tax year of distribution.

**Key 1099-R fields:**
- Gross distribution amount
- Taxable amount
- Federal income tax withheld
- State income tax withheld (if applicable)
- Distribution code (determines tax treatment — must be accurate)

**Common distribution codes:**
| Code | Distribution Type |
|---|---|
| 1 | Early distribution, no known exception |
| 2 | Early distribution with exception |
| 4 | Death |
| 7 | Normal distribution (age 59½+) |
| B | Designated Roth account distribution |
| G | Direct rollover to qualified plan or IRA |
| H | Direct rollover from designated Roth to Roth IRA |
| L | Loans treated as deemed distributions |

**Platform requirements:**
- Generate 1099-R data for all distributions in the calendar year
- Apply the correct distribution code based on distribution type, participant age, and eligibility
- Include all required 1099-R fields
- Deliver 1099-R to participant by IRS deadline [DATE-VERIFY — confirm current 1099-R delivery deadline]
- File 1099-R data with IRS by IRS deadline [DATE-VERIFY]

[COMPLIANCE-SENSITIVE]

---

## 8. Distribution Settlement

After the distribution is approved and the 402(f) notice period satisfied:
1. Liquidate participant account in source and fund order
2. Apply tax withholding calculations
3. Generate payment (check, wire, ACH, or direct rollover wire)
4. Update participant account balances
5. Generate transaction records
6. Schedule 1099-R generation for year end

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — 402(f) Special Tax Notice is a prerequisite to distribution processing. No ERD may be initiated without confirmed notice delivery or participant waiver of the 30-day period.
- **[COMPLIANCE-SENSITIVE]** — Mandatory 20% federal withholding on non-direct-rollover ERDs cannot be waived by the participant. Failing to apply mandatory withholding creates IRS compliance exposure.
- **[COMPLIANCE-SENSITIVE]** — 1099-R distribution codes must be accurate. An incorrect code mis-represents the tax character of the distribution to the IRS and participant.
- State withholding rules must be maintained and updated as state laws change — these cannot be hardcoded.
- Direct rollover information must be captured accurately before processing — once funds are sent, reversing a rollover requires cooperation of the receiving institution.

---

## Sources

- IRC Sections 402(f), 3405 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- IRS Publication 575 (Pension and Annuity Income) | https://www.irs.gov/publications/p575 | Retrieved 2026-03-06
- DOL Regulation 29 CFR 1.402(f)-1 | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRS 1099-R Instructions | https://www.irs.gov/forms-pubs/about-form-1099-r | Retrieved 2026-03-06
