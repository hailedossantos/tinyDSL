import sys
import json

sys.argv

data = json.loads(argv[0])

class TinyDSL:
    """Tiny DSL class"""
    predicates = {
        "equal": "=",
        "lt": "<",
        "gt": ">",
        "contains": "LIKE"
    }
    logic_operators = ["and", "or"]

    def convertQuery(self, queryString):
        json_query = loads(queryString)
        syntaxOK = checkSyntax(json_query)
        if syntaxOK:
            return getSQL(json_query)

    def getSQL(json_query):
        result = "SELECT"
        result.append(", ".join(json_query.get("fields")))
        result.append("\t")
        result.append("FROM crawls\t")
        if json_query.has_key("filters"):
            result.append("WHERE ")
            result.append(getFilters(json_query.get("filters")))

    def getFilters(json_filter):
        if len(json_filter) == 1:
            [(operator, child_filters)] = json_filter.items()
            return getFilters(child_filters[0])+" "+operator.upper()+" "+getFilters(child_filters[1])
        else:
            return json_filter.get("field")+" "+predicates.get(json_filter.get("predicate"))+" "+json_filter.get("value")

    def checkSyntax(json_query):
