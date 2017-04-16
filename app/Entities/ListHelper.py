class ListHelper:
    @staticmethod
    def union(a, b):
        return list(set(a) | set(b))

    @staticmethod
    def diferencia(a, b):
        b = set(b)
        return [item for item in a if item not in b]

    @staticmethod
    def contiene_todos(one, two):
        # all(x in two for x in one)
        return set(one).issubset(set(two))

    @staticmethod
    def remover_index(list, index):
        # [dependencia for j, dependencia in enumerate(list) if index != j]
        return list[:index] + list[index + 1:]
