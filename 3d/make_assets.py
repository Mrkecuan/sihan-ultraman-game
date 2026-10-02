import json,math,wave,struct,random
from pathlib import Path
random.seed(42)
# Joint origins in bind space. Every vertex carries joint indices and normalized weights.
bones=[('hips',-1,[0,1.05,0]),('spine',0,[0,1.30,0]),('chest',1,[0,1.65,0]),('head',2,[0,2.05,0]),('shoulderL',2,[-.43,1.8,0]),('elbowL',4,[-.52,1.36,0]),('handL',5,[-.53,.99,0]),('shoulderR',2,[.43,1.8,0]),('elbowR',7,[.52,1.36,0]),('handR',8,[.53,.99,0]),('thighL',0,[-.20,1.04,0]),('kneeL',10,[-.20,.57,0]),('footL',11,[-.20,.10,.07]),('thighR',0,[.20,1.04,0]),('kneeR',13,[.20,.57,0]),('footR',14,[.20,.10,.07])]
def model(monster=False,variant="hero"):
 v=[];idx=[]
 silver=[.68,.76,.84];red=[.66,.035,.07];dark=[.055,.085,.13];gold=[.9,.52,.11];blue=[.05,.75,1.]
 if variant=="lightning":red=[.025,.16,.32];gold=[.76,.88,.96];blue=[.05,.65,1.]
 if variant=="trinity":red=[.12,.065,.09];silver=[.79,.64,.35];gold=[.95,.70,.20];blue=[.08,.70,.98]
 if monster:silver=[.24,.33,.30];red=[.36,.19,.10];dark=[.12,.15,.13];gold=[.7,.38,.09];blue=[1.,.24,.035]
 def ell(c,r,col,j,blend=None,seg=16,rings=10):
  start=len(v)//15
  for iy in range(rings+1):
   a=iy/rings*math.pi
   for ix in range(seg+1):
    b=ix/seg*math.tau;n=[math.sin(a)*math.cos(b),math.cos(a),math.sin(a)*math.sin(b)];p=[c[k]+n[k]*r[k] for k in range(3)];wt=1.
    if blend:wt=max(.05,min(.95,(p[1]-blend[1])/.2+.5))
    v.extend(p+n+col+[j,blend[0] if blend else j,wt,1-wt,0,0])
  for iy in range(rings):
   for ix in range(seg):
    q=start+iy*(seg+1)+ix;idx.extend([q,q+1,q+seg+1,q+1,q+seg+2,q+seg+1])
 if not monster:
  # Tailored continuous suit sections, hard-surface chest and helmet plates.
  def tube(cx,cz,profile,col,j,blend=None):
   start=len(v)//15;segs=24
   for yy,rx,rz in profile:
    for n in range(segs+1):
     a=n/segs*math.tau;nx,nz=math.cos(a),math.sin(a);wt=1 if not blend else max(0,min(1,(yy-blend[1])/.16+.5))
     v.extend([cx+rx*nx,yy,cz+rz*nz,nx,0,nz,*col,j,blend[0] if blend else j,wt,1-wt,0,0])
   for k in range(len(profile)-1):
    for n in range(segs):
     q=start+k*(segs+1)+n;idx.extend([q,q+1,q+segs+1,q+1,q+segs+2,q+segs+1])
  def plate(points,col,j):
   start=len(v)//15;c=[sum(p[k] for p in points)/len(points) for k in range(3)]
   for p in [c]+points:v.extend([*p,0,0,1,*col,j,j,1,0,0,0])
   for n in range(len(points)):idx.extend([start,start+1+n,start+1+(n+1)%len(points)])
  tube(0,0,[(1.02,.25,.16),(1.15,.25,.16),(1.35,.23,.15),(1.5,.28,.18),(1.73,.36,.205),(1.85,.34,.18),(1.94,.15,.12)],red,2,(1,1.47))
  tube(0,0,[(1.02,.24,.14),(1.10,.27,.17),(1.2,.24,.16)],dark,0)
  ell([0,1.035,0],[.29,.15,.165],dark,0)
  ell([0,1.96,0],[.10,.12,.10],dark,3)
  ell([0,2.16,0],[.175,.235,.16],silver,3,seg=28,rings=18)
  # Almond lenses lie on the helmet surface; jaw and mouth are separate hard plates.
  for side in [-1,1]:
   plate([[side*.025,2.19,.16],[side*.115,2.245,.139],[side*.167,2.205,.094],[side*.123,2.165,.144],[side*.052,2.166,.162]],[1.8,2.0,2.2],3)
   plate([[side*.035,2.12,.157],[side*.13,2.105,.12],[side*.087,1.999,.108],[side*.025,2.04,.157]],[.40,.49,.59],3)
   plate([[side*.04,1.63,.21],[side*.31,1.88,.153],[side*.35,1.77,.18],[side*.11,1.54,.197]],silver,2)
   plate([[side*.10,1.56,.195],[side*.34,1.74,.18],[side*.30,1.63,.19],[side*.13,1.44,.18]],[.10,.28,.47],2)
  plate([[-.055,2.095,.162],[.055,2.095,.162],[.040,2.079,.164],[-.040,2.079,.164]],dark,3)
  plate([[-.023,2.12,.163],[-.029,2.40,0],[0,2.46,-.04],[.029,2.40,0],[.023,2.12,.163]],[.78,.85,.91],3)
  ell([0,2.27,.166],[.019,.047,.009],[1.,.055,.06],3)
  ell([0,1.72,.21],[.070,.086,.026],gold,2)
  ell([0,1.72,.238],[.050,.062,.012],blue,2)
  for side,sh,el,hand,hip,knee,foot in [(-1,4,5,6,10,11,12),(1,7,8,9,13,14,15)]:
   ell([side*.43,1.79,0],[.135,.145,.143],silver,sh)
   tube(side*.49,0,[(1.35,.075,.08),(1.46,.10,.11),(1.67,.11,.12),(1.79,.10,.10)],red,sh,(el,1.38))
   ell([side*.52,1.36,0],[.080,.09,.083],dark,el)
   tube(side*.52,0,[(1.015,.073,.078),(1.12,.087,.09),(1.27,.11,.11),(1.37,.081,.085)],silver,el,(hand,1.04))
   ell([side*.53,1.0,.035],[.082,.105,.095],silver,hand)
   tube(side*.20,0,[(.55,.092,.105),(.66,.116,.12),(.89,.134,.145),(1.05,.125,.13)],red,hip,(knee,.59))
   ell([side*.20,.57,0],[.092,.105,.10],dark,knee)
   plate([[side*.20-.076,.65,.099],[side*.20+.076,.65,.099],[side*.20+.06,.50,.107],[side*.20-.06,.50,.107]],silver,knee)
   tube(side*.20,0,[(.13,.078,.085),(.25,.094,.098),(.43,.102,.11),(.54,.088,.092)],silver,knee,(foot,.15))
   ell([side*.20,.095,.12],[.09,.09,.19],red,foot)
  if variant!='hero':
   for side in [-1,1]:
    plate([[side*.13,2.20,.10],[side*.23,2.43,-.01],[side*.18,2.47,-.04],[side*.08,2.28,.145]],silver,3)
   plate([[-.03,2.17,.168],[0,2.45,.08],[.03,2.17,.168]],blue if variant=='trinity' else [1,.025,.04],3)
  return {'name':{'hero':'思翰 · 赤曜装甲','lightning':'欧布 · 闪电装甲','trinity':'欧布 · 三重装甲'}[variant],'bones':[{'name':n,'parent':p,'origin':o} for n,p,o in bones],'stride':15,'vertices':[round(x,5) for x in v],'indices':idx}
 ell([0,1.28,0],[.29,.32,.18],dark,1,(0,1.16));ell([0,1.68,0],[.42,.36,.23],red,2,(1,1.45));ell([0,1.08,0],[.30,.17,.18],silver,0)
 ell([0,2.12,0],[.24,.31,.22],silver,3);ell([0,1.93,0],[.12,.14,.12],dark,3)
 # chest plates and luminous timer
 for side in [-1,1]:
  ell([side*.20,1.80,.18],[.21,.105,.055],silver,2);ell([side*.14,2.19,.183],[.092,.058,.055],gold if not monster else blue,3)
 ell([0,1.70,.23],[.095,.105,.035],gold,2);ell([0,1.70,.261],[.067,.075,.018],blue,2)
 ell([0,2.36,0],[.045,.17,.17],red if not monster else gold,3)
 for side,sh,el,hand,hip,knee,foot in [(-1,4,5,6,10,11,12),(1,7,8,9,13,14,15)]:
  ell([side*.43,1.79,0],[.19,.17,.21],silver,sh)
  ell([side*.49,1.57,0],[.105,.26,.115],red,sh,(el,1.38))
  ell([side*.52,1.24,0],[.105,.22,.12],silver,el,(hand,1.06))
  ell([side*.53,1.01,.018],[.12,.13,.13],dark if monster else silver,hand)
  ell([side*.20,.83,0],[.155,.32,.17],red,hip,(knee,.59));ell([side*.20,.58,.1],[.125,.125,.10],silver,knee)
  ell([side*.20,.32,0],[.115,.26,.13],silver,knee,(foot,.15));ell([side*.20,.09,.12],[.13,.10,.23],red,foot)
  if monster:
   for n in range(3):ell([side*(.41+n*.07),1.94+n*.09,-.03],[.10,.23,.10],gold,sh)
   ell([side*.20,2.37,0],[.075,.30,.10],gold,3)
 if monster:
  for n in range(5):ell([0,1.10-n*.12,-.18-n*.15],[.18-n*.024,.16-n*.018,.20],red,0)
 return {'name':'熔甲兽' if monster else '光之守护者','bones':[{'name':n,'parent':p,'origin':o} for n,p,o in bones],'stride':15,'vertices':[round(x,5) for x in v],'indices':idx}
