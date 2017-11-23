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
        json_query = json.loads(queryString)
        syntaxOK = self.checkSyntax(json_query)
        if syntaxOK:
            return self.getSQL(json_query)

    def getSQL(self, json_query):
        result = "SELECT "
        result += ", ".join(json_query.get("fields"))
        result += "\n"
        result += "FROM crawls"
        if json_query.has_key("filters"):
            result += "\nWHERE "
            result += self.getFilters(json_query.get("filters"))
        return result

    def getFilters(self, json_filter):
        if len(json_filter) == 1:
            [(operator, child_filters)] = json_filter.items()
            return self.getFilters(child_filters[0])+" "+operator.upper()+" "+self.getFilters(child_filters[1])
        else:
            return (json_filter.get("field")+" "+
                    (self.predicates.get(json_filter.get("predicate")) if json_filter.has_key("predicate") else "=")+" "+
                    str(json_filter.get("value")))

    def checkSyntax(self, json_query):
        if len(json_query) > 2:
            return False
        if not json_query.has_key("fields"):
            return False
        if not json_query.get("fields"):
            return False
        if json_query.has_key("filters"):
            return self.checkFiltersSyntax(json_query.get("filters"))
        return True

    def checkFiltersSyntax(self, filters):
        if filters.has_key("field"):
            if not filters.has_key("value"):
                return False
            if len(filters) == 3:
                if not filters.has_key("predicate"):
                    return False
                if not self.predicates.has_key(filters.get("predicate")):
                    return False
            return True
        elif len(filters) == 1:
            [(operator, child_filters)] = filters.items()
            if not operator in self.logic_operators:
                return False
            if not len(child_filters) == 2:
                return False
            if not (self.checkFiltersSyntax(child_filters[0]) and self.checkFiltersSyntax(child_filters[1])):
                return False
            return True
        else:
            return False
