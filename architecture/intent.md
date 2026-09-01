<!-- paos:reviewed=2026-09-01 -->
# Intent

## One sentence

Return clinician time to care by composing source-linked clinical context and bounded assistance **without weakening provenance, uncertainty or human clinical authority**.

## Primary user

Clinicians who currently reconstruct patient context across KIS/EHR, LIS, RIS/PACS, documents, ePA and legacy communication channels.

## Problem

Healthcare workers act as human middleware between fragmented systems. The obvious automation shortcut — summarise everything with an LLM — is unacceptable when pending information, corrected results, provenance or authority can be lost.

## Desired outcome

A clinician can reconstruct changed, pending and critical context faster, inspect every important source, prepare bounded documentation work and recover safely when sources change or systems degrade.

## Non-goals

- autonomous diagnosis, treatment recommendation or clinical decision-making;
- replacing KIS/EHR systems;
- production PHI write-back in the current research stage;
- calling synthetic evaluation clinical validation;
- hiding safety/recall failures behind a polished workflow demo.

## North star

**Time Returned to Care — safety gated.**

A speed improvement is not a win if source verification, correctness or safety becomes worse.

## Success looks like

Real clinicians complete a defined workflow faster or with less cognitive friction **without more errors, missed pending items, verification collapse or hidden safety stops**. External clinical/privacy/security/IT review must be able to falsify assumptions, not merely praise the interface.
