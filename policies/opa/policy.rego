package example

default allow = false

allow if {
    input.method = "GET"
    input.path = ["api", "v1", "resources"]
}

allow if {
    input.method = "POST"
    input.path = ["api", "v1", "resources"]
    input.user.role == "admin"
}

allow if {
    input.method = "DELETE"
    input.path = ["api", "v1", "resources", resource_id]
    input.user.role == "admin"
    resource_id = input.path[3]
}
