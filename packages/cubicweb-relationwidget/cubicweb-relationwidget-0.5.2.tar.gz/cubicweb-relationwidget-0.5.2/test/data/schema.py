from yams.buildobjs import EntityType, RelationDefinition, String


class MyThing(EntityType):
    label = String(required=True)


class my_relation(RelationDefinition):
    subject = 'CWUser'
    object = ('CWGroup', 'MyThing')
