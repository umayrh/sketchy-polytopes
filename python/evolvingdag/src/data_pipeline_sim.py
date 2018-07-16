##
# Simulates a data pipeline's execution over time
# - Data pipeline graph
#   - properties: name/execution id, tags
#   - nodes are tasks; edges represent dependency
#       - Future work: edges also represent a set of data dependencies
# - Node
#   - Label is Task
#   - Properties must include a unique name, and other tags
# - Open questions:
#   - Should task tags be properties or labels?
##
