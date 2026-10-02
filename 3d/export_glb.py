import json,struct,math
from pathlib import Path
clips=json.loads(Path('assets/animations.json').read_text())
for name in ['hero','monster','lightning','trinity']:
 data=json.loads(Path('assets/'+name+'.json').read_text());blob=bytearray();views=[];access=[]
 def acc(values,typ,component=5126,bounds=False):
  while len(blob)%4:blob.append(0)
  start=len(blob);size={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[typ];fmt={5126:'f',5123:'H'}[component]
  blob.extend(struct.pack('<'+fmt*len(values),*values));views.append({'buffer':0,'byteOffset':start,'byteLength':len(blob)-start});a={'bufferView':len(views)-1,'componentType':component,'count':len(values)//size,'type':typ}
  if bounds:a.update(min=[min(values[i::size]) for i in range(size)],max=[max(values[i::size]) for i in range(size)])
  access.append(a);return len(access)-1
 v=data['vertices'];rows=[v[i:i+15] for i in range(0,len(v),15)]
 attrs={'POSITION':acc([x for r in rows for x in r[:3]],'VEC3',bounds=True),'NORMAL':acc([x for r in rows for x in r[3:6]],'VEC3'),'COLOR_0':acc([x for r in rows for x in r[6:9]],'VEC3'),'JOINTS_0':acc([int(x) for r in rows for x in [r[9],r[10],0,0]],'VEC4',5123),'WEIGHTS_0':acc([x for r in rows for x in [r[11],r[12],0,0]],'VEC4')}
 ix=acc(data['indices'],'SCALAR',5123);nodes=[];inv=[]
 for i,b in enumerate(data['bones']):
  par=b['parent'];o=b['origin'];p=[0,0,0] if par<0 else data['bones'][par]['origin'];nodes.append({'name':b['name'],'translation':[o[k]-p[k] for k in range(3)]});children=[j for j,n in enumerate(data['bones']) if n['parent']==i]
  if children:nodes[-1]['children']=children
  inv.extend([1,0,0,0,0,1,0,0,0,0,1,0,-o[0],-o[1],-o[2],1])
 invAcc=acc(inv,'MAT4');nodes.append({'name':data['name'],'mesh':0,'skin':0});animations=[]
 for cname,clip in clips.items():
  times=acc([k[0] for k in clip['keys']],'SCALAR',bounds=True);samplers=[];channels=[]
  for i,b in enumerate(data['bones']):
   quats=[]
   for t,pose in clip['keys']:
    x,y,z=[v/2 for v in pose.get(b['name'],[0,0,0])];cx,cy,cz=math.cos(x),math.cos(y),math.cos(z);sx,sy,sz=math.sin(x),math.sin(y),math.sin(z)
    quats.extend([sx*cy*cz+cx*sy*sz,cx*sy*cz-sx*cy*sz,cx*cy*sz+sx*sy*cz,cx*cy*cz-sx*sy*sz])
   samplers.append({'input':times,'output':acc(quats,'VEC4'),'interpolation':'LINEAR'});channels.append({'sampler':i,'target':{'node':i,'path':'rotation'}})
  animations.append({'name':cname,'samplers':samplers,'channels':channels})
 gltf={'asset':{'version':'2.0','generator':'Sihan original rig prototype'},'scene':0,'scenes':[{'nodes':[0,16]}],'nodes':nodes,'meshes':[{'primitives':[{'attributes':attrs,'indices':ix,'material':0}]}],'materials':[{'pbrMetallicRoughness':{'metallicFactor':.65,'roughnessFactor':.34},'doubleSided':True}],'skins':[{'joints':list(range(16)),'inverseBindMatrices':invAcc,'skeleton':0}],'animations':animations,'buffers':[{'byteLength':len(blob)}],'bufferViews':views,'accessors':access}
 j=json.dumps(gltf,separators=(',',':')).encode();j+=b' '*((-len(j))%4);blob.extend(b'\0'*((-len(blob))%4));out=struct.pack('<III',0x46546c67,2,12+8+len(j)+8+len(blob))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(blob),0x004e4942)+blob;Path('assets/'+name+'.glb').write_bytes(out)
 print(name,len(out),'bytes / 16 joints /',len(animations),'animation clips')
