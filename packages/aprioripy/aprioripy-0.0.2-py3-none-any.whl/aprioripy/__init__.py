import pandas as pd
import itertools


class Aprioripy:
    
    def __init__(self,
                 table,
                 convert=True,
                 items=[],
                 excluded_items=[],
                 positive_label=1):

        def converter(table):
            item_list = list(set(sum([x.split(", ") for x in table["items"].tolist()], [])))
            item_list.sort()
            
            new_table = []
            for row in table["items"].tolist():
                table = {}
                for item in item_list:
                    if item in row:
                        table[item] = 1
                    else:
                        table[item] = 0
                new_table.append(table)

            table = pd.DataFrame(new_table)

            return table

        if convert:
            table = converter(table)
        
        if len(items) == 0:
            items = table.keys()
            
        if len(excluded_items) != 0:
            items = [item for item in items if item not in excluded_items]
        
        table = table.filter(items=items)
        
        for item in items:
            table[item] = table[item].apply(lambda x: 1 if x == positive_label else 0)
        
        self.frequency_table = pd.DataFrame({
            "item": items,
            "frequency": [table[item].tolist().count(1)/len(table) for item in items]
        })
        
        self.table = table  
        
    def apriori(self, min_support=0):
        
        frequency_table = self.frequency_table[self.frequency_table["frequency"] >= min_support]
        
        self.association_tables = {
            "L1": frequency_table
        }
        
        for step in range(2, len(self.frequency_table["item"].tolist())):
            itemsets = list(itertools.combinations(self.frequency_table['item'], step))
            
            itemset_table = pd.DataFrame({
                "itemset": [itemset for itemset in itemsets]
            })
            
            def count_itemsets(items):
                table = self.table
                
                for item in items:
                    table = table[table[item] == 1]
                    
                return len(table)/len(self.table)
            
            itemset_table["frequency"] = itemset_table["itemset"].apply(lambda x: count_itemsets(x))
            
            association_table = itemset_table[itemset_table["frequency"] >= min_support]

            if len(association_table) > 0:
                self.association_tables["L"+str(step)] = association_table

def test():
    test_table = pd.DataFrame({
        "items": ["1, 3, 4", "2, 3, 5", "1, 2, 3, 5", "2, 5"]
    })

    print("Test table")
    print(test_table)

    ap = Aprioripy(table=test_table)

    print("\nFrequency table:")
    print(ap.frequency_table)

    ap.apriori(min_support=0.5)

    for i in ap.association_tables.keys():
        print("\nAssociation table " + i)
        print(ap.association_tables[i])
    
    test_table = pd.DataFrame(
        [
            {"1": 1, "2": 0, "3": 1, "4": 1, "5": 0},
            {"1": 0, "2": 1, "3": 1, "4": 0, "5": 1},
            {"1": 1, "2": 1, "3": 1, "4": 0, "5": 1},
            {"1": 0, "2": 1, "3": 0, "4": 0, "5": 1}
        ]
    )
    
    print("\nTest table:")
    print(test_table)

    ap = Aprioripy(table=test_table, convert=False)

    print("\nFrequency table:")
    print(ap.frequency_table)

    ap.apriori(min_support=0.5)

    for i in ap.association_tables.keys():
        print("\nAssociation table " + i)
        print(ap.association_tables[i])


if __name__ == '__main__':
    test()
    