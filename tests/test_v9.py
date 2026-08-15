from app.specialties import SPECIALTY_PACKS, list_specialty_packs, specialty_demo
from app.global_packs import architecture_manifest
from app.monetization_agent import monetization_manifest
from app.portability import ips_preview


def test_infectiology_pack_is_source_and_pending_focused():
    p=specialty_demo('infectiology')
    assert p['name']=='Infektiologie'
    labels={c['label'] for c in p['demo']['cards']}
    assert {'Mikrobiologie','Resistenz','Antiinfektiva','Hygiene','Device','Verlauf'} <= labels
    assert p['demo']['pending']
    assert all(c['source'] for c in p['demo']['cards'])
    assert 'RKI/KRINKO' in p['guideline_sources']


def test_oncology_and_neurology_share_pack_contract():
    required={'id','name','tagline','priority_sections','questions','guideline_sources','demo'}
    for pack_id in ('oncology','neurology'):
        assert required <= set(SPECIALTY_PACKS[pack_id])
        assert SPECIALTY_PACKS[pack_id]['demo']['patient']['name']
        assert SPECIALTY_PACKS[pack_id]['demo']['cards']


def test_list_hides_large_demo_payload():
    items=list_specialty_packs()
    assert len(items)>=3
    assert all('demo' not in x for x in items)


def test_global_layers_are_orthogonal():
    a=architecture_manifest()
    assert {'DE','EU','VN'} <= set(a['countries'])
    assert {'de','en','vi'} <= set(a['languages'])
    assert {'clinician','patient_family','payer'} <= set(a['audiences'])
    assert 'Specialty Pack' in a['composition'] and 'Country Pack' in a['composition']


def test_payer_is_minimum_necessary_not_clinical_mirror():
    a=architecture_manifest()['audiences']['payer']['rule'].lower()
    assert 'minimum necessary' in a
    assert 'no default access' in a


def test_monetization_agent_has_patient_data_red_line():
    m=monetization_manifest()
    text=' '.join(m['red_lines']).lower()
    assert 'no sale' in text and 'patient data' in text
    assert any(x['id']=='hospital-pilot' for x in m['models'])


def test_ips_preview_is_honest_and_provenance_preserving():
    b=ips_preview('farid','vi')
    assert b['resourceType']=='Bundle' and b['type']=='document'
    assert b['meta']['conformance']=='preview-not-validated'
    assert b['meta']['presentation_language']=='vi'
    assert b['translation_policy']['clinical_source_text_preserved'] is True
    assert all(x.get('source') for x in b['sections']['recent_events'])
