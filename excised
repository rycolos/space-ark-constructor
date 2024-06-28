#name validation
if not name:
    raise ValueError("Missing name")

    #ship class validation
    @property #getter
    def sclass(self):
        return self._sclass

    @sclass.setter #setter
    def sclass(self, sclass):
        if sclass not in [i['sclass'] for i in sclass_details]:
            raise ValueError("Invalid class")
        self._sclass = sclass

    #outer hull validation
    @property #getter
    def outer_hull_strength(self):
        return self._outer_hull_strength

    @sclass.setter #setter
    def outer_hull_strength(self, outer_hull_strength):
        if outer_hull_strength not in strength_list:
            raise ValueError("Invalid strength")
        self._outer_hull_strength = outer_hull_strength