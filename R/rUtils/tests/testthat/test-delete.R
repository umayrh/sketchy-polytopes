library(testthat)
library(rUtils)

test_that("delete data.table directly", {
  target1 = data.table::data.table(A=5:1,B=letters[5:1])
  delete.data.table(target1, ls(), environment())
  expect_false(exists("target1"))
})

test_that("delete data.table by reference", {
  target1 = data.table::data.table(A=5:1,B=letters[5:1])
  target2 = target1
  target2[1, A := 6]
  delete.data.table(target2, ls(), environment())
  expect_false(exists("target1"))
  expect_false(exists("target2"))
})
