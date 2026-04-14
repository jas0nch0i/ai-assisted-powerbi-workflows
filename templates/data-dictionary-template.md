# Data Dictionary Template

Use this template to document fields in a semantic model or reporting dataset.

| Field Name | Business Definition | Source Table | Data Type | Transformation Notes | Usage Notes |
|---|---|---|---|---|---|
| Example: Region | Geographic region assigned to each record | DimRegion | Text | Standardized from source values | Used for slicers and drill-down |
| Example: OpenDate | Date the case was opened | FactOperations | Date | Converted to date format | Used in trend reporting |

## Instructions

- Add one row per field.
- Keep business definitions short and clear.
- Note any calculations or transformations that affect how the field should be interpreted.
