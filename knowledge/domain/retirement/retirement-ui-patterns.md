# Retirement Planning UI Patterns

## 1. Core Retirement UI Principles

### Reduce Anxiety, Build Confidence
- Retirement planning causes significant anxiety — UI must reduce cognitive load
- Show progress, not just gaps ("You've saved $X" before "You need $Y more")
- Use positive framing: "You're on track for 73% of your goal" not "You're 27% short"
- Complex calculations made visual: charts over tables, plain English over percentages
- Education integrated contextually: explain concepts at the moment of decision, not upfront

### Regulatory Requirements
- Plan documents (SPD, SAI) must be accessible within 2 clicks
- Fee disclosure: all fees expressed as percentage AND dollar amount per $1,000 invested
- ERISA-required notices: quarterly statements, annual fee disclosure, blackout periods
- RMD (Required Minimum Distribution) reminders at age 73 (SECURE Act 2.0)

## 2. Retirement Dashboard

### Hero Section
- Projected retirement income (monthly at target retirement age): LARGE, prominent
- "On track" indicator: green check, amber warning, or red alert with action step
- Retirement readiness score: 0–100 gauge or progress ring
- Target retirement age: editable inline

### Account Summary
- Each account (401k, IRA, Roth IRA, pension) shown as card:
  - Account type badge
  - Current balance (large)
  - YTD return: percentage + dollar amount, green if positive
  - YTD contribution vs. annual limit
  - Employer match: "Capturing X% of available match"
- Total across all accounts: shown prominently above individual cards

### Projection Chart
- Line chart: current savings path vs. goal path
- X-axis: current age to target retirement age
- Y-axis: portfolio value
- Two lines: "At current rate" vs. "Target"
- Gap area shaded in amber/red
- Milestone markers: age 59½ (penalty-free withdrawals), age 65 (Medicare), age 67/70 (Social Security)
- Toggle: include/exclude Social Security in projection

## 3. Contribution Management

### Annual Limit Display
- 401(k) limit: $23,000 (2024), $30,500 if age 50+ (catch-up)
- IRA limit: $7,000 (2024), $8,000 if age 50+
- Progress bar: "You've contributed $14,500 of $23,000 (63%)"
- Pacing indicator: "You're on pace to contribute $18,200 this year — $4,800 below the limit"
- "Increase contribution" CTA always visible near limit display

### Contribution Change Flow
- Current contribution: percentage of salary + equivalent dollar amount
- New contribution: slider + text input (dual input — users think in both %)
- Impact calculator: "With this change, your estimated monthly retirement income changes from $X to $Y"
- Employer match implication: "At X%, you're capturing Y% of available employer match"
- Effective date: next pay period or specific date

### Catch-Up Contributions
- Alert at age 50: "You're now eligible for catch-up contributions — add up to $7,500 more per year"
- Separate catch-up contribution toggle/field
- Tax year cutoff reminder: December 31 for 401(k), April 15 for IRA

## 4. Investment Allocation

### Portfolio Overview
- Asset allocation donut chart: stocks, bonds, real estate, cash — with percentages and dollar values
- Target vs. actual allocation: side-by-side comparison
- Rebalancing alert: "Your portfolio has drifted X% from target — consider rebalancing"
- Risk score: current (measured) vs. target (selected by user), 1–10 scale

### Fund Selection UI
- Fund name + ticker symbol
- Asset class (US Stock, International, Bond, etc.)
- Expense ratio: shown as %, flagged if > 0.5% (high cost)
- 1yr, 3yr, 5yr, 10yr performance vs. benchmark
- Morning star rating (if licensed)
- Fund category filter + search
- Comparison tool: select up to 3 funds to compare side by side

### Risk Questionnaire
- 5–10 questions with clear, everyday-language options (not financial jargon)
- After each answer, progress indicator updates
- Result: risk profile (Conservative / Moderately Conservative / Moderate / Growth / Aggressive)
- Suggested allocation tied directly to result
- "How we calculated this" expandable explanation
- Allow manual override with warning about deviation from recommendation

## 5. Social Security Optimisation

### Claiming Age Comparison
- Show monthly benefit at ages 62, 65, 66/67 (FRA), 70
- Break-even age calculator: "Waiting until 70 pays off after [age X]"
- Spousal benefit: show if married, eligible for spousal vs. own benefit comparison
- Chart: monthly benefit over time for different claiming ages
- Clear explanation: taking early permanently reduces benefit

### Social Security Integration
- SSA.gov API integration (with user consent): pull actual earnings record
- Privacy notice: explain what data is pulled and why
- If no SSA data: income-based estimate with clear disclaimer

## 6. Retirement Income Planning

### Withdrawal Strategy UI
- 4% rule calculator: sustainable withdrawal amount from current balance
- Bucket strategy visual: short-term (cash, 0–2yrs), medium-term (bonds, 2–10yrs), long-term (equities, 10yr+)
- Sequence of returns risk: "Bad market in first 5 years of retirement can deplete portfolio X% faster" — visual simulation
- Tax-efficient withdrawal order: taxable account → Traditional → Roth (show the recommended order and why)

### Required Minimum Distributions (RMDs)
- Alert at age 72/73: "Your first RMD is due by April 1 of next year"
- RMD calculator: balance × distribution factor from IRS Uniform Lifetime Table
- Show RMD as both dollar amount and percentage of balance
- Tax impact: estimated federal/state tax on RMD
- Charitable distribution option (QCD): highlight for users over 70½ who give to charity

## 7. Pension & Defined Benefit UI

- Projected monthly benefit at target retirement date
- Early retirement reduction: how much benefit reduces per year before normal retirement age
- Survivor benefit option: show trade-off between single life annuity vs. joint & survivor
- Service years counter: credited years of service, years to vesting, years to full benefit

## 8. Education & Guidance UI

### Contextual Education
- Tooltip on every financial term: APR, AER, RMD, vesting, etc.
- "Why this matters" expandable sections for key metrics
- Article links related to current screen: viewing asset allocation → link to "How to rebalance your portfolio"

### Retirement Calculators
- Retirement income needs: expenses in retirement (housing, healthcare, travel, daily living)
- Inflation adjustment: show values in today's dollars AND future dollars
- Healthcare cost estimator: average retiree spends $315,000 on healthcare in retirement
- Life expectancy: use actuarial tables; show probability of living to various ages

## 9. Accessibility for Retirement Products

- Charts must have tabular alternatives (accessible to screen readers)
- Projection numbers must be readable without chart (aria-label with key figures)
- Data tables: proper `<th scope>` for row and column headers
- Complex calculations: show step-by-step breakdown for transparency
- Large font: default body text at 16px; key numbers at 24px+ (older user base)
- High contrast: all chart colours must maintain 3:1 contrast against white background
- Print view: optimised print stylesheet for regulatory statement requirements
