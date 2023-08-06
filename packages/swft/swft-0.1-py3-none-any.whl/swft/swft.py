import pandas as pd
import re
import warnings

DESC = re.compile(r'# +([^ :\n]+)(?: *: *([^ \(\n]+)(?: *\(([^ ,\n]+)(?:, *([^ \)\n]+))?\))?)? *\n?')
UNIT = re.compile(r'(.+) \[([^\]]+)\]')


def load(path):

    warnings.filterwarnings('ignore', category=UserWarning)

    tables = {}
    lineNo = 0
    with open(path) as file:
        while True:
            line = file.readline()

            if line.startswith('#'):
                name = ''
                desc = {}
                m = DESC.fullmatch(line)
                if not m:
                    raise RuntimeError('Invalid table description: "'+line+'"')
                name = m.group(1)
                desc['child'] = m.group(2)
                desc['idCol'] = m.group(3)
                desc['posCol'] = m.group(4)
                if desc['child'] and not desc['idCol']:
                    desc['idCol'] = name+'.id'
                
                header = file.readline()[:-1].split('\t')
                units = ['']*len(header)
                for i in range(len(header)):
                    m = UNIT.fullmatch(header[i])
                    if m:
                        units[i] = m.group(2)
                        header[i] = m.group(1)
                    
                desc['header'] = header
                desc['units'] = units

                desc['start'] = lineNo + 2
                count = 0
                while True:
                    line = file.readline()
                    if not line or line == '\n':
                        break
                    count += 1
                desc["count"] = count

                tables[name] = desc
                lineNo = lineNo + count + 2
                
            if not line:
                break

            lineNo += 1
    
    data = {}
    for name, desc in tables.items():

        if desc['child']:
            if not desc['child'] in tables:
                raise RuntimeError('Child table not in data set: "'+desc['child']+'"')
            if desc['idCol'] not in tables[desc['child']]['header']:
                raise RuntimeError('Invalid ID column: No column "'+desc['idCol']+'" in table "'+desc['child']+'"')
            if desc['posCol'] and desc['posCol'] not in tables[desc['child']]['header']:
                raise RuntimeError('Invalid position column: No column "'+desc['posCol']+'" in table "'+desc['child']+'"')

        d = pd.read_csv(path, sep='\t', quotechar='"', engine='python', names=desc['header'], skiprows=desc['start'], nrows=desc['count'])
        d.child = desc['child']
        d.id_col = desc['idCol']
        d.pos_col = desc['posCol']
        d.units = desc['units']
        data[name] = d

    for name in data:
        d = data[name]
        if d.empty and d.child:
            d_new = pd.DataFrame(index=list(range(data[d.child][d.id_col].max())))
            d_new.child = d.child
            d_new.id_col = d.id_col
            d_new.pos_col = d.pos_col
            d_new.units = d.units
            data[name] = d_new

    warnings.resetwarnings()

    return data


def dump(data, path):
    with open(path, 'w') as file:
        for name, d in data.items():
            file.write('# '+name)
            if d.child:
                file.write(' : '+d.child+' ('+d.id_col+(', '+d.pos_col if d.pos_col else '')+')')
            file.write('\n')

            if not d.empty:
                header = [p[0]+' ['+p[1]+']' if p[1] else p[0] for p in zip(d.columns, d.units)]
                d.to_csv(file, sep='\t', quotechar='"', header=header, index=False)
            file.write('\n')
        
