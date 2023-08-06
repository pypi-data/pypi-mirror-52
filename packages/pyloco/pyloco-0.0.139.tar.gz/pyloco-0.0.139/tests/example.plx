text@arg = "data", type=str, help="text to print"
output @ forward = "textout", help="printed text"

#s = "${text:arg}$"
#print(s)

echo@shell = echo __{text:arg}__

[forward*]

output = "Printed text is %s"%str(echo[1])

[attribute*]

__doc__ = """my plx script

This script is an example plx script
"""

# print is not allowed as it is used a keyword in python2
[display@True]

print("True")
