
# Class: clinical modifier


Used to characterize and specify the phenotypic abnormalities defined in the Phenotypic abnormality subontology, with respect to severity, laterality, age of onset, and other aspects

URI: [biolink:ClinicalModifier](https://w3id.org/biolink/vocab/ClinicalModifier)

![img](images/ClinicalModifier.png)

## Parents

 *  is_a: [Attribute](Attribute.md) - A property or characteristic of an entity

## Referenced by class

 *  **[Association](Association.md)** *[clinical modifier qualifier](clinical_modifier_qualifier.md)*  <sub>OPT</sub>  **[ClinicalModifier](ClinicalModifier.md)**

## Attributes


### Inherited from named thing:

 * [id](id.md)  <sub>REQ</sub>
    * Description: A unique identifier for a thing. Must be either a CURIE shorthand for a URI or a complete URI
    * range: [IdentifierType](IdentifierType.md)
    * inherited from: [NamedThing](NamedThing.md)
    * in subsets: (translator_minimal)
 * [name](name.md)  <sub>REQ</sub>
    * Description: A human-readable name for a thing
    * range: [LabelType](LabelType.md)
    * inherited from: [NamedThing](NamedThing.md)
    * in subsets: (translator_minimal)
 * [category](category.md)  <sub>1..*</sub>
    * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In a neo4j database this MAY correspond to the neo4j label tag
    * range: [IriType](IriType.md)
    * inherited from: [NamedThing](NamedThing.md)
    * in subsets: (translator_minimal)
