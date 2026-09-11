import json 

with open('pattern.json','r') as f:
    data = json.load(f)

data['created_by'] = 'ahmad@gmail.com'

with open('pattern.json','w') as f:
    json.dump(data,f,indent=4)


