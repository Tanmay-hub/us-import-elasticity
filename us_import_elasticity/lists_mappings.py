import os
_BASE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_BASE, 'datasets')

 
# For each calendar month in the panel, which CGDev snapshot was in effect?
# Logic:
#   Apr 2025: Liberation Day tariffs (Apr 2), snapshot Apr 29
#   May 2025: May 22 snapshot
#   Jun 2025: Jun 4 snapshot (90-day pause announced Apr 9, in effect most of June)
#   Jul 2025: Jun 4 snapshot (no new snapshot; same tariffs in effect)
#   Aug 2025: Aug 7 snapshot
#   Sep-Oct 2025: Aug 7 snapshot (no new snapshot)
#   Nov 2025: Nov 21 snapshot (later in month; more complete than Nov 6)
#   Dec 2025: Nov 21 snapshot (latest available)
#   Jan 2026: Nov 21 snapshot (latest available; Feb 2026 escalations not yet in effect)
MONTH_TO_SNAPSHOT = {
    '2025-M04': 'apr29',
    '2025-M05': 'may22',
    '2025-M06': 'june4',
    '2025-M07': 'june4', # The new tariffs from CGDEV's july snapshot were set to take effect in August
    '2025-M08': 'aug7',
    '2025-M09': 'aug7',
    '2025-M10': 'aug7',
    '2025-M11': 'nov21',
    '2025-M12': 'nov21',
    '2026-M01': 'nov21',
}
 
# Census month-column → panel month label
CENSUS_MONTH_COLS = {
    'IJAN': 'M01', 'IFEB': 'M02', 'IMAR': 'M03', 'IAPR': 'M04',
    'IMAY': 'M05', 'IJUN': 'M06', 'IJUL': 'M07', 'IAUG': 'M08',
    'ISEP': 'M09', 'IOCT': 'M10', 'INOV': 'M11', 'IDEC': 'M12',
}
 
# Aggregate / non-country rows in the Census file — drop these
CENSUS_ROWS_TO_DROP = {
    'Advanced Technology Products', 'Africa', 'Asia', 'Europe',
    'European Union', 'Pacific Rim', 'Sub Saharan Africa',
    'World, Not Seasonally Adjusted', 'World, Seasonally Adjusted',
    'Australia and Oceania', 'CAFTA-DR', 'North America',
    'South and Central America', 'USMCA with Canada (Consump)',
    'USMCA with Mexico (Consump)',
}
 
# Census name → CGDev name (only entries that differ)
CENSUS_TO_CGDEV = {
    'Burma':                        'Myanmar',
    'Congo':                        'Republic of the Congo',
    'Democratic Republic of Congo': 'Democratic Republic of the Congo',
    "Cote d'Ivoire":                'Ivory Coast',
    'East Timor':                   'Timor-Leste',
    'Korea, South':                 'South Korea',
    'Korea, North':                 'North Korea',
    'Macedonia':                    'Republic of Macedonia',
    'Republic of Yemen':            'Yemen',
    # Territories and micro-states with no CGDev entry → map to None (drop)
    'Andorra':                          None,
    'Anguilla':                         None,
    'Aruba':                            None,
    'British Indian Ocean Terr.':       None,
    'British Virgin Islands':           None,
    'Cayman Islands':                   None,
    'Christmas Island':                 None,
    'Cocos (Keeling) Islands':          None,
    'Cook Islands':                     None,
    'Curacao':                          None,
    'Falkland Islands(Islas Malvin':    None,
    'Faroe Islands':                    None,
    'French Guiana':                    None,
    'French Polynesia':                 None,
    'French Southern and Antarctic':    None,
    'Gambia':                           None,
    'Gaza Strip admin. by Israel':      None,
    'Gibraltar':                        None,
    'Guadeloupe':                       None,
    'Heard and McDonald Islands':       None,
    'Hong Kong':                        None,  # separate tariff treatment; not in CGDev
    'Liechtenstein':                    None,
    'Macau':                            None,  # separate tariff treatment; not in CGDev
    'Malta':                            None,
    'Marshall Islands':                 None,
    'Martinique':                       None,
    'Mayotte':                          None,
    'Micronesia':                       None,
    'Monaco':                           None,
    'Montserrat':                       None,
    'Niue':                             None,
    'Norfolk Island':                   None,
    'Pitcairn Islands':                 None,
    'Reunion':                          None,
    'San Marino':                       None,
    'Sint Maarten':                     None,
    'Solomon Islands':                  None,
    'St Helena':                        None,
    'St Pierre and Miquelon':           None,
    'Svalbard, Jan Mayen Island':       None,
    'Tokelau':                          None,
    'Turks and Caicos Islands':         None,
    'Vatican City':                     None,
    'Wallis and Futuna':                None,
    'West Bank admin. by Israel':       None,
}