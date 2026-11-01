"""Resume only report construction after QA completed; never re-evaluate passing QA."""
from pathlib import Path
import ast
p=Path(__file__).resolve().parent
s=(p/'qa_and_report.py').read_text()
imports=s[:s.index("assert not (P/'qa_results.md')")]
counts_line=(p/'qa_results.md').read_text().splitlines()[2].split('** ')[1]
counts=ast.literal_eval(counts_line)
report=s[s.index("s=pd.read_csv(P/'comparables.csv')"):]
exec(compile(imports+'\ncounts='+repr(counts)+'\n'+report,str(p/'qa_and_report.py'),'exec'))
