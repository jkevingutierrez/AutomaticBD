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
        # all(item in two for item in one)
        return set(one).issubset(set(two))

    @staticmethod
    def remover_index(list, index):
        # [item for j, item in enumerate(list) if index != j]
        return list[:index] + list[index + 1:]
