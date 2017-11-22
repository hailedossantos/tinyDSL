import sys
import json

# sys.argv

# data = json.loads(argv[0])

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
        result += ", ".join(json_query.get("fields"))
        result += "\t"
        result += "FROM crawls\t"
        if json_query.has_key("filters"):
            result += "WHERE "
            result += getFilters(json_query.get("filters"))

    def getFilters(json_filter):
        if len(json_filter) == 1:
            [(operator, child_filters)] = json_filter.items()
            return getFilters(child_filters[0])+" "+operator.upper()+" "+getFilters(child_filters[1])
        else:
            return json_filter.get("field")+" "+predicates.get(json_filter.get("predicate"))+" "+json_filter.get("value")

    def checkSyntax(json_query):
        if len(json_query) > 2:
            return False
        if not json_query.has_key("fields"):
            return False
        if not json_query.get("fields"):
            return False
        if json_query.has_key("filters"):
            return checkFiltersSyntax(json_query.get("filters"))

        return True

    def checkFiltersSyntax(filters):
        if filters.has_key("field"):
            if not filters.has_key("value"):
                return False
            if len(filters) == 3:
                if not filters.has_key("predicate"):
                    return False
                if not predicates.has_key(filters.get("predicate")):
                    return False
            return True
        elif len(filters) == 1:
            [(operator, child_filters)] = filters.items()
            if not operator in logic_operators:
                return False
            if not len(child_filters) == 2:
                return False
            if not (checkFiltersSyntax(child_filters[0]) and checkFiltersSyntax(child_filters[1])):
                return False
            return True
        else:
            return False
