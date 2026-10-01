# Problem statement and solution brief

## The problem

People in Bharat often know the need (“I need crop insurance”, “my father
needs a pension”, “I need a working-capital loan”) but not the programme,
department, documents, state condition, deadline, or next action. The existing
discovery journey makes a person search across departmental portals and interpret
long eligibility pages. A wrong or overconfident answer can cost time, money,
trust, or a missed deadline.

The task is not to replace a department. It is to provide a **safe first mile**:
structure broad facts, discover relevant official programmes, explain why a
programme surfaced, show what is unknown, and help a person prepare for the
official channel.

## Users

- Citizens with a mobile phone and limited time or digital confidence.
- Common Service Centre / NGO / panchayat facilitators helping multiple people.
- Family members assisting an older person, farmer, student, or vendor.
- Judges who need to see an agent reason and act, not only produce fluent text.

## Solution: HaqSetu

HaqSetu is a bilingual (English/Hindi), low-bandwidth, evidence-first agent. A
user provides broad profile facts without identity credentials and describes a
need in natural language. HaqSetu then:

1. **Understands** the profile and need fields.
2. **Retrieves** relevant scheme records from a curated source-linked catalogue.
3. **Reasons** with explicit, inspectable rules.
4. **Uses tools/data** through the catalogue and rule engine.
5. **Acts safely** by producing a source-backed action plan and missing-fact list.
6. **Delivers** a local draft checklist only after explicit consent.

## Differentiator

### Evidence + Counterfactual Ledger

Most scheme chatbots jump from a prompt to a recommendation. HaqSetu exposes the
intermediate ledger:

- `matched`: the provided fact is consistent with a screening rule;
- `not_matched`: the supplied fact is inconsistent, without calling it a
  rejection;
- `missing`: the fact is not provided and must be verified;
- `counterfactual`: the smallest next fact/condition to check that could change
  the screening signal.

The user sees the source, the rule, and the reason. The agent cannot silently
turn uncertainty into approval.

## Scope boundary for the hackathon

The prototype uses seven central/portal records to demonstrate the agent loop:
PM-KISAN, PMFBY, Ayushman Bharat PM-JAY, IGNOAPS/NSAP, PMAY-G, PM SVANidhi,
and National Scholarship Portal post-matric catalogues. It deliberately does
not perform live application submission, identity verification, payment, or
official eligibility adjudication.

## Expected impact hypothesis

For a first-mile user or facilitator, HaqSetu should reduce the effort of
scanning multiple scheme pages and make uncertainty visible. The demo measures
the proxy “estimated minutes saved” and, more importantly, records whether the
agent exposes citations, missing facts, and the consent boundary. A production
pilot should measure:

- time-to-first-relevant-official-link;
- percentage of users who can name the next action;
- source-groundedness and stale-source rate;
- successful hand-off to a CSC/department;
- false-positive / false-confidence rate;
- language and accessibility success by user cohort.
