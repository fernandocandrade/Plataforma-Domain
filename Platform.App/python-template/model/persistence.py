class Persistence:

    def persist(self, objs):
        to_create  = []
        to_update  = []
        to_destroy = []
        for o in objs:
            if not self.is_valid_changed_obj(o):
                continue
            if self.is_to_create(o):
                to_create.append(o)
            elif self.is_to_update(o):
                to_update.append(o)
            elif self.is_to_destroy(o):
                to_destroy.append(o)
        result = self.create(to_create)
        result = result + self.update(to_update)
        self.destroy(to_destroy)
        return result

    def create(self, objs):
        for o in objs:
            o["id"] = "1"
        return objs

    def update(self, objs):
        return objs

    def destroy(self, objs):
        return []

    def is_to_create(self, obj):
        return obj["_metadata"]["changeTrack"] == "create"

    def is_to_update(self, obj):
        return obj["_metadata"]["changeTrack"] == "update" and "id" in obj

    def is_to_destroy(self, obj):
        return obj["_metadata"]["changeTrack"] == "destroy" and "id" in obj

    def is_valid_changed_obj(self,obj):
        if not "_metadata" in obj:
            return False
        if not "changeTrack" in obj["_metadata"]:
            return False
        if obj["_metadata"]["changeTrack"] not in ["create", "update","destroy"]:
            return False
        return True


