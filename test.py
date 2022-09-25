import re

cr_re = re.compile("Cr\. ([a-zA-Z0-9\-]*)\.")

match0 = cr_re.findall("Cr. R.  F.S.")
print(match0)

match0 = cr_re.findall("(2-2) Cr. 3.  F.S.SS.")
print(match0)

match0 = cr_re.findall("F.S.SS.")
print(len(match0))


fall_re = re.compile("F\.*") 
spring_re = re.compile("[^S]S\.*") 
summer_re = re.compile("SS\.*")

txt = "(2-2) Cr. 3.  F.S.S."
match0 = fall_re.search(txt)
print(match0)
match0 = spring_re.search(txt)
print(match0)
match0 = summer_re.search(txt)
print(match0)