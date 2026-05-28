import os
root=r'd:\GenAiProject1\.venv\Lib\site-packages'
for dirpath,dirnames,filenames in os.walk(root):
    for fn in filenames:
        if fn.endswith('.py'):
            path=os.path.join(dirpath,fn)
            try:
                with open(path,'r',encoding='utf-8') as f:
                    txt=f.read()
                if 'get_tracing_context' in txt:
                    print(path)
            except Exception:
                pass
print('done')
