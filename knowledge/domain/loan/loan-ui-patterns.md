# Loan & Mortgage UI Patterns

## 1. Core Loan UI Principles

### Transparency Is Non-Negotiable
- Total cost of credit must be displayed before any commitment
- APR must be shown more prominently than the monthly payment (regulators require this)
- All fees itemised: origination fee, appraisal fee, title insurance, closing costs
- No teaser rates without prominently showing the revert rate and when it applies
- Comparison of offered rate vs. average market rate helps trust (optional but recommended)

### Regulatory Requirements
- TILA (Truth in Lending Act): Loan Estimate (LE) disclosure within 3 business days of application
- RESPA: Good Faith Estimate for mortgages
- Right of rescission: 3-day cooling-off period for refinances; show timer in UI
- HMDA data collection for mortgage applications
- State usury laws: maximum APR varies by state — validate and display limit

## 2. Loan Application Flow

### Personal Loan Application
```
Step 1: Loan purpose & amount
  - Purpose dropdown: debt consolidation, home improvement, medical, auto, other
  - Amount slider/input: show real-time estimated monthly payment as amount changes
  - Term selector: 12, 24, 36, 48, 60 months with monthly payment for each

Step 2: Personal information
  - Full legal name, date of birth, SSN (last 4 initially; full SSN after soft check)
  - Address (current + 2 years history if < 2 years at current address)
  - Employment status and income verification

Step 3: Soft credit check & pre-qualification
  - "This won't affect your credit score" — display prominently
  - Show range of rates for which you qualify (not a firm offer yet)
  - Pre-qualification is not approval — make this clear

Step 4: Rate selection
  - Show 2–3 rate options: lowest monthly payment, lowest total cost, middle option
  - For each: APR, monthly payment, total interest, origination fee
  - Allow direct comparison table

Step 5: Full application
  - Hard credit pull consent — explicit checkbox, explain impact
  - Income documentation upload: payslips, bank statements, tax returns
  - Bank account for disbursement

Step 6: Decision
  - Instant decision if possible: approved, pending review, declined
  - Declined: show reason categories (score, income, DTI) without exact score (FCRA compliance)
  - Counter-offer: lower amount approved — show clearly this is a different offer

Step 7: Offer acceptance & e-signature
  - Full loan agreement in readable format (Flesch score > 60)
  - Material terms callout box before signature: APR, payment, total cost, penalties
  - E-signature: clear, deliberate action (not just a checkbox)

Step 8: Funding
  - Timeline: "Funds deposited within X business days"
  - Confirmation with reference number
  - Email + in-app notification
```

## 3. Mortgage Application UI

### Mortgage-Specific Steps
- Property information: address, estimated value, property type
- Purchase vs. refinance: different flows and disclosures
- Down payment amount and source (own funds, gift, grant — HMDA requirement)
- Loan-to-value (LTV) calculator shown inline
- Rate lock option: show rate lock period and expiry

### Mortgage Rate Display
- Always show: interest rate AND APR (APR includes fees)
- Points: show option to buy down rate with points vs. no-points comparison
- Lock period: 30/45/60 day lock with pricing difference
- Rate comparison chart: show historical 30-day average for context

### Loan Estimate (LE) UI
Required by law within 3 business days:
- Section A: Loan terms (amount, interest rate, monthly principal & interest, prepayment penalty Y/N, balloon payment Y/N)
- Section B: Projected payments table (years 1–7 and 8–30 for 30-yr mortgage)
- Section C: Costs at closing (itemised)
- Section D: Calculating cash to close
- Section E: Comparisons (APR, total interest percentage)

## 4. Loan Dashboard (Post-Origination)

### Loan Summary Card
- Remaining balance (large, bold)
- Next payment: amount + due date + "X days away"
- Interest rate + loan type (fixed/variable)
- Payoff date
- Quick actions: Make Payment, View Statement, Set Up Auto-Pay

### Payment History
- Each row: payment date, amount paid, principal portion, interest portion, remaining balance
- Missed payment: red row with "Missed" badge and late fee charged
- Extra payment applied to principal: show with different colour; indicate months saved
- Year-to-date interest paid (for tax purposes)

### Amortisation Schedule
- Full schedule in a table: month, payment, principal, interest, balance
- Chart overlay: principal vs. interest over time (shows how early payments reduce total interest)
- Toggle: show/hide full schedule (usually very long)
- Highlight current row (current month)

### Auto-Pay Management
- Clear display of: payment amount, payment date, source account
- Change date: option to change within current billing cycle
- Pause: one-time skip option (within lender policy)
- Bank account management: add/remove source accounts

## 5. Affordability Calculator UI

### Key Inputs
- Gross monthly income
- Monthly debts (credit cards, car loans, student loans)
- Down payment amount (and % of purchase price)
- Annual property tax (pull from address lookup)
- Home insurance estimate
- HOA fees (if applicable)

### Outputs to Display
- Debt-to-income (DTI) ratio: target < 43% (conventional), < 50% (FHA)
- Maximum loan amount qualifying for
- Estimated purchase price range
- Monthly payment breakdown: P+I, tax, insurance, PMI (if LTV > 80%)
- Cash needed to close: down payment + closing costs estimate

### Visual Design
- Real-time updates as inputs change
- DTI gauge: green (< 36%), amber (36–43%), red (> 43%)
- Slider for purchase price: updates all calculations dynamically
- "What if I pay more down?" toggle to show PMI removal impact

## 6. Refinance UI

### Refinance Decision Support
- Break-even calculator: months to recoup closing costs via monthly savings
- Current loan info vs. new loan comparison: side-by-side table
- Total interest savings over loan life
- Cash-out refinance: show equity available, amount requested, new LTV

## 7. Error States for Loan Applications

### Application Errors
- Incomplete field: immediate inline error with specific guidance
- Income mismatch: "The income entered doesn't match your documents. Please review."
- Duplicate application: "An application is already in progress. Continue or start fresh?"
- System error during credit pull: "We're having trouble accessing credit data. Try again in a few minutes."

### Decline Handling (Adverse Action)
- Required by ECOA and FCRA: specific reasons for adverse action
- Typical reasons: credit score below minimum, DTI too high, insufficient income, derogatory marks
- Must provide: adverse action notice with reasons, right to get free credit report
- UI: empathetic tone; suggest alternatives (lower amount, co-borrower, wait 6 months)

## 8. Accessibility & Usability for Loan Applications

- Save progress: never lose form data on back navigation; auto-save every 30 seconds
- Long applications: progress bar with percentage complete, step names shown
- Document upload: drag-and-drop + tap-to-upload; show upload progress; confirm success
- Help text: every technical term has a tooltip or expandable explanation
- Live chat: provide chat option during business hours for complex questions
- Mobile-optimised: entire application must be completable on mobile (captures large audience)
- Pre-fill from government data: where possible, use IRS transcript, employer verification APIs