for name,m in [('hero',False),('monster',True),('lightning',False),('trinity',False)]:Path('assets/'+name+'.json').write_text(json.dumps(model(m,name if not m else 'hero'),separators=(',',':')))
# Authored clips: angles in radians, interpolated in game with a transition blend.
clips={
'idle':{'duration':2.4,'loop':True,'keys':[[0,{'spine':[.025,0,0],'shoulderL':[.05,0,-.10],'shoulderR':[.05,0,.10]}],[1.2,{'spine':[-.025,0,0],'shoulderL':[-.03,0,-.08],'shoulderR':[-.03,0,.08]}],[2.4,{'spine':[.025,0,0],'shoulderL':[.05,0,-.10],'shoulderR':[.05,0,.10]}]]},
'run':{'duration':.65,'loop':True,'keys':[[0,{'thighL':[.8,0,0],'thighR':[-.65,0,0],'kneeL':[-.3,0,0],'kneeR':[-1.,0,0],'shoulderL':[-.7,0,-.12],'shoulderR':[.7,0,.12],'spine':[.10,0,0]}],[.325,{'thighL':[-.65,0,0],'thighR':[.8,0,0],'kneeL':[-1.,0,0],'kneeR':[-.3,0,0],'shoulderL':[.7,0,-.12],'shoulderR':[-.7,0,.12],'spine':[.10,0,0]}],[.65,{'thighL':[.8,0,0],'thighR':[-.65,0,0],'kneeL':[-.3,0,0],'kneeR':[-1.,0,0],'shoulderL':[-.7,0,-.12],'shoulderR':[.7,0,.12],'spine':[.10,0,0]}]]},
'punch':{'duration':.55,'keys':[[0,{}],[.14,{'chest':[0,-.55,0],'shoulderR':[-.5,0,.4],'elbowR':[-1.4,0,0],'shoulderL':[-.7,0,-.2],'elbowL':[-1.3,0,0]}],[.25,{'chest':[0,.5,0],'shoulderR':[-1.5,0,-.15],'elbowR':[-.12,0,0],'thighL':[-.2,0,0]}],[.55,{}]]},
'kick':{'duration':.75,'keys':[[0,{}],[.22,{'thighR':[-1.4,0,0],'kneeR':[-1.2,0,0],'spine':[-.15,0,0]}],[.36,{'thighR':[-1.7,0,0],'kneeR':[-.12,0,0],'chest':[0,.4,0],'shoulderL':[-.5,0,-.7]}],[.75,{}]]},
'jump':{'duration':.8,'keys':[[0,{'thighL':[-.5,0,0],'kneeL':[-1.,0,0],'thighR':[-.6,0,0],'kneeR':[-1.1,0,0]}],[.35,{'shoulderL':[-2.,0,-.2],'shoulderR':[-2.,0,.2],'thighR':[-.5,0,0],'kneeR':[-.8,0,0]}],[.8,{}]]},
'dodge':{'duration':.45,'keys':[[0,{}],[.12,{'spine':[.7,0,0],'thighL':[-.8,0,0],'kneeL':[-1.2,0,0],'shoulderL':[.7,0,-.2],'shoulderR':[.7,0,.2]}],[.32,{'spine':[.4,0,0],'thighR':[-.6,0,0],'kneeR':[-1.,0,0]}],[.45,{}]]},
'ult':{'duration':2.7,'keys':[[0,{}],[.55,{'shoulderL':[-2.8,0,-.2],'shoulderR':[-2.8,0,.2],'chest':[-.15,0,0]}],[1.0,{'shoulderL':[-1.3,0,-.8],'shoulderR':[-1.3,0,.8],'elbowL':[-1.5,0,0],'elbowR':[-1.5,0,0]}],[1.35,{'shoulderL':[-1.5,0,-.2],'shoulderR':[-1.5,0,.2],'elbowL':[-.25,0,0],'elbowR':[-.25,0,0],'chest':[.12,0,0]}],[2.2,{'shoulderL':[-1.5,0,-.2],'shoulderR':[-1.5,0,.2],'chest':[.12,0,0]}],[2.7,{}]]},
'hurt':{'duration':.35,'keys':[[0,{}],[.10,{'spine':[-.25,0,0],'head':[.2,0,0],'shoulderL':[0,0,-.3],'shoulderR':[0,0,.3]}],[.35,{}]]},
'grab':{'duration':.9,'keys':[[0,{}],[.2,{'shoulderL':[-1.3,0,-.2],'shoulderR':[-1.3,0,.2]}],[.55,{'shoulderL':[-2.5,0,-.4],'shoulderR':[-2.5,0,.4],'spine':[-.15,0,0]}],[.75,{'shoulderL':[-1.2,0,-.1],'shoulderR':[-1.2,0,.1],'spine':[.25,0,0]}],[.9,{}]]}}
# Correct knees to bend backward; avoid lower legs folding through thighs.
for clip in clips.values():
 for _,pose in clip['keys']:
  for joint in ['kneeL','kneeR']:
   if joint in pose:pose[joint][0]=abs(pose[joint][0])
Path('assets/animations.json').write_text(json.dumps(clips,separators=(',',':')))
for name,dur,freq in [('punch',.16,95),('whoosh',.28,330),('charge',1.2,150),('blast',.7,65),('step',.07,70),('hit',.2,120)]:
 data=[];rate=22050
 for i in range(int(dur*rate)):
  t=i/rate;q=t/dur;env=(1-q)**2*min(1,t/.008);noise=random.uniform(-1,1)
  f=freq*(1+q*3 if name=='charge' else 1-q*.6)
  v=(math.sin(math.tau*f*t)*.45+noise*(.12 if name=='charge' else .5))*env*.45
  data.append(struct.pack('<h',int(max(-1,min(1,v))*32767)))
 with wave.open('assets/audio/'+name+'.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(b''.join(data))
print('Created two weighted 16-bone meshes, nine clips and six original WAV effects')
