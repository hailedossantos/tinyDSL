from tinyDSL import TinyDSL

dsl = TinyDSL()

queries = [
"""{"fields": ["url", "http_code"]}""",
"""{
"fields": ["url"],
"filters": {
"field": "http_code", "value": 200
}
}""",
"""{
"fields": ["url"],
"filters": {
"field": "http_code", "value": 200,
"predicate": "gt"
}
}""",
"""{
"fields": ["url"],
"filters": {"and": [
{
"field": "http_code",
"value": 200,
"predicate": "gt"
},
{
"field": "h1",
"value": "Obama",
"predicate": "contains"
}
]
}
}"""]

for query in queries:
    print("\nJSON query:")
    print query
    print("\nSQL query:")
    print dsl.convertQuery(query)
