# Banking & Financial Services UI Patterns

## 1. Core Banking UI Principles

### Trust & Security First
- Display security indicators prominently: SSL lock icon, "Secure" badge near login
- Two-factor authentication UI: SMS/TOTP code entry with clear countdown timer and resend option
- Session timeout warning: show 2-minute warning modal before auto-logout; allow "Stay logged in"
- Never log users out without warning — always show timeout countdown
- Last login info: display "Last logged in: [date/time] from [location]" on dashboard

### Number Formatting
- Currency: always show currency symbol and 2 decimal places — `$1,234.56` not `$1234.5`
- Large amounts: use comma separators — `$1,000,000.00` not `$1000000`
- Negative balances: red with minus sign — `−$234.50` (use minus − not hyphen -)
- Percentage rates: always show 2 decimal places — `4.25%` not `4.2%`
- Account numbers: mask middle digits — `•••• •••• •••• 4821`
- Sort codes: format as `XX-XX-XX`, routing numbers as 9 digits

## 2. Account Dashboard

### Layout Pattern
- Account summary cards at top: account name, masked number, current balance, available balance
- Quick actions row: Transfer, Pay, Deposit, More
- Recent transactions list: date, merchant name + category icon, amount (credit=green, debit=black)
- Spending overview: pie or bar chart of category spend this month
- Upcoming scheduled payments section

### Account Card Design
- Balance is the primary focus: display large (28–36px, bold)
- Available vs. ledger balance: clearly distinguish these — customers confuse them
- Account type badge: Checking, Savings, Credit Card, ISA
- Color coding: use subtle account-type colour, not brand primary (reserved for CTA)

### Transaction List
- Group by date (Today, Yesterday, [Date])
- Each row: merchant icon/initials, merchant name, category, amount, pending indicator
- Pending transactions: muted colour + "Pending" badge
- Category icons: grocery cart, restaurant fork/knife, gas pump, shopping bag etc.
- Search: always include transaction search by merchant name, amount, or category
- Filter: by date range, category, amount range, transaction type

## 3. Transfer & Payment Flows

### Internal Transfer (Between Own Accounts)
```
Step 1: Select source account (dropdown with balance shown)
Step 2: Select destination account
Step 3: Enter amount (large numeric input, formatted in real-time)
Step 4: Select date (immediate or scheduled future date)
Step 5: Review screen — show all details, confirm button
Step 6: Success screen — reference number, option to transfer again
```

### External Payment / Bill Pay
- Payee management: saved payees list with avatar/logo, recent at top
- Adding new payee: account number + sort code + name; confirmation step with micro-deposit option
- Payment limits: clearly show daily/transaction limits; disable amount field if exceeded
- Recurring payments: toggle for one-time vs. recurring; frequency options (weekly, monthly, custom)
- Reference/note field: optional but prominent (important for rent, business payments)

### International Transfer / SWIFT / SEPA
- Currency selector with live exchange rate display
- Fee disclosure: must show all fees before confirmation (TILA/FCA requirement)
- Exchange rate: show mid-market rate and actual rate being applied with spread explanation
- Estimated arrival time by destination country
- BIC/SWIFT code validation with bank name confirmation

## 4. Credit Card Specific UI

### Statement
- Current balance, minimum payment, payment due date — all above the fold
- Available credit and credit limit in secondary position
- Payment button: primary CTA always "Make a Payment"
- Statement download: PDF and CSV options
- Interest charges: clearly itemised separately from purchases

### Credit Card Dashboard
- Credit utilisation meter (circular or linear gauge)
- 30/60/90 day statement periods
- Card-in-use animation for freeze/unfreeze toggle
- Rewards/points balance with redemption link

## 5. Savings & Goals UI

### Savings Goal Card
- Progress bar: percentage filled, amount saved vs. target
- Target date: countdown in days, "on track" / "behind" status
- Auto-save toggle: round-up rules, scheduled transfers
- Goal name and custom emoji/icon

### Interest Display
- AER/APY displayed prominently (required disclosure)
- Compound vs. simple interest: explain clearly
- Interest earned this period: show separately from deposits

## 6. Loan & Mortgage UI (covered in detail in loan domain)

## 7. Security & Alerts UI

### Alert Centre
- Transaction alerts: amount threshold controls, merchant category toggles
- Login notifications: show for every new device/location
- Large transaction alert: configurable threshold
- Alert delivery: in-app, push notification, email, SMS — let users choose per alert type

### Card Controls
- Freeze/unfreeze: prominent toggle at top of card detail view; instant feedback
- Contactless payments: toggle
- Online payments: toggle
- ATM withdrawals: toggle with withdrawal limit control
- Travel notification: date range + countries selector

## 8. Accessibility Requirements for Banking

- Screen reader must read full account numbers if revealed (do not mask from AT)
- Number keypad: for PIN entry, display large buttons (min 64×64px)
- Biometric authentication: always provide PIN/password fallback
- High contrast mode: balance amounts must remain legible in Windows High Contrast
- Session timeout warning: must be announced via aria-live
- Transaction confirmation: always require deliberate confirmation (no accidental transfers)
- WCAG 2.1 AA minimum; WCAG 2.2 AA strongly recommended for financial applications

## 9. Error States in Banking

### Insufficient Funds
- Show current balance vs. attempted amount
- Suggest overdraft option if available (with clear fee disclosure)
- Suggest transferring from another account (with link)

### Payment Failed
- Distinguish between: card declined, network error, fraud hold, daily limit exceeded
- Each case has a different resolution path — show the right one
- Reference number for every failed transaction (for customer support)

### Technical Errors
- Never show technical error codes to end users
- Always provide: what went wrong (vaguely), what to do next, support contact
- Retry button for transient errors
- If money was debited and confirmation failed: show "We're checking your transaction" state

## 10. Regulatory Disclosure UI

### Required Disclosures
- Interest rate changes: 30-day notice requirement — in-app banner + email
- Fee changes: mandatory notice period; display in alert centre
- Terms & conditions updates: require active re-acceptance for material changes
- FSCS/FDIC protection notice: show on account overview, maximum per-institution amount
- Currency conversion: mid-market rate source, timestamp, and spread must be shown
