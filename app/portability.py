from __future__ import annotations
from datetime import datetime, timezone
from .demo_data import PATIENTS, TIMELINES, FOCUS


def _patient(patient_id: str):
    return next((p for p in PATIENTS if p['id']==patient_id), None)


def ips_preview(patient_id: str, language: str = 'en'):
    """IPS-shaped portability preview. Not validated as an IPS-conformant document."""
    p=_patient(patient_id)
    if not p:
        return None
    focus=FOCUS.get(patient_id, {})
    facts=focus.get('facts', [])
    allergies=[f for f in facts if 'allerg' in f['label'].lower()]
    meds=[f for f in facts if 'medik' in f['label'].lower()]
    problems=[]
    for item in TIMELINES.get(patient_id, []):
        if any(word in item['summary'].lower() for word in ['niereninsuffizienz','stadium','diagnose']):
            problems.append({'text':item['summary'],'source_ref':item['source_ref']})
    return {
        'resourceType':'Bundle',
        'type':'document',
        'meta':{
            'profile_hint':'hl7.fhir.uv.ips',
            'conformance':'preview-not-validated',
            'generated_at':datetime.now(timezone.utc).isoformat(),
            'presentation_language':language,
        },
        'patient':{
            'id':p['patient_no'], 'name':p['name'], 'birthDate_display':p['dob'], 'sex_display':p['sex']
        },
        'sections':{
            'allergies':[{'text':x['value'],'source':x['source']} for x in allergies],
            'medications':[{'text':x['value'],'source':x['source']} for x in meds],
            'problems':problems,
            'recent_events':[
                {'title':x['title'],'summary':x['summary'],'source':x['source'],'source_ref':x['source_ref']}
                for x in TIMELINES.get(patient_id, [])[:5]
            ],
        },
        'translation_policy':{
            'clinical_source_text_preserved':True,
            'machine_translation_may_change_presentation_only':True,
            'high_risk_content_requires_original_available':True,
        }
    }
