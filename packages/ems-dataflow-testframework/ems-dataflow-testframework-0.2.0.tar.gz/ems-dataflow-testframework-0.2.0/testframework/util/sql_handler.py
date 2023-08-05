import logging


class SqlHandler(object):

    def build_query(self, path_to_query, dynamic_content):
        with open(path_to_query, "r") as input:
            result = input.readlines()
        query = "".join(result)
        formatted_query = query.format(**dynamic_content)
        logging.debug(formatted_query)

        return formatted_query
