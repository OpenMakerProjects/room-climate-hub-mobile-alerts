import hashlib,json,pathlib,re,subprocess,sys,xml.etree.ElementTree as ET
from decode_project_image import validate_png
ROOT=pathlib.Path(__file__).resolve().parents[1]
required=['README.md','LICENSE','docs/circuit-diagram.svg','docs/images/project-overview.png','platformio.ini','requirements.txt','tools/mobile_bridge.py','tests/alert_policy_test.cpp','firmware/room-climate-hub-mobile-alerts/config.h']
for path in required:assert (ROOT/path).is_file(),path
readme=(ROOT/'README.md').read_text(encoding='utf-8')
for heading in ['Objectives','Architecture','Bill of materials','Prerequisites','Exact pin','Assembly','Setup','Configuration','Telemetry','Validation','Troubleshooting','Limitations','Future work','Contributing']:assert heading in readme,heading
for target in re.findall(r'\]\(([^)]+)\)',readme):
    if not target.startswith(('https://','http://','#')):assert (ROOT/target.split('#')[0]).exists(),target
svg=(ROOT/'docs/circuit-diagram.svg').read_text(encoding='utf-8');ET.fromstring(svg)
assert not re.search(r'<(?:script|foreignObject)|(?:href|src)=["\']https?://',svg)
for label in ['A4/SDA','A5/SCL','D3','D5','D6','0x76','0x3C','Common cathode','1 kΩ']:assert label in svg,label
png=(ROOT/'docs/images/project-overview.png').read_bytes();dimensions=validate_png(png)
manifest=json.loads((ROOT/'docs/images/project-overview.manifest.json').read_text(encoding='utf-8'))
assert hashlib.sha256(png).hexdigest()==manifest['sha256'] and len(png)==manifest['bytes'] and list(dimensions)==manifest['dimensions']
assert not list((ROOT/'docs/images').glob('*.b64.*')),'Temporary image transport remains'
assert 'MIT License' in (ROOT/'LICENSE').read_text(encoding='utf-8')
for p in ROOT.rglob('*'):
    if not p.is_file() or any(x in p.parts for x in ['.git','.pio','.venv','__pycache__']):continue
    assert p.name!='config.local.h','Local credentials must never be committed'
    if p.suffix not in ['.png','.b64']:
        content=p.read_text(encoding='utf-8',errors='ignore')
        assert not re.search(r'(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-proj-[A-Za-z0-9_-]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY)',content),p
subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Werror','tests/alert_policy_test.cpp','-o','/tmp/alert-policy'],cwd=ROOT,check=True)
subprocess.run(['/tmp/alert-policy'],check=True)
subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,check=True)
print('PASS: policy, bridge, transport tests; README links; SVG; PNG SHA/dimensions; license; credential patterns')
