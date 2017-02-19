import time
import ort

d = time.time()
#print 'No obscenity: What a splendid day. I can\'t wait to see my love'
#print(ort.rankText('What a splendid day. I can\'t wait to see my love'))
#print('\n')

#print 'Little obscenity: I\'m so fucking mad right now. I need help'
#print(ort.rankText('I\'m so fucking mad right now. I need help'))
#print('\n')

#print 'Little obscenity: Fuck the broncos'
#print(ort.rankText('Fuck the broncos'))
#print('\n')

#print 'Moderate obscenity with meaning: Fuck trump man, nigga is gay af and can suck a dick '
#print(ort.rankText('Fuck trump man, nigga is gay af and can suck a dick'))

print ort.rankText('@demgndboiz u put me on something 💪🏿💪🏿 shit 🔥 @rontuckergnd #imjustdifferent #philly #iremember\u2026 https://t.co/0BDgFFtlv9')
#print(rankText('dick ass fuck'))
#print('\n')
#print rankText('long dick in my ass fuck')
#print('\n')
#print rankText('sexy little lady, god damn')
#print('\n')
#print('\n')
#print(rankText('Did you cum in me!? Fuck you did huh you know what FUCK YOU fuck you fuck you, you fucking asshole.'))
#print('\n')
print(time.time() - d)
