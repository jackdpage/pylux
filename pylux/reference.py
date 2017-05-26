# reference.py is part of Pylux
#
# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
# Pylux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylux is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''This file contains various universal constants.'''

usitt_line_weights = {
    'scenery' : 'line-weight-light',
    'leader' : 'line-weight-light',
    'dimension' : 'line-weight-light',
    'masking' : 'line-weight-medium',
    'drop' : 'line-weight-medium',
    'centre' : 'line-weight-medium',
    'plaster' : 'line-weight-medium',
    'batten' : 'line-weight-heavy',
    'fixture' : 'line-weight-heavy',
    'architecture' : 'line-weight-heavy',
    'border' : 'line-weight-heavy'}

paper_sizes = {
    'A0' : (841, 1189),
    'A1' : (594, 841),
    'A2' : (420, 594),
    'A3' : (297, 420),
    'A4' : (210, 297)}

gel_colours = {
# Rosco E-Colour+
    'Rose Pink' : '#FF40B9',
    'E002' : '#FF40B9',
    'Lavender Tint' : '#F5E6FF',
    'E003' : '#F5E6FF',
    'Medium Bastard Amber' : '#FAB8AC',
    'E004' : '#FAB8AC',
    'Pale Yellow' : '#FFFFDE',
    'E007' : '#FFFFDE',
    'Dark Salmon' : '#FF5E48',
    'E008' : '#FF5E48',
    'Pale Amber Gold' : '#FFD28A',
    'E009' : '#FFD28A',
    'Medium Yellow' : '#FFF30D',
    'E010' : '#FFF30D',
    'Straw Tint' : '#FFDBA1',
    'E013' : '#FFDBA1',
    'Deep Straw' : '#FDC819',
    'E015' : '#FDC819',
    'Surprise Peach' : '#CC5F3D',
    'E017' : '#CC5F3D',
    'Fire' : '#ED2000',
    'E019' : '#ED2000',
    'Medium Amber' : '#FF8A24',
    'E020' : '#FF8A24',
    'Gold Amber' : '#FF4800',
    'E021' : '#FF4800',
    'Dark Amber' : '#FF1900',
    'E022' : '#FF1900',
    'Scarlet' : '#F00E25',
    'E024' : '#F00E25',
    'Sunset Red' : '#FF4B2B',
    'E025' : '#FF4B2B',
    'Bright Red' : '#C70011',
    'E026' : '#C70011',
    'Medium Red' : '#A10000',
    'E027' : '#A10000',
    'Plasa Red' : '#BC0010',
    'E029' : '#BC0010',
    'Light Pink' : '#FFB8CE',
    'E035' : '#FFB8CE',
    'Medium Pink' : '#FF6E9E',
    'E036' : '#FF6E9E',
    'Pink Carnation' : '#FAC0D8',
    'E039' : '#FAC0D8',
    'Dark Magenta' : '#C5004F',
    'E046' : '#C5004F',
    'Rose Purple' : '#C43BFF',
    'E048' : '#C43BFF',
    'Medium Purple' : '#BE00D4',
    'E049' : '#BE00D4',
    'Light Lavender' : '#D7BAFF',
    'E052' : '#D7BAFF',
    'Paler Lavender' : '#E5DEFF',
    'E053' : '#E5DEFF',
    'Lavender' : '#9235FD',
    'E058' : '#9235FD',
    'Mist Blue' : '#D6E8FF',
    'E061' : '#D6E8FF',
    'Pale Blue' : '#B0D5F7',
    'E063' : '#B0D5F7',
    'Sky Blue' : '#597DFF',
    'E068' : '#597DFF',
    'Tokyo Blue' : '#3600B1',
    'E071' : '#3600B1',
    'Evening Blue' : '#4C79FF',
    'E075' : '#4C79FF',
    'Just Blue' : '#3700EB',
    'E079' : '#3700EB',
    'Deeper Blue' : '#1A00BF',
    'E085' : '#1A00BF',
    'Lime Green' : '#BEFF85',
    'E088' : '#BEFF85',
    'Moss Green' : '#00CD55',
    'E089' : '#00CD55',
    'Dark Yellow Green' : '#00870B',
    'E090' : '#00870B',
    'Spring Yellow' : '#F2FF30',
    'E100' : '#F2FF30',
    'Yellow' : '#FFEB0F',
    'E101' : '#FFEB0F',
    'Light Amber' : '#FFE74A',
    'E102' : '#FFE74A',
    'Straw' : '#FFE7C4',
    'E103' : '#FFE7C4',
    'Deep Amber' : '#FCD628',
    'E104' : '#FCD628',
    'Orange' : '#FF760D',
    'E105' : '#FF760D',
    'Primary Red' : '#DE0000',
    'E106' : '#DE0000',
    'Light Rose' : '#FF809F',
    'E107' : '#FF809F',
    'English Rose' : '#FAAD96',
    'E108' : '#FAAD96',
    'Light Salmon' : '#FF919C',
    'E109' : '#FF919C',
    'Middle Rose' : '#FFA3CA',
    'E110' : '#FFA3CA',
    'Dark Pink' : '#FF63A4',
    'E111' : '#FF63A4',
    'Magenta' : '#FF004D',
    'E113' : '#FF004D',
    'Peacock Blue' : '#00C9BF',
    'E115' : '#00C9BF',
    'Medium Blue Green' : '#009E96',
    'E116' : '#009E96',
    'Steel Blue' : '#A3E2FF',
    'E117' : '#A3E2FF',
    'Light Blue' : '#00B7FF',
    'E118' : '#00B7FF',
    'Dark Blue' : '#3300D9',
    'E119' : '#3300D9',
    'Deep Blue' : '#2800C9',
    'E120' : '#2800C9',
    'Leaf Green' : '#93FF54',
    'E121' : '#93FF54',
    'Fern Green' : '#74F55D',
    'E122' : '#74F55D',
    'Dark Green' : '#00AB44',
    'E124' : '#00AB44',
    'Mauve' : '#D400DB',
    'E126' : '#D400DB',
    'Smokey Pink' : '#BB334C',
    'E127' : '#BB334C',
    'Bright Pink' : '#FF177F',
    'E128' : '#FF177F',
    'Heavy Frost' : '#FFFFFF',
    'E129' : '#FFFFFF',
    'Clear' : '#FFFFFF',
    'E130' : '#FFFFFF',
    'Marine Blue' : '#02E3CC',
    'E131' : '#02E3CC',
    'Medium Blue' : '#5286FF',
    'E132' : '#5286FF',
    'Golden Amber' : '#F5632F',
    'E134' : '#F5632F',
    'Deep Golden Amber' : '#FF4A00',
    'E135' : '#FF4A00',
    'Pale Lavender' : '#E2C7FF',
    'E136' : '#E2C7FF',
    'Special Lavender' : '#B695FC',
    'E137' : '#B695FC',
    'Pale Green' : '#B4FFA8',
    'E138' : '#B4FFA8',
    'Primary Green' : '#009107',
    'E139' : '#009107',
    'Summer Blue' : '#38CAFF',
    'E140' : '#38CAFF',
    'Bright Blue' : '#00ACF0',
    'E141' : '#00ACF0',
    'Pale Violet' : '#AA96FF',
    'E142' : '#AA96FF',
    'Pale Navy Blue' : '#007194',
    'E143' : '#007194',
    'No Color Blue' : '#4FC4FF',
    'E144' : '#4FC4FF',
    'Apricot' : '#FF7438',
    'E147' : '#FF7438',
    'Bright Rose' : '#FF1472',
    'E148' : '#FF1472',
    'Gold Tint' : '#FFC0B5',
    'E151' : '#FFC0B5',
    'Pale Gold' : '#FFCAA8',
    'E152' : '#FFCAA8',
    'Pale Salmon' : '#FFB2BA',
    'E153' : '#FFB2BA',
    'Pale Rose' : '#FFB2BA',
    'E154' : '#FFB2BA',
    'Chocolate' : '#C57951',
    'E156' : '#C57951',
    'Pink' : '#FF4551',
    'E157' : '#FF4551',
    'Deep Orange' : '#FF5E00',
    'E158' : '#FF5E00',
    'No Color Straw' : '#FFFAE0',
    'E159' : '#FFFAE0',
    'Slate Blue' : '#4AABFF',
    'E161' : '#4AABFF',
    'Bastard Amber' : '#FFCFA8',
    'E162' : '#FFCFA8',
    'Flame Red' : '#F02225',
    'E164' : '#F02225',
    'Daylight Blue' : '#1CACFF',
    'E165' : '#1CACFF',
    'Pale Red' : '#FF3352',
    'E166' : '#FF3352',
    'Lilac Tint' : '#EBDAF5',
    'E169' : '#EBDAF5',
    'Deep Lavender' : '#DAADFF',
    'E170' : '#DAADFF',
    'Lagoon Blue' : '#00AACC',
    'E172' : '#00AACC',
    'Dark Steel Blue' : '#52B4FF',
    'E174' : '#52B4FF',
    'Loving Amber' : '#FAA498',
    'E176' : '#FAA498',
    'Chrome Orange' : '#FF9900',
    'E179' : '#FF9900',
    'Dark Lavender' : '#8B2BFF',
    'E180' : '#8B2BFF',
    'Congo Blue' : '#29007A',
    'E181' : '#29007A',
    'Light Red' : '#CC0000',
    'E182' : '#CC0000',
    'Moonlight Blue' : '#00BAF2',
    'E183' : '#00BAF2',
    'Cosmetic Peach' : '#FFFFFF',
    'E184' : '#FFFFFF',
    'Cosmetic Burgundy' : '#FFFFFF',
    'E185' : '#FFFFFF',
    'Cosmetic Silver Rose' : '#FFFFFF',
    'E186' : '#FFFFFF',
    'Cosmetic Rouge' : '#FFFFFF',
    'E187' : '#FFFFFF',
    'Cosmetic Highlight' : '#FFFFFF',
    'E188' : '#FFFFFF',
    'Cosmetic Silver Moss' : '#FFFFFF',
    'E189' : '#FFFFFF',
    'Cosmetic Emerald' : '#FFFFFF',
    'E190' : '#FFFFFF',
    'Cosmetic Aqua Blue' : '#FFFFFF',
    'E191' : '#FFFFFF',
    'Flesh Pink' : '#FF639F',
    'E192' : '#FF639F',
    'Rosy Amber' : '#FF454B',
    'E193' : '#FF454B',
    'Surprise Pink' : '#AC82FF',
    'E194' : '#AC82FF',
    'Zenith Blue' : '#0003CC',
    'E195' : '#0003CC',
    'True Blue' : '#00A1FF',
    'E196' : '#00A1FF',
    'Alice Blue' : '#1958CF',
    'E197' : '#1958CF',
    'Palace Blue' : '#43009C',
    'E198' : '#43009C',
    'Regal Blue' : '#3700EE',
    'E199' : '#3700EE',
    'Double CT Blue' : '#0F5BFF',
    'E200' : '#0F5BFF',
    'Full CT Blue' : '#73A9FF',
    'E201' : '#73A9FF',
    '1/2 CT Blue' : '#B8D5FF',
    'E202' : '#B8D5FF',
    '1/4 CT Blue' : '#E0EDFF',
    'E203' : '#E0EDFF',
    'Full CT Orange' : '#FF9B30',
    'E204' : '#FF9B30',
    '1/2 CT Orange' : '#FFD28F',
    'E205' : '#FFD28F',
    '1/4 CT Orange' : '#FFE6B8',
    'E206' : '#FFE6B8',
    'CT Orange + .3 Neutral Density' : '#A86300',
    'E207' : '#A86300',
    'CT Orange + .6 Neutral Density' : '#974400',
    'E208' : '#974400',
    '.3 Neutral Density' : '#BFBDBD',
    'E209' : '#BFBDBD',
    '.6 Neutral Density' : '#969595',
    'E210' : '#969595',
    '.9 Neutral Density' : '#636262',
    'E211' : '#636262',
    'LCT Yellow' : '#FBFFD9',
    'E212' : '#FBFFD9',
    'White Flame Green' : '#E0FCB3',
    'E213' : '#E0FCB3',
    'Full Tough Spun' : '#FFFFFF',
    'E214' : '#FFFFFF',
    'Half Tough Spun' : '#FFFFFF',
    'E215' : '#FFFFFF',
    'White Diffusion' : '#FFFFFF',
    'E216' : '#FFFFFF',
    'Blue Diffusion' : '#FFFFFF',
    'E217' : '#FFFFFF',
    'Eighth CT Blue ' : '#EBF3FF',
    'E218' : '#EBF3FF',
    'Fluorescent Green ' : '#2EE8CF',
    'E219' : '#2EE8CF',
    'White Frost' : '#FFFFFF',
    'E220' : '#FFFFFF',
    'Blue Frost' : '#FFFFFF',
    'E221' : '#FFFFFF',
    '1/8 CT Orange' : '#FFEAD1',
    'E223' : '#FFEAD1',
    'Daylight Blue Frost' : '#FFFFFF',
    'E224' : '#FFFFFF',
    'Neutral Density Frost' : '#FFFFFF',
    'E225' : '#FFFFFF',
    'U.V. Filter' : '#FFFFFF',
    'E226' : '#FFFFFF',
    'Brushed Silk' : '#FFFFFF',
    'E228' : '#FFFFFF',
    'Quarter Tough Spun' : '#FFFFFF',
    'E229' : '#FFFFFF',
    'Super Correction WF Green' : '#AD6824',
    'E232' : '#AD6824',
    'HMI To Tungsten' : '#FF8438',
    'E236' : '#FF8438',
    'C.I.D. to Tungsten' : '#F08F56',
    'E237' : '#F08F56',
    'C.S.I. to Tungsten' : '#E5B1A0',
    'E238' : '#E5B1A0',
    'Polarizer' : '#FFFFFF',
    'E239' : '#FFFFFF',
    'Fluorescent 5700K' : '#1AD8D8',
    'E241' : '#1AD8D8',
    'Fluorescent 4300K' : '#5AE2C7',
    'E242' : '#5AE2C7',
    'Fluorescent 3600K' : '#87E5B6',
    'E243' : '#87E5B6',
    'Plus Green' : '#E0FC90',
    'E244' : '#E0FC90',
    'Half Plus Green' : '#EAFCB8',
    'E245' : '#EAFCB8',
    'Quarter Plus Green' : '#F0FCD2',
    'E246' : '#F0FCD2',
    'Minus Green' : '#FFB8D0',
    'E247' : '#FFB8D0',
    'Half Minus Green' : '#FACDE0',
    'E248' : '#FACDE0',
    'Quarter Minus Green' : '#FADEE8',
    'E249' : '#FADEE8',
    'Half White Diffusion' : '#FFFFFF',
    'E250' : '#FFFFFF',
    'Quarter White Diffusion' : '#FFFFFF',
    'E251' : '#FFFFFF',
    'Eighth White Diffusion' : '#FFFFFF',
    'E252' : '#FFFFFF',
    'Hanover Frost' : '#FFFFFF',
    'E253' : '#FFFFFF',
    'HT New Hanover Frost' : '#FFFFFF',
    'E254' : '#FFFFFF',
    'Haarlem Frost' : '#FFFFFF',
    'E255' : '#FFFFFF',
    'Half Hanover Frost' : '#FFFFFF',
    'E256' : '#FFFFFF',
    'Quarter Hanover Frost' : '#FFFFFF',
    'E257' : '#FFFFFF',
    'Eighth Hanover Frost' : '#FFFFFF',
    'E258' : '#FFFFFF',
    'Heat Shield' : '#FFFFFF',
    'E269' : '#FFFFFF',
    'Scrim' : '#FFFFFF',
    'E270' : '#FFFFFF',
    'Mirror Silver' : '#FFFFFF',
    'E271' : '#FFFFFF',
    'Soft Gold Reflector' : '#FFFFFF',
    'E272' : '#FFFFFF',
    'Soft Silver Reflector' : '#FFFFFF',
    'E273' : '#FFFFFF',
    'Mirror Gold' : '#FFFFFF',
    'E274' : '#FFFFFF',
    'Black Scrim' : '#FFFFFF',
    'E275' : '#FFFFFF',
    'Eighth Plus Green' : '#F6FFE0',
    'E278' : '#F6FFE0',
    'Eighth Minus Green' : '#FCE8F3',
    'E279' : '#FCE8F3',
    'Three Quarter CT Blue' : '#9CC5FF',
    'E281' : '#9CC5FF',
    '1.5 CT Blue' : '#759EE5',
    'E283' : '#759EE5',
    '3/4 CT Orange' : '#F7AF5C',
    'E285' : '#F7AF5C',
    '1.5 CT Orange' : '#F8963E',
    'E286' : '#F8963E',
    'Double CT Orange' : '#F77F1E',
    'E287' : '#F77F1E',
    '.15 Neutral Density' : '#DCD9D9',
    'E298' : '#DCD9D9',
    '1.2 Neutral Density' : '#474747',
    'E299' : '#474747',
    'Soft Green' : '#02E59A',
    'E322' : '#02E59A',
    'Jade' : '#02E2A3',
    'E323' : '#02E2A3',
    'Mallard Green' : '#005C46',
    'E325' : '#005C46',
    'Forest Green' : '#006539',
    'E327' : '#006539',
    'Follies Pink' : '#FF33A0',
    'E328' : '#FF33A0',
    'Special Rose Pink' : '#FF0D6A',
    'E332' : '#FF0D6A',
    'Plum' : '#CD9BD1',
    'E341' : '#CD9BD1',
    'Special Medium Lavender' : '#7345FF',
    'E343' : '#7345FF',
    'Violet' : '#A98AFF',
    'E344' : '#A98AFF',
    'Fuschia Pink' : '#C953DB',
    'E345' : '#C953DB',
    'Glacier Blue' : '#00A6FF',
    'E352' : '#00A6FF',
    'Lighter Blue' : '#54D5FF',
    'E353' : '#54D5FF',
    'Special Steel Blue ' : '#00BFD8',
    'E354' : '#00BFD8',
    'Special Medium Blue' : '#0236DF',
    'E363' : '#0236DF',
    'Cornflower' : '#5783CF',
    'E366' : '#5783CF',
    'Rolux' : '#FFFFFF',
    'E400' : '#FFFFFF',
    'Light Rolux' : '#FFFFFF',
    'E401' : '#FFFFFF',
    'Soft Frost' : '#FFFFFF',
    'E402' : '#FFFFFF',
    'Half Soft Frost' : '#FFFFFF',
    'E404' : '#FFFFFF',
    'Opal Frost' : '#FFFFFF',
    'E410' : '#FFFFFF',
    'Highlight' : '#FFFFFF',
    'E414' : '#FFFFFF',
    'Three Quarter White' : '#FFFFFF',
    'E416' : '#FFFFFF',
    'Light Opal Frost' : '#FFFFFF',
    'E420' : '#FFFFFF',
    'Quiet Frost' : '#FFFFFF',
    'E429' : '#FFFFFF',
    'Grid Cloth' : '#FFFFFF',
    'E430' : '#FFFFFF',
    'Light Grid Cloth' : '#FFFFFF',
    'E432' : '#FFFFFF',
    'Quarter Grid Cloth' : '#FFFFFF',
    'E434' : '#FFFFFF',
    'Full CT Straw' : '#F7BF4F',
    'E441' : '#F7BF4F',
    'Half CT Straw' : '#FFCE9C',
    'E442' : '#FFCE9C',
    'Quarter CT Straw' : '#FFE3BA',
    'E443' : '#FFE3BA',
    'Eighth CT Straw' : '#FFF5DC',
    'E444' : '#FFF5DC',
    'Three Eighths White' : '#FFFFFF',
    'E450' : '#FFFFFF',
    'One Sixteenth White' : '#FFFFFF',
    'E452' : '#FFFFFF',
    'Quiet Grid Cloth' : '#FFFFFF',
    'E460' : '#FFFFFF',
    'Quiet Light Grid Cloth' : '#FFFFFF',
    'E462' : '#FFFFFF',
    'Quiet Quarter Grid Cloth' : '#FFFFFF',
    'E464' : '#FFFFFF',
    'Full Atlantic Frost' : '#FFFFFF',
    'E480' : '#FFFFFF',
    'Half Atlantic Frost' : '#FFFFFF',
    'E481' : '#FFFFFF',
    'Quarter Atlantic Frost' : '#FFFFFF',
    'E482' : '#FFFFFF',
    'Double New Colour Blue' : '#6977FF',
    'E500' : '#6977FF',
    'New Colour Blue (Robertson Blue)' : '#BFC7FB',
    'E501' : '#BFC7FB',
    'Half New Colour Blue' : '#D9E3FF',
    'E502' : '#D9E3FF',
    'Quarter New Colour Blue' : '#F0F5FF',
    'E503' : '#F0F5FF',
    'Waterfront Green' : '#B3DCE3',
    'E504' : '#B3DCE3',
    'Sally Green' : '#BFFF59',
    'E505' : '#BFFF59',
    'Marlene' : '#F7C9A3',
    'E506' : '#F7C9A3',
    'Madge' : '#E93511',
    'E507' : '#E93511',
    'Midnight Maya' : '#1602AA',
    'E508' : '#1602AA',
    'Argent Blue' : '#2261D6',
    'E525' : '#2261D6',
    'Gold Medal' : '#F5AE3F',
    'E550' : '#F5AE3F',
    'Full CT Eight Five' : '#FFC470',
    'E604' : '#FFC470',
    'Half Mustard Yellow' : '#DFAB00',
    'E642' : '#DFAB00',
    'Quarter Mustard Yellow' : '#FDC200',
    'E643' : '#FDC200',
    'Industry Sodium' : '#D9CE73',
    'E650' : '#D9CE73',
    'HI Sodium' : '#FFB95C',
    'E651' : '#FFB95C',
    'Urban Sodium' : '#FF752B',
    'E652' : '#FF752B',
    'LO Sodium' : '#5E2A02',
    'E653' : '#5E2A02',
    'Perfect Lavender' : '#7500EB',
    'E700' : '#7500EB',
    'Provence' : '#9A3BFF',
    'E701' : '#9A3BFF',
    'Special Pale Lavender' : '#DACCFF',
    'E702' : '#DACCFF',
    'Cold Lavender' : '#C587FF',
    'E703' : '#C587FF',
    'Lily' : '#E2BAFF',
    'E704' : '#E2BAFF',
    'Lily Frost' : '#D59EFF',
    'E705' : '#D59EFF',
    'King Fals Lavender' : '#6600FF',
    'E706' : '#6600FF',
    'Ultimate Violet' : '#7500F2',
    'E707' : '#7500F2',
    'Cool Lavender' : '#BFC8FF',
    'E708' : '#BFC8FF',
    'Electric Lilac' : '#7394FF',
    'E709' : '#7394FF',
    'Spir Special Blue' : '#554CFF',
    'E710' : '#554CFF',
    'Cold Blue' : '#224ED4',
    'E711' : '#224ED4',
    'Bedford Blue' : '#3853FF',
    'E712' : '#3853FF',
    'Winter Blue' : '#1F009A',
    'E713' : '#1F009A',
    'Elysian Blue' : '#0F17FF',
    'E714' : '#0F17FF',
    'Cabanna Blue' : '#072EDE',
    'E715' : '#072EDE',
    'Mikkel Blue' : '#2600BF',
    'E716' : '#2600BF',
    'Shanklin Frost' : '#FFFFFF',
    'E717' : '#FFFFFF',
    '1/2 Shanklin Frost' : '#FFFFFF',
    'E718' : '#FFFFFF',
    'Colour Wash Blue' : '#2265F5',
    'E719' : '#2265F5',
    'Daylight Frost' : '#FFFFFF',
    'E720' : '#FFFFFF',
    'Berry Blue' : '#0036E8',
    'E721' : '#0036E8',
    'Bray Blue' : '#0024C2',
    'E722' : '#0024C2',
    'Virgin Blue' : '#0031F7',
    'E723' : '#0031F7',
    'Ocean Blue' : '#2BC7FF',
    'E724' : '#2BC7FF',
    'Old Steel Blue' : '#8CDFFF',
    'E725' : '#8CDFFF',
    'QFD Blue' : '#007385',
    'E727' : '#007385',
    'Steel Green' : '#95DEDA',
    'E728' : '#95DEDA',
    'Scuba Blue' : '#007070',
    'E729' : '#007070',
    'Liberty Green' : '#A3F7DB',
    'E730' : '#A3F7DB',
    'Dirty Ice' : '#B4F0D2',
    'E731' : '#B4F0D2',
    'Damp Squib' : '#A8E5C7',
    'E733' : '#A8E5C7',
    'Velvet Green' : '#005C1D',
    'E735' : '#005C1D',
    'Twickenham Green' : '#0D5700',
    'E736' : '#0D5700',
    'Jas Green' : '#5FE300',
    'E738' : '#5FE300',
    'Aurora Borealis Green' : '#354D15',
    'E740' : '#354D15',
    'Mustard Yellow' : '#C5A100',
    'E741' : '#C5A100',
    'Bram Brown' : '#8E5324',
    'E742' : '#8E5324',
    'Dirty White' : '#F7C757',
    'E744' : '#F7C757',
    'Brown ' : '#753900',
    'E746' : '#753900',
    'Easy White' : '#CC8C7C',
    'E747' : '#CC8C7C',
    'Seedy Pink' : '#C23061',
    'E748' : '#C23061',
    'Hanover Rose' : '#FFBCBA',
    'E749' : '#FFBCBA',
    'Durham Frost' : '#FFFFFF',
    'E750' : '#FFFFFF',
    'Wheat' : '#FFEFBA',
    'E763' : '#FFEFBA',
    'Sun Colour Straw' : '#FFEC94',
    'E764' : '#FFEC94',
    'Sunlight Yellow' : '#FFEC6E',
    'E765' : '#FFEC6E',
    'Oklahoma Yellow' : '#FFDE24',
    'E767' : '#FFDE24',
    'Egg Yolk Yellow' : '#FCC200',
    'E768' : '#FCC200',
    'Burnt Yellow' : '#FF8A0D',
    'E770' : '#FF8A0D',
    'Cardbox Amber' : '#FFB28F',
    'E773' : '#FFB28F',
    'Soft Amber' : '#FFC49C',
    'E774' : '#FFC49C',
    'Soft Amber 2' : '#FFBA8C',
    'E775' : '#FFBA8C',
    'Nectarine' : '#FF8345',
    'E776' : '#FF8345',
    'Rust' : '#D94F18',
    'E777' : '#D94F18',
    'Millennium Gold' : '#FF4405',
    'E778' : '#FF4405',
    'Bastard Pink' : '#F56A2F',
    'E779' : '#F56A2F',
    'As Golden Amber' : '#FF3B05',
    'E780' : '#FF3B05',
    'Terry Red' : '#FF0F0D',
    'E781' : '#FF0F0D',
    'Marius Red' : '#91001B',
    'E787' : '#91001B',
    'Blood Red' : '#99000D',
    'E789' : '#99000D',
    'Moroccan Pink' : '#FF919C',
    'E790' : '#FF919C',
    'Moroccan Frost' : '#FFFFFF',
    'E791' : '#FFFFFF',
    'Vanity Fair' : '#FF12AC',
    'E793' : '#FF12AC',
    'Pretty N Pink' : '#FF82DE',
    'E794' : '#FF82DE',
    'Magical Magenta' : '#FF00C8',
    'E795' : '#FF00C8',
    'Deep Purple' : '#AD00CC',
    'E797' : '#AD00CC',
    'Chrysalis Pink' : '#7B0FFF',
    'E798' : '#7B0FFF',
    'Special K.H. Lavender' : '#120096',
    'E799' : '#120096',
    'Damson Violet' : '#8800C7',
    'E5084' : '#8800C7',
    'French Lilac' : '#6D00F2',
    'E5085' : '#6D00F2',
    'Max Blue' : '#B8D4FF',
    'E5202' : '#B8D4FF',
    'Ice Blue' : '#E8F4FF',
    'E5211' : '#E8F4FF',
    'Venetian Blue' : '#96C9FF',
    'E5264' : '#96C9FF',
    'Fuji Blue' : '#002DE3',
    'E5287' : '#002DE3',
    'Aztec Gold' : '#F2CF88',
    'E5336' : '#F2CF88',
    'Wisteria' : '#DFCFFF',
    'E5404' : '#DFCFFF',
    'Olympia Green' : '#009C72',
    'E5454' : '#009C72',
    'Tarragon' : '#7DFFB1',
    'E5455' : '#7DFFB1',
    'Grotto Green' : '#02BF9C',
    'E5461' : '#02BF9C',
    'Prussian Green' : '#00A6B5',
    'E5463' : '#00A6B5',
# Rosco Supergel
    'Dempster Open White' : '#FFFFFF',
    'R00' : '#FFFFFF',
    'Light Bastard Amber' : '#FBB39A',
    'R01' : '#FBB39A',
    'Bastard Amber' : '#FFD1AC',
    'R02' : '#FFD1AC',
    'Dark Bastard Amber' : '#FBBA9A',
    'R03' : '#FBBA9A',
    'Warm Peach' : '#FF8A4A',
    'R303' : '#FF8A4A',
    'Medium Bastard Amber' : '#F9B09A',
    'R04' : '#F9B09A',
    'Pale Apricot' : '#FABCA9',
    'R304' : '#FABCA9',
    'Rose Tint' : '#FFD7D3',
    'R05' : '#FFD7D3',
    'Rose Gold' : '#F5BAB8',
    'R305' : '#F5BAB8',
    'No Color Straw' : '#FCFADB',
    'R06' : '#FCFADB',
    'Pale Yellow ' : '#FDFAD1',
    'R07' : '#FDFAD1',
    'Pale Amber Gold' : '#FFCB86',
    'R09' : '#FFCB86',
    'Medium Yellow' : '#FFF200',
    'R10' : '#FFF200',
    'Light Straw' : '#FFD21A',
    'R11' : '#FFD21A',
    'Canary' : '#FFEA00',
    'R312' : '#FFEA00',
    'Straw Tint ' : '#FFD88F',
    'R13' : '#FFD88F',
    'Light Relief Yellow' : '#FFE462',
    'R313' : '#FFE462',
    'Medium Straw' : '#FCD419',
    'R14' : '#FCD419',
    'Deep Straw ' : '#FECB00',
    'R15' : '#FECB00',
    'Apricot' : '#FF7418',
    'R317' : '#FF7418',
    'Mayan Sun' : '#FF6F29',
    'R318' : '#FF6F29',
    'Fire' : '#FF390B',
    'R19' : '#FF390B',
    'Medium Amber' : '#FF871C',
    'R20' : '#FF871C',
    'Golden Amber' : '#FF6613',
    'R21' : '#FF6613',
    'Deep Amber' : '#FF430A',
    'R22' : '#FF430A',
    'Orange' : '#FF5A00',
    'R23' : '#FF5A00',
    'Scarlet' : '#F50014',
    'R24' : '#F50014',
    'Gypsy Red' : '#F50F39',
    'R324' : '#F50F39',
    'Orange Red' : '#E51F00',
    'R25' : '#E51F00',
    'Light Red' : '#D70229',
    'R26' : '#D70229',
    'Medium Red' : '#B00202',
    'R27' : '#B00202',
    'Light Salmon Pink' : '#FF7A59',
    'R30' : '#FF7A59',
    'Salmon Pink' : '#FF847F',
    'R31' : '#FF847F',
    'Shell Pink' : '#FF9D8D',
    'R331' : '#FF9D8D',
    'Medium Salmon Pink' : '#FF413C',
    'R32' : '#FF413C',
    'Cherry Rose' : '#FF2957',
    'R332' : '#FF2957',
    'No Color Pink' : '#FFC2D0',
    'R33' : '#FFC2D0',
    'Light Pink' : '#FFA7BB',
    'R35' : '#FFA7BB',
    'Medium Pink' : '#FF6D96',
    'R36' : '#FF6D96',
    'Billington Pink' : '#FF73B7',
    'R336' : '#FF73B7',
    'True Pink' : '#FFAFC2',
    'R337' : '#FFAFC2',
    'Light Rose' : '#FFBBE2',
    'R38' : '#FFBBE2',
    'Broadway Pink' : '#FF1283',
    'R339' : '#FF1283',
    'Skelton Exotic Sangria' : '#E800BC',
    'R39' : '#E800BC',
    'Light Salmon' : '#FF4F1F',
    'R40' : '#FF4F1F',
    'Rose Pink' : '#FF1562',
    'R342' : '#FF1562',
    'Deep Pink' : '#FF3E93',
    'R43' : '#FF3E93',
    'Neon Pink' : '#FF397F',
    'R343' : '#FF397F',
    'Follies Pink' : '#FF05D3',
    'R344' : '#FF05D3',
    'Rose' : '#EB016D',
    'R45' : '#EB016D',
    'Magenta' : '#BD045D',
    'R46' : '#BD045D',
    'Tropical Magenta' : '#FF2DD5',
    'R346' : '#FF2DD5',
    'Light Rose Purple' : '#CC4EB9',
    'R47' : '#CC4EB9',
    'Belladonna Rose' : '#B101DD',
    'R347' : '#B101DD',
    'Rose Purple' : '#C800CF',
    'R48' : '#C800CF',
    'Purple Jazz' : '#DA2DFF',
    'R348' : '#DA2DFF',
    'Medium Purple' : '#C900E6',
    'R49' : '#C900E6',
    'Fisher Fuchsia' : '#F000FF',
    'R349' : '#F000FF',
    'Mauve' : '#BB002C',
    'R50' : '#BB002C',
    'Lavender Mist' : '#EFDCFF',
    'R351' : '#EFDCFF',
    'Light Lavender' : '#DDBFFF',
    'R52' : '#DDBFFF',
    'Pale Lavender' : '#E4DCFF',
    'R53' : '#E4DCFF',
    'Lilly Lavender' : '#C4ADFF',
    'R353' : '#C4ADFF',
    'Special Lavender' : '#E6C7FF',
    'R54' : '#E6C7FF',
    'Lilac' : '#C0AAFD',
    'R55' : '#C0AAFD',
    'Pale Violet' : '#A590FF',
    'R355' : '#A590FF',
    'Gypsy Lavender' : '#8C2FFF',
    'R56' : '#8C2FFF',
    'Middle Lavender' : '#C38DFF',
    'R356' : '#C38DFF',
    'Lavender' : '#B482FF',
    'R57' : '#B482FF',
    'Royal Lavender' : '#8A2BFF',
    'R357' : '#8A2BFF',
    'Deep Lavender' : '#933FFD',
    'R58' : '#933FFD',
    'Rose Indigo' : '#8E0AEA',
    'R358' : '#8E0AEA',
    'Indigo' : '#7200FF',
    'R59' : '#7200FF',
    'Medium Violet' : '#683FFF',
    'R359' : '#683FFF',
    'Mist Blue' : '#D3EAFF',
    'R61' : '#D3EAFF',
    'Hemsley Blue' : '#669EFC',
    'R361' : '#669EFC',
    'Booster Blue' : '#A1CEFF',
    'R62' : '#A1CEFF',
    'Pale Blue' : '#A4D3FF',
    'R63' : '#A4D3FF',
    'Aquamarine' : '#ABE9FF',
    'R363' : '#ABE9FF',
    'Light Steel Blue' : '#50AEFD',
    'R64' : '#50AEFD',
    'Daylight Blue' : '#00A9FF',
    'R65' : '#00A9FF',
    'Cool Blue' : '#94EAFF',
    'R66' : '#94EAFF',
    'Jordan Blue' : '#29C0F9',
    'R366' : '#29C0F9',
    'Light Sky Blue' : '#14A9FF',
    'R67' : '#14A9FF',
    'Slate Blue' : '#44A5FF',
    'R367' : '#44A5FF',
    'Parry Sky Blue' : '#447DFF',
    'R68' : '#447DFF',
    'Winkler Blue' : '#448AFF',
    'R368' : '#448AFF',
    'Brilliant Blue' : '#00A3F7',
    'R69' : '#00A3F7',
    'Tahitian Blue' : '#00C6FF',
    'R369' : '#00C6FF',
    'Nile Blue' : '#6CE5FF',
    'R70' : '#6CE5FF',
    'Italian Blue' : '#01CDDF',
    'R370' : '#01CDDF',
    'Sea Blue' : '#0096C7',
    'R71' : '#0096C7',
    'Theatre Booster 1' : '#A3A8FF',
    'R371' : '#A3A8FF',
    'Azure Blue' : '#55CCFF',
    'R72' : '#55CCFF',
    'Theatre Booster 2' : '#D9DCFF',
    'R372' : '#D9DCFF',
    'Peacock Blue' : '#00A4B8',
    'R73' : '#00A4B8',
    'Theatre Booster 3' : '#E0E9FD',
    'R373' : '#E0E9FD',
    'Night Blue' : '#4200FF',
    'R74' : '#4200FF',
    'Sea Green' : '#01A4A6',
    'R374' : '#01A4A6',
    'Twilight Blue' : '#007AAC',
    'R75' : '#007AAC',
    'Light Green Blue' : '#005773',
    'R76' : '#005773',
    'Iris Purple' : '#7124FF',
    'R377' : '#7124FF',
    'Trudy Blue' : '#6F6FFF',
    'R78' : '#6F6FFF',
    'Bright Blue' : '#1626FF',
    'R79' : '#1626FF',
    'Primary Blue' : '#0048FF',
    'R80' : '#0048FF',
    'Urban Blue' : '#486FFF',
    'R81' : '#486FFF',
    'Surprise Blue' : '#4F34F8',
    'R82' : '#4F34F8',
    'Congo Blue' : '#250070',
    'R382' : '#250070',
    'Medium Blue' : '#0228EC',
    'R83' : '#0228EC',
    'Sapphire Blue' : '#0022D1',
    'R383' : '#0022D1',
    'Zephyr Blue' : '#5767FF',
    'R84' : '#5767FF',
    'Midnight Blue' : '#0500D0',
    'R384' : '#0500D0',
    'Deep Blue' : '#0049CE',
    'R85' : '#0049CE',
    'Royal Blue' : '#4F02CF',
    'R385' : '#4F02CF',
    'Pea Green' : '#89FA19',
    'R86' : '#89FA19',
    'Leaf Green' : '#7BD300',
    'R386' : '#7BD300',
    'Gaslight Green' : '#D0F54E',
    'R388' : '#D0F54E',
    'Moss Green' : '#51F655',
    'R89' : '#51F655',
    'Chroma Green' : '#29F433',
    'R389' : '#29F433',
    'Dark Yellow Green' : '#007F06',
    'R90' : '#007F06',
    'Primary Green' : '#005E2C',
    'R91' : '#005E2C',
    'Pacific Green' : '#009493',
    'R392' : '#009493',
    'Blue Green' : '#01A3A0',
    'R93' : '#01A3A0',
    'Emerald Green' : '#007150',
    'R393' : '#007150',
    'Kelly Green' : '#00985D',
    'R94' : '#00985D',
    'Medium Blue Green' : '#009C91',
    'R95' : '#009C91',
    'Teal Green' : '#00726A',
    'R395' : '#00726A',
    'Lime' : '#F3FF6B',
    'R96' : '#F3FF6B',
    'Neutral Grey' : '#B0B4B9',
    'R398' : '#B0B4B9',
    'Frost' : '#FFFFFF',
    'R100' : '#FFFFFF',
    'Light Frost' : '#FFFFFF',
    'R101' : '#FFFFFF',
    'Tough Silk' : '#FFFFFF',
    'R104' : '#FFFFFF',
    'Matte Silk' : '#FFFFFF',
    'R113' : '#FFFFFF',
    'Hamburg Frost' : '#FFFFFF',
    'R114' : '#FFFFFF',
    'Light Hamburg Frost' : '#FFFFFF',
    'R119' : '#FFFFFF',
    'Red Diffusion' : '#FFFFFF',
    'R120' : '#FFFFFF',
    'Blue Diffusion' : '#FFFFFF',
    'R121' : '#FFFFFF',
    'Green Diffusion' : '#FFFFFF',
    'R122' : '#FFFFFF',
    'Red Cyc Silk' : '#FFFFFF',
    'R124' : '#FFFFFF',
    'Blue Cyc Silk' : '#FFFFFF',
    'R125' : '#FFFFFF',
    'Green Cyc Silk' : '#FFFFFF',
    'R126' : '#FFFFFF',
    'Amber Cyc Silk' : '#FFFFFF',
    'R127' : '#FFFFFF',
    'Quarter Hamburg Frost' : '#FFFFFF',
    'R132' : '#FFFFFF',
    'Subtle Hamburg Frost' : '#FFFFFF',
    'R140' : '#FFFFFF',
    'Light Tough Silk' : '#FFFFFF',
    'R160' : '#FFFFFF',
# HTML standard colours
    'AliceBlue': '#F0F8FF',
    'AntiqueWhite': '#FAEBD7',
    'Aqua': '#00FFFF',
    'Aquamarine': '#7FFFD4',
    'Azure': '#F0FFFF',
    'Beige': '#F5F5DC',
    'Bisque': '#FFE4C4',
    'Black': '#000000',
    'BlanchedAlmond': '#FFEBCD',
    'Blue': '#0000FF',
    'BlueViolet': '#8A2BE2',
    'Brown': '#A52A2A',
    'BurlyWood': '#DEB887',
    'CadetBlue': '#5F9EA0',
    'Chartreuse': '#7FFF00',
    'Chocolate': '#D2691E',
    'Coral': '#FF7F50',
    'CornflowerBlue': '#6495ED',
    'Cornsilk': '#FFF8DC',
    'Crimson': '#DC143C',
    'Cyan': '#00FFFF',
    'DarkBlue': '#00008B',
    'DarkCyan': '#008B8B',
    'DarkGoldenrod': '#B8860B',
    'DarkGray': '#A9A9A9',
    'DarkGreen': '#006400',
    'DarkKhaki': '#BDB76B',
    'DarkMagenta': '#8B008B',
    'DarkOliveGreen': '#556B2F',
    'DarkOrange': '#FF8C00',
    'DarkOrchid': '#9932CC',
    'DarkRed': '#8B0000',
    'DarkSalmon': '#E9967A',
    'DarkSeaGreen': '#8FBC8F',
    'DarkSlateBlue': '#483D8B',
    'DarkSlateGray': '#2F4F4F',
    'DarkTurquoise': '#00CED1',
    'DarkViolet': '#9400D3',
    'DeepPink': '#FF1493',
    'DeepSkyBlue': '#00BFFF',
    'DimGray': '#696969',
    'DodgerBlue': '#1E90FF',
    'FireBrick': '#B22222',
    'FloralWhite': '#FFFAF0',
    'ForestGreen': '#228B22',
    'Fuchsia': '#FF00FF',
    'Gainsboro': '#DCDCDC',
    'GhostWhite': '#F8F8FF',
    'Gold': '#FFD700',
    'Goldenrod': '#DAA520',
    'Gray': '#808080',
    'Green': '#008000',
    'GreenYellow': '#ADFF2F',
    'Honeydew': '#F0FFF0',
    'HotPink': '#FF69B4',
    'IndianRed': '#CD5C5C',
    'Indigo': '#4B0082',
    'Ivory': '#FFFFF0',
    'Khaki': '#F0E68C',
    'Lavender': '#E6E6FA',
    'LavenderBlush': '#FFF0F5',
    'LawnGreen': '#7CFC00',
    'LemonChiffon': '#FFFACD',
    'LightBlue': '#ADD8E6',
    'LightCoral': '#F08080',
    'LightCyan': '#E0FFFF',
    'LightGoldenrodYellow': '#FAFAD2',
    'LightGreen': '#90EE90',
    'LightGrey': '#D3D3D3',
    'LightPink': '#FFB6C1',
    'LightSalmon': '#FFA07A',
    'LightSeaGreen': '#20B2AA',
    'LightSkyBlue': '#87CEFA',
    'LightSlateGray': '#778899',
    'LightSteelBlue': '#B0C4DE',
    'LightYellow': '#FFFFE0',
    'Lime': '#00FF00',
    'LimeGreen': '#32CD32',
    'Linen': '#FAF0E6',
    'Magenta': '#FF00FF',
    'Maroon': '#800000',
    'MediumAquamarine': '#66CDAA',
    'MediumBlue': '#0000CD',
    'MediumOrchid': '#BA55D3',
    'MediumPurple': '#9370DB',
    'MediumSeaGreen': '#3CB371',
    'MediumSlateBlue': '#7B68EE',
    'MediumSpringGreen': '#00FA9A',
    'MediumTurquoise': '#48D1CC',
    'MediumVioletRed': '#C71585',
    'MidnightBlue': '#191970',
    'MintCream': '#F5FFFA',
    'MistyRose': '#FFE4E1',
    'Moccasin': '#FFE4B5',
    'NavajoWhite': '#FFDEAD',
    'Navy': '#000080',
    'OldLace': '#FDF5E6',
    'Olive': '#808000',
    'OliveDrab': '#6B8E23',
    'Orange': '#FFA500',
    'OrangeRed': '#FF4500',
    'Orchid': '#DA70D6',
    'PaleGoldenrod': '#EEE8AA',
    'PaleGreen': '#98FB98',
    'PaleTurquoise': '#AFEEEE',
    'PaleVioletRed': '#DB7093',
    'PapayaWhip': '#FFEFD5',
    'PeachPuff': '#FFDAB9',
    'Peru': '#CD853F',
    'Pink': '#FFC0CB',
    'Plum': '#DDA0DD',
    'PowderBlue': '#B0E0E6',
    'Purple': '#800080',
    'Red': '#FF0000',
    'RosyBrown': '#BC8F8F',
    'RoyalBlue': '#4169E1',
    'SaddleBrown': '#8B4513',
    'Salmon': '#FA8072',
    'SandyBrown': '#F4A460',
    'SeaGreen': '#2E8B57',
    'Seashell': '#FFF5EE',
    'Sienna': '#A0522D',
    'Silver': '#C0C0C0',
    'SkyBlue': '#87CEEB',
    'SlateBlue': '#6A5ACD',
    'SlateGray': '#708090',
    'Snow': '#FFFAFA',
    'SpringGreen': '#00FF7F',
    'SteelBlue': '#4682B4',
    'Tan': '#D2B48C',
    'Teal': '#008080',
    'Thistle': '#D8BFD8',
    'Tomato': '#FF6347',
    'Turquoise': '#40E0D0',
    'Violet': '#EE82EE',
    'Wheat': '#F5DEB3',
    'White': '#FFFFFF',
    'WhiteSmoke': '#F5F5F5',
    'Yellow': '#FFFF00',
    'YellowGreen': '#9ACD32'
}
