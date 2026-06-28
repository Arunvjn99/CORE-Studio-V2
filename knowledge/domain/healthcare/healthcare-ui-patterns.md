# Healthcare UI Patterns

## 1. Core Healthcare UI Principles

### Patient Safety First
- Clinical information must be unambiguous — no abbreviations without explanation
- Medication names: display both brand and generic names
- Dosage: always include unit (mg, ml, mcg) — never just a number
- Allergy information: must be surfaced prominently at point of prescribing/ordering
- Critical values: red with high-visibility alert pattern; cannot be dismissed without acknowledgement

### Trust & Privacy
- HIPAA compliance is non-negotiable (see compliance standards)
- PHI indicators: show a privacy badge when displaying protected health information
- Session timeout: 15 minutes maximum for clinical applications
- Audit trail: "This record was last accessed by [Role] on [Date]" for sensitive records
- Role-based access: what a patient sees vs. clinician vs. admin must be clearly differentiated by UI

## 2. Patient Portal UI

### Dashboard (Patient View)
- Upcoming appointments: next 3 appointments at top, with join link for telehealth
- Recent test results: status badge (Ready to View / Pending / Reviewed by Doctor)
- Medication list: name, dosage, frequency, next refill date
- Outstanding action items: forms to complete, payments due, messages to respond to
- Health summary: key metrics (last BP reading, last A1C, etc.) with trending arrows

### Appointment Booking Flow
```
Step 1: Select appointment type (New patient / Follow-up / Urgent care / Specialist)
Step 2: Select provider (show name, photo, specialty, next available slot)
Step 3: Select date/time (calendar picker with available slots highlighted)
Step 4: Insurance verification (pre-fill from profile, confirm coverage)
Step 5: Reason for visit (free text + pre-set categories)
Step 6: Confirmation + add to calendar option
```

### Telehealth / Video Consultation UI
- Pre-visit checklist: camera test, microphone test, internet speed check
- Waiting room: estimated wait time, provider profile, ability to notify if running late
- In-call: large video area, muted indicator, chat panel, screen share, end call clearly labeled
- Post-call: visit summary, prescription issued, follow-up booking

## 3. Clinical Application UI (EHR/EMR)

### Patient Header (Persistent)
Present on every clinical screen:
- Patient name (large, 18px+), age, gender identity, date of birth
- MRN (Medical Record Number) clearly labeled
- Allergies: red badge with allergy count; click to expand; critical allergies bolded
- Code status: prominent colour-coded indicator (Full Code / DNR / DNI)
- Isolation precautions: yellow/orange badge if applicable
- Active alerts (falls risk, organ donor, etc.)

### Medication Administration Record (MAR)
- Drug name: bold, large
- Dose and route: below drug name, smaller but clear
- Schedule: time slots across columns with administered/missed/due states
- Administered: green check with timestamp and nurse initials
- Missed: red X with reason required
- Due now: amber highlight
- High-alert medications: red border + warning icon (insulin, heparin, opioids)
- Five Rights display: Patient, Drug, Dose, Route, Time — always visible in admin workflow

### Lab Results UI
- Normal range always shown alongside result value
- Out-of-range values: critical low (blue), low (yellow), normal (green), high (orange), critical high (red)
- Delta (change from previous): show trend arrow and previous value
- Result age: timestamp + "X days ago" label
- Ordered by: provider name + date ordered
- Resulted by: lab name + date resulted
- Actionable results: "Review Required" badge triggers alert to ordering provider

### Order Entry (CPOE)
- Drug interaction alerts: block (contraindicated) vs. warn (monitor closely) vs. inform (FYI)
- Alert fatigue mitigation: only show actionable alerts; suppress low-priority informational alerts
- Dosing calculator: weight-based dosing for paediatric; renal dose adjustment prompts
- Allergy cross-check: real-time allergy screening before order completion
- Duplicate order detection: flag if same drug already ordered
- Formulary: show formulary status; suggest alternatives for non-formulary drugs

## 4. Vital Signs & Monitoring UI

### Vital Signs Entry
- Fields: Temperature (with unit toggle °C/°F), Blood Pressure (systolic/diastolic), Heart Rate, Respiratory Rate, SpO2, Weight, Height, Pain Score (0–10)
- Normal ranges shown as input field placeholder or info tooltip
- Out-of-range: immediate red border + clinical alert if critical threshold crossed
- Pain scale: numeric + visual faces scale for paediatric/communication-impaired patients

### Trend Charts
- Default view: last 24 hours; allow zoom to 72h, 7 days, admission period
- Multiple vitals on same chart: colour-coded lines, legend always visible
- Abnormal range shading: light red background for values outside normal range
- Intervention markers: medication given, procedure performed marked on timeline

## 5. Patient Communication UI

### Secure Messaging (Patient ↔ Provider)
- Reply time expectation: "Our team typically responds within 2 business days"
- Subject line required for new messages
- Urgency selector: Non-urgent / Needs attention soon / Urgent (urgent routes to triage)
- Message threads: group by topic, show provider name + role
- Attachments: allow images (wound photos), documents; size limit 10MB with clear guidance
- HIPAA reminder: "Do not send sensitive information via insecure channels"

### After-Visit Summary
- Diagnosis (in plain language, not ICD codes)
- Instructions: numbered list, action-oriented
- Prescriptions: name, dose, frequency, duration, pharmacy
- Follow-up: date, provider, location
- Resources: links to condition-specific patient education
- Emergency symptoms: red-bordered section "Go to ER if you experience…"

## 6. Insurance & Billing UI

### Explanation of Benefits (EOB) UI
- Billed amount vs. plan discount vs. what insurance paid vs. patient owes — 4 clear columns
- Claim status: Processed / Pending / Denied with appeal option
- Balance due: prominent, with Pay Now CTA
- Payment plan: instalment option for large balances

### Prior Authorization UI (Provider)
- Auth request status: Submitted / Pending / Approved / Denied / Expired
- Denial reason: must be shown with appeal deadline
- Auth number: prominent display for approved auths
- Expiry date with countdown: "Expires in 23 days"

## 7. Accessibility in Healthcare

Healthcare has elevated accessibility requirements due to:
- Patients with visual impairment using screen readers to manage their health
- Elderly users who may have motor difficulties
- Clinical staff using with gloves (no fine touch)
- Emergency scenarios where speed matters

Required:
- WCAG 2.1 AA absolute minimum; AAA preferred for critical functions
- Touch targets for clinical apps: 48×48px minimum
- Colour never the sole differentiator for clinical status (always add icon or text)
- Voice input support for note-taking (clinical workflow)
- High contrast mode must not lose any clinical information

## 8. Emergency & Urgent States

- Critical alerts: full-screen overlay with acknowledge button (not dismissible by clicking outside)
- Code Blue/Emergency: distinct visual pattern breaking from normal UI, cannot be ignored
- "Do not disturb" mode for non-urgent notifications during critical events
- Offline capability: key reference data (drug reference, allergy list) must work without internet
