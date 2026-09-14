# API conventions

Command methods use the SCPI path in their docstring and map naturally to
Python names. A method with an optional `value` is a combined query/setter:
call it without a value to query, or pass a value to write. Query-only methods
return a typed value; setters return `None`.

Enums accept their enum member, its integer value, or the instrument's string
form where the method annotation permits it. Raw SCPI access is available via
`SCPIBase.write`, `SCPIBase.query`, and `SCPIBase.query_block`.
