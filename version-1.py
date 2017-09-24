import sys
import urllib2
import xml.etree.ElementTree as ET

channelCodes = {
    'rtu': 'UC__Oy3QdB3d9_FHO_XG1PZg',
    'savage': 'UCoTemf51gr0OPV-jjPKumJA',
    'savage2': 'UC6Msyx_FPSo4T1jHddmmdKg',
    'infowars': 'UCYv-5LsUyc_P8KMo7YGPFPA',
    'macbreak': 'UC7DLT1zdSVGvnW11y4kqDng',
    'rightside': 'UCHqC-yWZ1kri4YzwRSt6RGQ',
    'cls': 'UCe3Dpne2qWldzpuiOd9hPLw',
    'dp': 'UCFzWAEPDGiY34bGpwM_DWmA',
    'md': 'UCzUV5283-l5c0oKRtyenj6Q',
    'aos': 'UCVtEytgcL5fZcSiKx-BjimQ',
    'pjw': 'UCittVh8imKanO_5KohzDbpg',
    'reddragon': 'UCpf0HFUmqDTnUY0fgaLqnFA',
    'ffp': 'UCKx31X4HNsuoLZjWiW7jbgQ'
}

if (len(sys.argv) < 2):
    for key, value in channelCodes.iteritems():
        print key
        
    quit()

channel = sys.argv[1]
baseURL = 'https://www.youtube.com/feeds/videos.xml?channel_id='



targetURL = baseURL + channelCodes[channel]


tree = ET.parse(urllib2.urlopen(targetURL))
root = tree.getroot()

print '\n'
print '########################################################################'
print '########################################################################'
print '########################################################################'
print '\n'

for child in root.findall('{http://www.w3.org/2005/Atom}entry'):
    print child[3].text
    url = child[4].get('href')
    print url
    space = ''
    for char in url:
        space += '-'
    space += '\n'
    print space

