# Skill: Investment Management
**Skill-ID:** 14-Investment-Management
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the participant investment management lifecycle — how participants change fund elections, how balances are rebalanced, how blackout periods are managed, and what ERISA Section 404(c) requires to protect plan fiduciaries. Investment management is a high-frequency, high-volume function in any recordkeeping platform.

---

## 1. Investment Election Types

Participants manage two distinct layers of investment elections:

### Future Contributions Allocation

Determines how new contributions (employee deferrals, employer match, non-elective) are allocated across available funds in percentage terms. This election is applied going forward and does not affect existing balances.

### Existing Balance Reallocation (Fund-to-Fund Transfer)

Transfers existing account balances from one or more funds to other funds. May be applied to the total account, a specific source, or a specific dollar or percentage amount.

**Platform requirements:**
- Separate UI/workflow paths for future contributions vs. existing balance transfers
- Both types of elections processed within the plan's trade execution window
- Investment elections apply across all sources unless the plan permits source-level elections

---

## 2. Fund Election Changes — Processing Rules

**Submission window:** Most daily-valued plans have a cut-off time for investment change submissions (e.g., 4:00 PM ET). Transactions submitted before the cut-off are processed at that day's end-of-day NAV. Transactions submitted after the cut-off are processed the next business day.

**Trading restrictions:**
- Fund-level restrictions (e.g., short-term redemption fees, excessive trading policies) must be enforced
- Stable value funds may have restrictions on transfers to competing fixed-income options
- Target-date funds may have specific rebalancing policies

**Platform requirements:**
- Enforce the plan's and fund's trading cut-off times
- Apply fund-level trading restrictions
- Confirm election changes to participants
- Aggregate net fund flows across all participant transactions and submit to custodian as net trade instructions

---

## 3. Rebalancing

Rebalancing restores a participant's account to their target asset allocation when it has drifted due to differential investment returns.

### Periodic Rebalancing

The participant's account is rebalanced to their target allocation on a plan-configured schedule (e.g., quarterly, semi-annually, annually). The system automatically generates the rebalancing trades without participant action.

### Threshold-Based Rebalancing

Rebalancing is triggered when any fund's allocation drifts by more than a plan-configured threshold percentage from the target allocation (e.g., if a fund target is 20% but the actual is now 25%, a 5% drift triggers rebalancing).

**Platform requirements:**
- Configure rebalancing type, frequency, and threshold per participant election or plan default
- Run rebalancing engine on the configured schedule or upon drift detection
- Generate rebalancing trades and submit to custodian within the plan's trade execution window
- Confirm rebalancing execution to participants
- Allow participants to opt in/out of automatic rebalancing (plan-configurable feature)

---

## 4. Blackout Periods

A **blackout period** is a period during which participant rights to direct investments, obtain loans, or take distributions are temporarily suspended.

**Common triggers:**
- Plan conversion to a new recordkeeper
- Fund mapping changes (replacing one fund with another on the investment menu)
- Trust/custodian transition
- System maintenance (short-duration blackouts)

### Notice Requirements (ERISA Section 101(i))

Participants must receive advance notice of a blackout period before it begins. [DATE-VERIFY — confirm current minimum notice period, generally at least 30 days]

**Exceptions:** The notice requirement may be shortened or waived in certain extraordinary circumstances outside the plan's control. [DATE-VERIFY — confirm current exception standards]

**Plan insider trading restriction:** Directors, officers, and 10%-or-greater shareholders of publicly-traded company sponsors may not trade in company stock during a blackout period covering the plan's company stock fund. The recordkeeper must maintain accurate blackout dates for insider trading compliance.

**Platform requirements:**
- Restrict participant investment transactions (transfers, elections, loans, distributions) during the blackout period
- Generate blackout notice at blackout period setup; enforce minimum notice period; track delivery
- Log blackout start and end dates with precision
- Allow only administrative transactions during blackout (e.g., processing pending contributions to a default fund)
- Provide a mechanism to extend or shorten a blackout period with appropriate notification

[COMPLIANCE-SENSITIVE]

---

## 5. Fund Mapping Changes

When a fund is removed from the investment menu and replaced with a new fund (fund substitution), the platform must:
- Create a mapping from the old fund to the new fund
- Transfer all participant balances in the old fund to the mapped new fund
- Update participant future contribution allocations to redirect from old to new fund
- Apply a blackout period (if needed) during the mapping process
- Generate required notices to participants (blackout notice and information about the new fund)
- Notify the plan sponsor or 3(38) of the completed mapping

---

## 6. QDIA Re-Enrollment

The plan sponsor may conduct a QDIA re-enrollment — a sweep that moves participants who have never made affirmative investment elections (or all participants, if the plan design allows) into the plan's QDIA.

**Platform requirements:**
- Identify participants meeting the re-enrollment criteria (no affirmative election, or all participants per plan design)
- Generate required notice to participants with advance opportunity to opt out or make an affirmative election
- Apply opt-out elections before the sweep date
- Move balances to QDIA for participants who did not opt out
- Update future contribution elections to QDIA for affected participants
- Log the re-enrollment event with participant-level detail

---

## 7. ERISA Section 404(c) Compliance Support

ERISA Section 404(c) provides fiduciary relief when participants exercise independent control over their investments. The platform supports 404(c) compliance by:

| 404(c) Requirement | Platform Support |
|---|---|
| Broad range of investment options (minimum 3 diversified) | Investment menu configuration enforces minimum options |
| Investment direction at least quarterly | Investment election change functionality available continuously |
| Sufficient information for informed decisions | Fund fact sheets, prospectuses, and performance data accessible in participant portal |
| Trade execution without undue delay | Same-day processing for elections submitted before cut-off |
| Confirmation of executed trades | Trade confirmations available to participants in transaction history |

[COMPLIANCE-SENSITIVE]

---

## 8. Revenue Sharing and Fee Tracking

Investment managers may pay revenue sharing (12b-1 fees, sub-TA fees) to the recordkeeper based on plan assets in their funds. Under ERISA fee disclosure rules:
- Revenue sharing rates must be disclosed to plan fiduciaries under 408(b)(2)
- Revenue sharing amounts must be disclosed to participants under 404(a)(5) fee disclosures
- Revenue sharing may be applied to offset plan expenses, credited to participant accounts, or used per the plan's revenue sharing policy

**Platform requirements:**
- Track revenue sharing rates per fund
- Calculate and apply revenue sharing credits per plan policy
- Include revenue sharing data in fee disclosure reports

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Blackout period notices are mandatory under ERISA 101(i). Failure to deliver advance notice is a violation.
- **[COMPLIANCE-SENSITIVE]** — The platform must not restrict participant investment direction beyond what blackout period rules permit. 404(c) protection requires that participants can exercise investment control.
- Never bypass the fund trading cut-off or fund-level restrictions. Trading restriction enforcement is required for both regulatory and fund compliance reasons.
- 3(21) vs. 3(38) status must be verified before designing fund substitution or investment menu change workflows — see Skill 04.
- Blackout period dates must be precisely recorded for insider trading compliance purposes.

---

## Sources

- ERISA Section 101(i) (Blackout Notice) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ERISA Section 404(c) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DOL Regulation 29 CFR 2550.404c-1 | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- DOL Regulation 29 CFR 2520.101-3 (Blackout Notice Regulation) | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SEC Rule 22c-2 (Shareholder data reporting) | https://www.sec.gov | Retrieved 2026-03-06
