# Skill: Termination of Employment
**Skill-ID:** 17-Termination-of-Employment
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill covers all platform workflows triggered when a participant terminates employment — vesting finalization, force-out processing, auto-rollover IRA mechanics, deferred vested participant tracking, and required notifications. Termination triggers a cascade of time-sensitive processes.

---

## 1. Termination Event — Data Requirements

Termination of employment must be reflected in the participant record before termination workflows can begin. The platform requires:
- Termination date (from payroll or census file)
- Reason for termination (voluntary, involuntary, retirement, disability, death — each may trigger different workflows)
- Final payroll data (last paycheck, any final contributions)

**Platform requirements:**
- Update participant employment status to "Terminated" upon receiving termination data
- Retain termination date for vesting service finalization
- Flag the participant record for termination workflow processing
- Ensure final payroll contributions are processed before vesting finalization

---

## 2. Vesting Finalization

Upon termination, the participant's vested percentage in each employer contribution source is finalized based on years of vesting service completed as of the termination date.

**Process:**
1. Calculate total years of vesting service through the termination date (using the plan's service calculation method: hours or elapsed time)
2. Apply the vesting schedule for each employer source to determine the vested percentage
3. Calculate the vested balance for each source = balance × vested percentage
4. Calculate the unvested balance for each source = balance − vested balance
5. Post unvested balances to the forfeiture account

**Platform requirements:**
- Run vesting finalization for each employer contribution source separately (different sources may have different schedules)
- Apply the correct vesting schedule version (if the plan amended its schedule, determine which version applies to which service years)
- Post forfeitures to the plan-level forfeiture account with full audit trail
- Update the participant record with final vested percentage and vested balance

---

## 3. Force-Out Distribution Processing

For terminated participants with small balances, the plan may distribute the account balance without the participant's consent (force-out).

### Force-Out Threshold Tiers

| Balance Range | Plan's Action |
|---|---|
| Below mandatory distribution threshold | Plan may distribute the balance without participant consent (force-out permitted) |
| Above mandatory threshold but below consent threshold | Plan must obtain participant consent before distributing |
| Above mandatory rollover threshold | If the participant does not elect otherwise, the plan must roll the balance to an auto-rollover IRA |

All dollar thresholds are **plan-configurable per IRS rules** — never hardcode. [DATE-VERIFY — confirm current IRS mandatory distribution thresholds]

### Mandatory Rollover IRA (Auto-Rollover)

For balances above the mandatory distribution threshold but below the plan-configured mandatory rollover threshold:
- The plan must roll over the distribution to an IRA on the participant's behalf if the participant does not affirmatively elect otherwise
- The plan sponsor or TPA selects an IRA provider for auto-rollover IRAs
- The auto-rollover IRA must be invested in a low-risk investment option per DOL safe harbor standards

[COMPLIANCE-SENSITIVE]

**Platform requirements:**
- Monitor terminated participant balances against force-out thresholds
- Generate force-out notification to participant with distribution options and deadline
- If participant does not respond within the plan-configured window, initiate force-out or auto-rollover processing
- For auto-rollover: submit rollover to the plan-designated IRA provider with participant identifying information
- Log all force-out processing with full audit trail

---

## 4. Distribution Options for Terminated Participants

Terminated participants with vested balances above the consent threshold may choose among distribution options (plan-configurable; must include at minimum all options required by ERISA):
- **Lump sum distribution** — full vested balance paid in cash; subject to mandatory 20% withholding if ERD
- **Direct rollover** — full or partial balance rolled directly to an eligible retirement plan or IRA; no mandatory withholding
- **Deferred distribution** — participant leaves the balance in the plan (deferred vested participant) for future distribution
- **Installments** — if the plan permits, periodic payments over a specified period

**Platform requirements:**
- Present all available distribution options based on the participant's vested balance and plan design
- Generate 402(f) Special Tax Notice before processing any eligible rollover distribution
- Capture rollover election and rollover destination information for direct rollovers
- Apply mandatory 20% withholding for non-direct-rollover distributions (subject to participant's optional withholding election for amounts above the mandatory minimum)
- Generate 1099-R at tax year end

---

## 5. Deferred Vested Participant Tracking

Participants who terminate with a vested balance but do not take a distribution are **deferred vested participants**. The plan must continue to maintain their account.

**Ongoing obligations for deferred vested participants:**
- Continue to track account balance and apply investment activity (daily valuation)
- Apply any future vesting changes (if rehire occurs before permanent break in service)
- Process RMDs when the participant reaches the required beginning date
- Respond to participant-initiated distribution requests at any time
- Deliver required notices (annual fee disclosures, statements)
- Report to DOL Lost and Found database (SECURE 2.0, when effective) [DATE-VERIFY]

**Platform requirements:**
- Flag terminated participant records as "Deferred Vested"
- Include deferred vested participants in daily valuation and investment processing
- Monitor deferred vested participants for RMD triggering events
- Generate annual participant statements for deferred vested participants

---

## 6. Required Notifications at Termination

The platform must generate and deliver to the terminating participant:
- **Distribution election notice** — options available, deadlines, and consequences of each choice
- **402(f) Special Tax Notice** — if any eligible rollover distribution is being processed
- **COBRA notice** — (outside plan scope; coordinate with employer HR system)
- **Loan repayment notice** — if outstanding loan balance (see Skill 15)
- **Summary of vested balance** — by source, showing vested and unvested amounts

---

## 7. Loan Handling at Termination

If the participant has an outstanding loan balance at termination, see Skill 15 (Loan Administration) for loan offset rules and the SECURE 2.0 extended rollover deadline for qualified plan loan offsets.

---

## 8. Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Auto-rollover processing must comply with DOL safe harbor requirements for mandatory rollovers. Failure to follow the safe harbor process exposes the plan to fiduciary liability.
- **[COMPLIANCE-SENSITIVE]** — Force-out thresholds are IRS-indexed and plan-configurable — never hardcode. Distributing without consent below the threshold is a participant rights violation; failing to distribute when required is a plan operational failure.
- **[EDGE CASE]** — Termination immediately followed by rehire requires careful handling of vesting finalization vs. service restoration. Flag for explicit acceptance criteria.
- Vesting finalization must run per source — different employer sources may have different vesting schedules. Running a single vesting calculation for the whole account is incorrect.
- 402(f) Special Tax Notice is required before processing any eligible rollover distribution — this includes lump sum distributions to terminated participants.

---

## Sources

- IRC Sections 401(a)(11), 402(f), 411 | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL Regulation 29 CFR 2550.404a-2 (Auto-Rollover Safe Harbor) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SECURE 2.0 Act of 2022 — Force-Out Threshold, DOL Lost and Found | https://www.congress.gov | Retrieved 2026-03-06
- ERISA Sections 203, 205 | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
