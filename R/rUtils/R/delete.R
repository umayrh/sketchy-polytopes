#' This function allows deleting a data.table by removing all references to it in a given environment.
#' In memory-strapped environments, we'd like to help the garbage collector reclaim memory that's not 
#' logically referenced anymore.
#' Note that any errors will be logged without a traceback for uninterrupted execution.
#' TODO: Note that this function is NOT thread-safe.
#'
#' @param target data.table object to be deleted
#' @param environObjs list of R objects in the given environment (see: ls())
#' @param environ environment to search for this object (default: .GlobalEnv)
#'
#' @export
#' @importFrom data.table address
#'
delete.data.table = function(target, environ_objs, environ = .GlobalEnv) {
  tryCatch({
    # TODO: document the mysteries of get() here
    target_obj = tryCatch({get(target, envir = environ)}, error = function(x){return (target)})
    target_address = address(target)
    message(paste("data.table address", target_address))
    object_groups_by_address = split(environ_objs, sapply(environ_objs, function(x) {address(get(x, envir=environ))}))
    target_objects = object_groups_by_address[[toString(target_address)]]
    message(paste("Objects referencing", target_address, ": ", toString(target_objects)))
    rm(list = target_objects, envir = environ)
  },
  error = function(cond) {
    message(toString(cond))
  })
}
